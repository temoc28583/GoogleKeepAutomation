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

        for title, info in self.notes.items(): #title is the ky and info is the value which is a dictionary with tags and content
            tags = info.get("tags", [])
            if not tags:
                tags = ['untagged'] #this tells us that there were no tages for the note
            content = info.get("Content", "")
            markdown_text = "---\n"
            markdown_text += f"## {title}\n"
            markdown_text += f"**Tags:** {', '.join(tags)}\n\n"
            markdown_text += f"{content}\n\n---\n\n"
            marked_dict[title] = markdown_text #dictionary with title as key and markdown string as value

        return marked_dict





