from authenticate import AuthHandle
from Notefetch import Notefetch
from Tag import Tag
from Convert import Convert
from Drive import Drive
import os
import sys
from dotenv import load_dotenv

# Define categories for tagging
categories = [
    'SEO', 'ads', 'marketing', 'technology',
    'Product management', 'business management',
    'Networking', 'business strategy'
]

# Step 0: Load environment variables from 'claude.env'
load_dotenv(dotenv_path="claude.env")
claude_key = os.getenv("CLAUDE_API_KEY")
folder_id = os.getenv("FOLDER_ID")
Notion_token = os.getenv("NOTION_TOKEN")
Database_ID = os.getenv("DATABASE_ID")

# Step 1: Validate environment variables
if not claude_key:
    print("Claude API key not set.")
    sys.exit(1)
if not Notion_token:
    print("NOTION_TOKEN not found in env file")
if not Database_ID:
    print("DATABASE_ID not found env file")
# Step 2: Check for existing Google Keep token file
    """if not os.path.exists("token_keep.pickle"):
    print("Google Keep token file not found.")
    sys.exit(1)

    """

# Step 3: Authenticate with Notion
auth_handler = AuthHandle()
notion_client = auth_handler.login_notion(Notion_token, Database_ID)

if not notion_client:
    print("Notion authentication failed.")
    sys.exit(1)

# Step 4: Fetch notes from Notion database
notes_fetcher = Notefetch(notion_client, Database_ID)
all_notes = notes_fetcher.get_all_notes()
if not all_notes:
    print("No notes found with the specified titles.")
    sys.exit(1)


# Optional: Print retrieved note titles for debugging
print("Retrieved notes:")
for title in all_notes.keys():
    print(f"• {title}")

# Step 5: Tag notes using Claude API
tagger = Tag(api_key=claude_key, notion_obj=notion_client, categories=categories)
results = tagger.consolidate_tags(all_notes)

# Step 6: Print tagging results
for tag, items in results.items():
    print(f"\nTag: {tag}")
    for title, note in items:
        print(f"• Title: {title}")
        print(f"  Note: {note}\n")

# Step 7: Restructure tagged notes into dictionary format for conversion
restructured_notes = {}
for tag, items in results.items():
    for title, note in items:
        if title not in restructured_notes:
            restructured_notes[title] = {"tags": [], "Content": note}
        if tag not in restructured_notes[title]["tags"]:
            restructured_notes[title]["tags"].append(tag)

# Step 8: Convert notes to Markdown format
converter = Convert(restructured_notes)
markdown_output = converter.markNotes()

# Step 9: Print Markdown output for each note
print("\nMarkdown Output:\n")
for title, md in markdown_output.items():
    print(f"---\n{md}")

# Step 10: Authenticate Google Drive and upload Markdown file
print("Authenticating Google Drive...")
drive_auth = auth_handler.login_drive()
if not drive_auth:
    print("Drive authentication failed. Cannot upload.")
    sys.exit(1)

drive = Drive(tagged_notes=markdown_output, service=drive_auth, file_name="Tagged.md")
file_id = drive.save_and_upload()

print(f"\n✅ Upload successful! View your file here:\nhttps://drive.google.com/file/d/{file_id}\n")



    
    




