# GoogleKeepAutomation
Utilized Google Keep APIs to extract notes utilizing authorization

One html file to keep track of the front-end interface
will keep track of Google Drive and Google Keep credentials

*credentials.json and pkl are not avaliable to safeguard personal information
Notes from Google keep are not saved to drive for the purpose of utilizing them in python
OOP aspect

Plan to utilize 5 classes total
authenticate.py
handles user credentials to google keep and drive by using authenicate and store the session in an object to avoid relogging in
*goal is to reuse the same keep session object across classes to ensure that authentication and uploading notes to drive do not require different sessions
Notefetch.py
retrieve notes to process for tagging (this includes taking the notes from keep)
use all() from the authenication object established in authenticate.py
keep_notes = TestAuth.get_keep_auth() this is the authentication object which will be used to get the notes from google keep
notes = Notefetch()
notes.keep_auth = keep_notes
fetched_notes = notes.get_notes()
Tag.py
tags the notes on an AI platform(use an API) for predefined sets
use the cateogories list with with the predefined tags
Use antrophic api to connect the prompts in the est_prompt and claude_process function to give approriate tags based on the content of the notes
use split() to format the notes
Note.py
Markdown.py
Convert the notes and tags into markdown format by using the markdown library

Drive.py
utiilize Google Drive API and and MediaFileUpload library to obtain information about the folder in google drive along with the converted tagged  notes to send the notes to google drive



interface.html
stores the backend form request to make sure the user is authenticated use form method= "POST"
Name will serve as data send to the backend request.form['email'] 
app.py
Flask file that will process the HTML Post Request

