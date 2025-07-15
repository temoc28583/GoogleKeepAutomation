import gkeepapi

class Notefetch():
    def __init__(self,keep_auth= None):
        self.keep_auth = keep_auth



# Notefetch.py will not use the login function to try to log the user in and provide validation as this is already done in the authentication class.

    def get_notes(self):
        if self.keep_auth is None:
            print("No session found")
            return None
        return self.keep_auth.all() #returns all the notes from google keep when the user authentication to google keep is sucessful
       
    
    
    
        