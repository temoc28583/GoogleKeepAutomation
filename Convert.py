class Convert:
    def __init__(self, notes):
        """
        :param notes: Dictionary with notes in format:
         {
            "NoteTitle1": {"tags": ['seo'], "Content": "..."},
            "NoteTitle2": {"tags": ['tech'], "Content": "..."}
         }
        """
        self.notes = notes

    def markNotes(self):
        """
        Convert notes dictionary into markdown strings.
        Returns dict with note title as key and markdown string as value.
        """
        marked_dict = {}

        for title, info in self.notes.items(): #info is a dictionary with tags(list) and the content itself {"tags": ["seo"], "Content": "..."}


            tags = info.get("tags", []) #reiteves tag list from info dictionary, if no tags, returns empty list
            content = info.get("Content", "") #returns content from info dictionary, if no content, returns empty string
            markdown_text = f"## {title}\n"
            markdown_text += f"**Tags:** {', '.join(tags)}\n\n"
            markdown_text += f"{content}\n\n---\n\n"
            marked_dict[title] = markdown_text

        return marked_dict




