from googleapiclient.http import MediaFileUpload
import os
import re
import time

class Drive:
    def __init__(self, tagged_notes, service, folder_id=None):
        self.tagged = tagged_notes  # dict {title: markdown_text}
        self.service = service
        self.folder_id = folder_id or os.getenv("FOLDER_ID")

    def sep_file(self, file_name):
        """Remove illegal characters from filename"""
        return re.sub(r'[\\/*?:"<>|]', "_", file_name)

    def save_and_upload_individual_notes(self):
        """Save each note as its own markdown and upload to Drive"""
        uploaded_files = {}

        if not self.service:
            print("Drive service not established.")
            return uploaded_files

        for title, markdown_text in self.tagged.items():
            safe_title = self.sep_file(title)
            file_name = f"{safe_title}.md"

            # 1️⃣ Save markdown locally
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(markdown_text)

            # 2️⃣ Upload to Google Drive
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id],
                'mimeType': 'text/markdown'
            }
            media = MediaFileUpload(file_name, mimetype='text/markdown')

            try:
                uploaded_file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                file_id = uploaded_file.get('id')
                uploaded_files[title] = file_id
                print(f"✅ Uploaded {file_name} (File ID: {file_id})")

            except Exception as e:
                print(f"❌ Failed to upload {file_name}: {e}")

            # 3️⃣ Try to remove local file safely
            time.sleep(0.1)  # Let Windows release file handle
            try:
                os.remove(file_name)
            except PermissionError:
                print(f"⚠ Could not delete {file_name} (still in use). Skipping.")

        return uploaded_files

