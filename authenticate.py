import os
import pickle
import gkeepapi
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class AuthHandle:
    def __init__(self):
        self.keep_auth = None  # gkeepapi.Keep() instance after auth
        self.drive_auth = None  # Google Drive API client after auth

        self.credentials_path = "credentials.json"  # OAuth2 client secrets file
        self.token_drive_path = "token_drive.pickle"  # Store Drive token here
        self.drive_scopes = ['https://www.googleapis.com/auth/drive.file']

    def login_gkeep(self, user_name, pass_word):
        keep = gkeepapi.Keep()

        # Attempt to log in
        try:
            success = keep.authenticate(user_name, pass_word)
            if success:
                self.keep_auth = keep
                print("Google Keep login successful")
                return True
            else:
                print("Google Keep login unsuccessful")
                return False
        except Exception as e:
            print(f"Something went wrong during Keep login: {e}")
            return False

    def login_drive(self):
        creds = None

        # Load token for Drive if it exists
        if os.path.exists(self.token_drive_path):
            with open(self.token_drive_path, 'rb') as token_file:
                creds = pickle.load(token_file)

        # If no valid token, perform OAuth2 flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path,
                    self.drive_scopes
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for next time
            with open(self.token_drive_path, 'wb') as token_file:
                pickle.dump(creds, token_file)

        # Build Drive API client
        self.drive_auth = build('drive', 'v3', credentials=creds)
        print("Google Drive login successful")
        return self.drive_auth

    def get_keep_auth(self):
        return self.keep_auth

    def get_drive_auth(self):
        return self.drive_auth
