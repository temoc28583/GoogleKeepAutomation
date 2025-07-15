import os
import pickle
import gkeepapi
from anthropic import Anthropic

class Tag:
    def __init__(self, api_key, email, pass_word, categories=None, token_file="keep_tok.pkl"):
        self.api_key = api_key
        self.categories = categories or [
            'SEO', 'ads', 'marketing', 'technology',
            'Product management', 'business management',
            'Networking', 'business strategy'
        ]
        self.token_file = token_file
        self.email = email
        self.pass_word = pass_word
        self.keep = self.keep_session()
        self.claude = Anthropic(api_key=api_key)


    def keep_session(self):
        keep = gkeepapi.Keep()
        # Try to resume from token file if it exists
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as f: #the purpose of token_file is so that it stores the token as part of the keep object and prevents multiple login attempts
                    token=pickle.load(f) #use pickle.load to extract session information and stores it in token so it can allow the user to resume their session from a binary file
                    keep.resume(token)
                    print("Resumed session from token file.")
            else:
                # If no token file, login freshly
                success = keep.authenticate(self.email, self.pass_word)  # Use your app password here
                if not success:
                    print("Google Keep login failed.")
                    return None
                print("Logged in fresh and creating token file.")
                with open(self.token_file, 'wb') as f:
                    pickle.dump(keep.getMasterToken(), f) #use dump to store the resumed session from the master token in the form of a file
        except Exception as e:
            print(f"Exception during session resume/login: {e}")
            return None

        return keep

    def fetch_notes(self, notes_amount=100):
        if self.keep is None:
            print("No active Keep session.")
            return []

        all_notes = self.keep.all()
        cleaned_notes = []

        for note in all_notes:
            # Get note content - prefer text if available, else title
            content = note.text.strip() if note.text else note.title.strip() if note.title else ''
            if content and len(cleaned_notes) < notes_amount:
                cleaned_notes.append(content)

        return cleaned_notes

    def est_prompt(self, note, categories):
        category_list = ":".join(categories)
        prompt = f"""
As a tagging assistant, use only the tags in the categories and assign them to notes based on your understanding.

Categories:
[{category_list}]

Note:
{note}
"""
        return prompt

    def claude_process(self, note_text, categories):
        prompt = self.est_prompt(note_text, categories)
        response = self.claude.completions.create(
            model="claude-sonnet-4-20250514",
            prompt=prompt,
            max_tokens_to_sample=800,
            stop_sequences=[note_text]
        )
        return response.completion  # extract the actual text from response

    def clean_notes(self, raw_prompt, categories):
        tags = [tag.strip() for tag in raw_prompt.split(',')]
        return [tag for tag in tags if tag in categories]

    def consolidate_tags(self, note_texts):
        full_prompt = []
        for i, note in enumerate(note_texts, start=1):
            tags_raw = self.claude_process(note, self.categories)
            clean_tags = self.clean_notes(tags_raw, self.categories)
            full_prompt.append({"Tags": clean_tags, f"Note {i}": note})
        return full_prompt
