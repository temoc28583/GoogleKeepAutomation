
from authenticate import AuthHandle
from Notefetch import Notefetch
from Tag import Tag
from Convert import Convert
from Drive import Drive

# Step 1: Authenticate to Google Keep
TestAuth = AuthHandle()
test_user = input("Enter your Google email: ")
test_pass = input("Enter your app password: ")

if not TestAuth.login_gkeep(test_user, test_pass):
    print("Authentication failed, exiting.")
    exit()

keep_notes = TestAuth.get_keep_auth()

# Step 2: Fetch notes from Keep
notes_fetcher = Notefetch(keep_auth=keep_notes)
fetched_notes = notes_fetcher.get_notes()

# Step 3: Tag notes using Claude and 16 digit App password
claude_key = "your_claude_api_key_here"
tagger = Tag(api_key=claude_key,email=test_user,password=test_pass)


results = tagger.consolidate_tags(fetched_notes)

# Step 4: Print tagged notes
for item in results:
    tags = item.get("Tags", [])
    note_text_key = next(k for k in item if k != "Tags")
    note_text = item[note_text_key]

    print("\nNote:\n", note_text)
    print("Tags:\n", tags)

# Step 5: Convert results to markdown (assuming Convert is defined)
markedText = Convert(results)
markedText.markNotes()

# Step 6: Upload tagged notes in JSON to Google Drive Folder
drive = Drive(results)
drive.to_json()
drive.login_drive()
drive.upload_drive()
