from anthropic import Anthropic

class Tag:
    def __init__(self, api_key, notion_obj, categories_synonyms):
        """
        :param api_key: Anthropic Claude API key
        :param notion_obj: Notefetch instance for fetching notes
        :param categories_synonyms: dict mapping categories to list of synonyms
        """
        self.api_key = api_key
        self.notion_obj = notion_obj
        self.claude = Anthropic(api_key=api_key)
        self.categories_synonyms = categories_synonyms
        self.categories = list(categories_synonyms.keys())
        
        # Build synonym -> canonical category mapping
        self.synonym_map = {}
        for category, synonyms in categories_synonyms.items():
            # include the category name itself
            self.synonym_map[category.lower()] = category
            for syn in synonyms:
                self.synonym_map[syn.lower()] = category

    def fetch_notes(self, notes_amount=None):
        """Fetch notes from Notion. notes_amount=None means unlimited."""
        if notes_amount is None:
            notes_amount = float('inf')  # unlimited

        if self.notion_obj is None:
            print("No active Notion session.")
            return {}

        all_notes_dict = self.notion_obj.get_all_notes()
        cleaned_notes = {}

        for title, content_dict in all_notes_dict.items():
            # content_dict is like {"id":..., "content": "..."}
            content = content_dict.get("content", "").strip()
            note_content = content if content else title.strip()
            if notes_amount is None:
                notes_amount = float('inf') 
            if note_content and len(cleaned_notes) < notes_amount:
                cleaned_notes[title.strip()] = note_content
                print(f"DEBUG: Note '{title}' content length = {len(note_content)}")

        return cleaned_notes

    def est_prompt(self, note_text, categories):
        """Build prompt for Claude."""
        category_list = ", ".join(categories)
        prompt = f"""
You are an assistant that assigns tags to notes.

Given the categories below, read the Note and respond **only** with a comma-separated list of zero or more tags that apply.

Categories:
[{category_list}]

Note:
{note_text}

Respond only with a comma-separated list of tags from the categories.
If no categories apply, respond with 'untagged'.
"""
        return prompt

    def claude_process(self, note_text, categories):
        """Call Anthropic Claude API to get tags."""
        try:
            prompt = self.est_prompt(note_text, categories)
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return ""

    def clean_notes(self, raw_tags_text):
        """Map raw tags to canonical categories via synonyms."""
        if not raw_tags_text:
            return []

        normalized = raw_tags_text.replace('\n', ',').lower()
        raw_tags = [tag.strip() for tag in normalized.split(',') if tag.strip()]

        cleaned = []
        for tag in raw_tags:
            canonical = self.synonym_map.get(tag)
            if canonical and canonical not in cleaned:
                cleaned.append(canonical)

        return cleaned

    def consolidate_tags(self, note_dict):
        """Return dict {tag: [(title, note_content), ...]}."""
        tagged_notes = {}

        for title, note in note_dict.items():
            raw_tags_text = self.claude_process(note, self.categories)
            print(f"Raw tags from Claude for note '{title}': {raw_tags_text}")
            clean_tags = self.clean_notes(raw_tags_text)
            if clean_tags:
                for tag in clean_tags:
                    tagged_notes.setdefault(tag, []).append((title, note))
            else:
                print(f"No valid tags found for note '{title}'. Marking as Uncategorized.")
                tagged_notes.setdefault('Uncategorized', []).append((title, note))

        return tagged_notes










