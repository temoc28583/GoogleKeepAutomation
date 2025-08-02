from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
FOLDER_ID = os.getenv("FOLDER_ID", '18gCIAXSBe3uOjz2KgUTc2K7iZ9Pfoz1e')


class Drive:
    def __init__(self, tagged_notes, service, file_name, folder_id=None):
        self.tagged = tagged_notes
        self.service = service
        self.mark_file = "tagged_notes.md"
        self.file_name = file_name
        self.folder_id = folder_id or FOLDER_ID

    def to_markdown(self):
        full_markdown = "\n".join(self.tagged.values())
        with open(self.mark_file, 'w', encoding='utf-8') as f:
            f.write(full_markdown) #combined all the notes into one markdown string and writes to a file
        print(f"Markdown notes saved to {self.mark_file}")

    def upload_file(self, file_path, file_name, mime_type='text/markdown'):
        if not self.service: #this is the drive service object that will recongize the reques to upload a file
            print("Drive service not established.")
            return None

        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            return None

        file_metadata = {
            'name': file_name,
            'parents': [self.folder_id],
            'mimeType': mime_type
        } #meta data for the file consiting of the name, ID of the folder where it will be uploaded and the type of file

        media = MediaFileUpload(file_path, mimetype=mime_type) #stores file in object to allow for streaming

        try:
            uploaded_file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute() #performs the upload task by calling files().create method by passing information and content and fields
            print(f"Uploaded {file_name} to Drive. File ID: {uploaded_file.get('id')}")
            return uploaded_file.get('id')
        except Exception as e:
            print(f"Failed to upload {file_name}: {e}")
            return None

    def save_and_upload(self):
        self.to_markdown() #saves notes to markdown which is later uploaded to drive
        return self.upload_file(
            file_path=self.mark_file,
            file_name=self.file_name,
            mime_type='text/markdown'
        )
