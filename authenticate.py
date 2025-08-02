import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from notion_client import Client


class AuthHandle:
    def __init__(self):
        self.notion_token = None
        self.notion_database = None
        self.notion_client = None #stores integration ID which can be used to authenticate with notion and the integration
        self.drive_auth = None  # Initialize to avoid AttributeError
        self.credentials_path = 'credentials.json'
        self.token_drive_path = "token_drive.pickle"
        self.drive_scopes = ['https://www.googleapis.com/auth/drive.file']

    def login_notion(self, notion_token, notion_database):
        """
        Authenticate with Notion and return Notion Client instance
        """
        self.notion_token = notion_token
        self.notion_database = notion_database

        if not self.notion_token or not self.notion_database:
            print("Notion token or Database ID is missing.") #prints this if the user does not have a notion token or a database id
            return None

        self.notion_client = Client(auth=self.notion_token) #creats a client instance using the token(integrated ID)
        print("Notion login successful")
        return self.notion_client #returns client instance to show that the authentication to notion was sucessful

    def login_drive(self):
        """
        Authenticate Google Drive and return Drive service object
        """
        creds = None #stores authentication session to make API calls to google drive
#the credential json file is important as it stores the redirect URI where the user goes as well as the scopes and client ID
        if not os.path.exists(self.credentials_path):
            print("Missing credentials.json file.") #prints this if there is no credential file that stores client information that recongizes the request to access drive
            return None

        # Load token if available
        if os.path.exists(self.token_drive_path):
            with open(self.token_drive_path, 'rb') as token_file:
                creds = pickle.load(token_file) #deserialized the token from the binary file and shows the information from that python object(prevents repeated Oauth20)

        # Refresh or generate new token
        if not creds or not creds.valid:
            try:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request()) #refreshes token if the activity on drive is expired
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path,#stores client ID and secret/scoeps
                        self.drive_scopes #creates a flow instance once the user has provided consent based on the scopes(allows for an oAuth20 process to happen once the user accepts consent for the app(python script))
                    )
                    creds = flow.run_local_server(port=8080) #opens consent screen with a broswer window for the user to login and accept consent and says the app wants to permission to view and edit files
            except Exception as e:
                print(f"Google Drive authentication failed: {e}")
                return None

            # Save token for future use
            with open(self.token_drive_path, 'wb') as token_file:
                pickle.dump(creds, token_file)#used to retrieve token for future use and saves everything into token_file from cred(python object) as a binary file and saves login session so we don't have to instantiate a flow object every time

        #we need drive_auth to access drive API and perform operations which in this case is uploading files
        self.drive_auth = build('drive', 'v3', credentials=creds) #Builds a drive service authentication connection via the drive API and version 3 with the credential object(cred with the token), atp, googl drive is authenticated from python
        print("Google Drive login successful") 
        return self.drive_auth

    def get_drive_auth(self):
        return self.drive_auth

    def get_notion_client(self):
        return self.notion_client

    def get_database_id(self):
        return self.notion_database


