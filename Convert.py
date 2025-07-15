import gkeepapi

class Convert:
    def __init__(self, fullNotes):
        self.notes = fullNotes  # Store the list of notes to be converted

    def markNotes(self):
        markdown_text = ""  # Initialize an empty string to store the final markdown content

        for note in self.notes:
            tags = note.get("Tags", [])  # Get the list of tags from the note, or empty list if not present

            # Find the key in the note dictionary that holds the note content (not 'Tags')
            contentKey = None
            for key in note:
                if key != "Tags":
                    contentKey = key
                    break  # Stop at the first non-Tag key

            # Get the actual note content using the identified key
            content = note.get(contentKey) if contentKey else ""

            # If there are any tags, format them and add to markdown output
            if tags:
                tags_mark = "#Tags# " + ": ".join(tags)  # Join tags with ": ", add a label
                markdown_text += f"{tags_mark}\n---\n"   # Separate tags from content using horizontal line

            # Add the note content followed by two newlines
            markdown_text += f"{content}\n\n"

        return markdown_text


       
            
            
                
            
            



        
    