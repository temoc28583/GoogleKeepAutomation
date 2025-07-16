from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')

TOKEN_FILE = 'token.pickle'
FOLDER_ID = '18gCIAXSBe3uOjz2KgUTc2K7iZ9Pfoz1e'  # Use just the folder ID, not the URL

class Drive:
    def __init__(self, tagged_notes):
        self.tagged = tagged_notes
        self.json_file = "tagged_notes.json"
        self.service = None

    def to_json(self):
        """Write tagged notes to a local JSON file."""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.tagged, f, indent=4)
        print(f"Tagged notes saved to {self.json_file}")

    def login_drive(self):
        """Authenticate and initialize Google Drive service."""
        creds = None

        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as file:
                creds = pickle.load(file)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the new token
            with open(TOKEN_FILE, 'wb') as f:
                pickle.dump(creds, f)

        # Build the Drive service
        self.service = build("drive", "v3", credentials=creds)

    def upload_drive(self):
        """Upload the JSON file to Google Drive."""
        if not self.service:
            print("Drive service not established.")
            return None

        file_metadata = {
            'name': 'TaggedNotes.json',
            'parents': [FOLDER_ID],
            'mimeType': 'application/json'
        }

        media = MediaFileUpload(self.json_file, mimetype='application/json')

        uploaded_file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"File uploaded to Drive. File ID: {uploaded_file.get('id')}")




        
    
    





