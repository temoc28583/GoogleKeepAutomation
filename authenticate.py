import gkeepapi
import os
import pickle  # For storing token
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials



import gkeepapi

class AuthHandle:
    def __init__(self):
        self.keep_auth = None  # stores gkeepapi.Keep() object
        self.drive_auth = None  # optionally for future Drive support
        self.credential_path= "credentials.json" #python script use this for the flow and starting a login session when a oAuth client ID is made
        self.drive_token= "token.pickle"#allows the session to resume
        self.scope='https://www.googleapis.com/auth/drive.file' #defines the permission within drive the request can go through to

    def login_gkeep(self, user, gPassword):
        try:
            keep = gkeepapi.Keep()
            keep.authenticate(user, gPassword)
            self.keep_auth = keep
            return True  # optional success return
        except gkeepapi.exception.LoginException as e:
            print(f"Authentication with Google Keep failed: {e}")
            self.keep_auth = None
            return False
        except Exception as e:
            print("Unexpected error during authentication:", e)
            self.keep_auth = None
            return False

    def get_keep_auth(self):
        if self.keep_auth:
               return self.keep_auth
            
     

    
    
def login_drive(self):
    cred=None #stores credentials with token, refresh token
    if os.path.exists(self.drive_token):
        with open(self.drive_token, 'rb') as file: #checks if credentials exist from previous session
            cred=pickle.load(file) #loads the object in memory
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refesh_token:
            cred.refresh(Request()) #use request to get updated token if the credentials expired but exist
    else:
        flow=InstalledAppFlow.from_client_secrets_file(
         self.credential_path, self.scope) #generate flow object to run a session if the credentials are not authorized uses scope  to define permission and the credentials file from the json file
        cred=flow.run_local_server(port=0) #Open browser for the user to log in
    #save credentials from the token but this time to resume it
    with open(self.drive_token, 'wb') as f:
        pickle.dump(cred,f) #save credentials to token once the user has a  sucessful login
    self.drive_auth=build("drive","v1", credentials=cred) #creates Google drive api via the client api
    return self.drive_auth #returns client
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def get_keep_auth(self):
    return self.keep_auth

def get_drive_auth(self):
    return self.drive_auth
