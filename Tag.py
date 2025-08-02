from anthropic import Anthropic
from Notefetch import Notefetch

class Tag:
    def __init__(self, api_key, notion_obj, categories=None, token_file="keep_tok.pkl"):
        self.api_key = api_key #claude or anthropic API key
        self.notion_obj = notion_obj #stores notion object to fetch notes
        self.token_file = token_file
        self.claude = Anthropic(api_key=api_key) #calls antrophic api key to call claude llm model
        self.categories = categories or [
            'SEO', 'ads', 'marketing', 'technology',
            'Product management', 'business management',
            'Networking', 'business strategy'
        ] #categories or tags used to tag the notes

    def fetch_notes(self, notes_amount=100):
        if self.notion_obj is None:
            print("No active Notion session.")
            return {}

        all_notes_dict = self.notion_obj.get_all_notes() #returns a dictionary of all the notes in the notion database(which ir raw)
        cleaned_notes = {}

        for title, content in all_notes_dict.items(): #keys are the title of the notes and values are the content of the notes
            note_content = content.strip() if content.strip() else title.strip() #removes leading and trailing whitespaces for the content else title if there is no content
            if note_content and len(cleaned_notes) < notes_amount:
                cleaned_notes[title.strip()] = note_content #appends the title and content to the cleaned_notes dictionary where the title does not have leading or trailing whitespaces
        """_summary_
          "Marketing Plan": "Steps for new campaign...",
  "Tech Update": "New iOS released..."
}

   
        """
        return cleaned_notes

    def est_prompt(self, note_text, categories):
        category_list = ", ".join(categories) #converts list into one string with commas seperating the categories
        prompt = f"""
You are an assistant that assigns tags to notes.

Given the categories below, read the Note and respond **only** with a comma-separated list of zero or more tags that apply.

Categories:
[{category_list}]  #creates a prompt sent to claude with the categories they must choose from to tag the note

Note:
{note_text}

Respond only with a comma-separated list of tags from the categories.
If no categories apply, respond with 'untagged'.
"""
        return prompt



    def claude_process(self, note_text, categories):
        try:
            prompt = self.est_prompt(note_text, categories)
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    } #creates a message to send to claude(chat object) (api response object) based on note-text which is a set of notes
                ]#Ads, Marketing\nSEO"
            )
            return response.content.text.strip() #returns response from claude as a string such as the tags(seo, marketing or untagged)
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return ""

    def clean_notes(self, raw_tags_text, categories):
        if not raw_tags_text:
            return []

        # Replace newlines with commas and split, strip spaces "seo,marketing"
        normalized = raw_tags_text.replace('\n', ',').lower() #splits raw tages with commans and coverts to lower case for matching
        #returns "seo", "marketing"
        raw_tags = [tag.strip() for tag in normalized.split(',') if tag.strip()] #splits continous string into a list of tags and removes leading and trailing whitespaces(marketingseo->marketing, seo)
        categories_lower = [cat.lower() for cat in categories] #->[seo, ads]

        cleaned = []
        for tag in raw_tags: #checks if the tag is in categories_lower and it already has not been added to cleaned
            if tag in categories_lower and tag not in cleaned:
                idx = categories_lower.index(tag) #returns index of tag in categories_lower
                cleaned.append(categories[idx]) #returns list of cleaned tags that match the categories list
        return cleaned

    def consolidate_tags(self, note_dict):
        """
        Tags notes and returns dict with tags for each note(cateogirze notes based on the tags)
        {tag: [(title, note_content), ...]}
        {
  "ads": [("Ad Campaign", "Launching Instagram ads for Gen Z")],
  "marketing": [("Ad Campaign", "Launching Instagram ads for Gen Z")]
}
        """
        tagged_notes = {}

        for title, note in note_dict.items():
            raw_tags_text = self.claude_process(note, self.categories) #gets raw tages from claude for tagging "seo,marketing"
            print(f"Raw tags from Claude for note '{title}': {raw_tags_text}")  # Printed for debugging through each notes
            clean_tags = self.clean_notes(raw_tags_text, self.categories) #cleans up the raw tags from claude using clean_notes
            #["ads", "marketing", "SEO"] → ["ads", "marketing"]
            if clean_tags:
                for tag in clean_tags:
                    tagged_notes.setdefault(tag, []).append((title, note)) #adds [] for the tag if it does not exist and appends the title and notes pair if associated with the tag
            else:
                print(f"No valid tags found for note '{title}'. Marking as untagged.")
                tagged_notes.setdefault('untagged', []).append((title, note)) #if no tag exists for the note, it appends the title and notes with untagged

        return tagged_notes





