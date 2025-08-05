from authenticate import AuthHandle
from Notefetch import Notefetch
from Tag import Tag
from Convert import Convert
from Drive import Drive
import os
import sys
from dotenv import load_dotenv

# Step 0: Load environment variables from 'claude.env'
load_dotenv(dotenv_path="claude.env")

claude_key = os.getenv("CLAUDE_API_KEY")
folder_id = os.getenv("FOLDER_ID")
Notion_token = os.getenv("NOTION_TOKEN")
Database_ID = os.getenv("DATABASE_ID")

if not Notion_token:
    print("NOTION_TOKEN not found in env file")
    sys.exit(1)

if not Database_ID:
    print("DATABASE_ID not found in env file")
    sys.exit(1)

if not claude_key:
    print("Claude API key not found in env file")
    sys.exit(1)

# Categories and their synonyms for fallback matching
categories_synonyms = {
    'SEO': ['seo', 'search engine optimization', 'keywords', 'backlinks'],
    'Ads': ['ads', 'advertisement', 'ad campaign', 'paid search'],
    'Marketing': ['marketing', 'promotion', 'brand', 'campaign'],
    'Technology': ['technology', 'tech', 'software', 'hardware'],
    'Product Management': ['product management', 'product manager', 'roadmap', 'mvp'],
    'Project Management': ['project management', 'project manager', 'team management', 'leadership', 'mentoring'],
    'Business Management': ['business management', 'operations', 'strategy', 'finance'],
    'Networking': ['networking', 'connections', 'contacts', 'social network'],
    'Business Strategy': ['business strategy', 'planning', 'growth', 'market positioning']
}

# Step 1: Authenticate with Notion
auth_handler = AuthHandle()
notion_client = auth_handler.login_notion(Notion_token, Database_ID)
if not notion_client:
    print("Notion authentication failed.")
    sys.exit(1)

# Step 2: Initialize Notefetch
notefetcher = Notefetch(notion_client, Database_ID)

# Step 3: Unarchive all archived notes before fetching
print("Checking for archived notes to unarchive...")
all_pages = notefetcher.get_all_pages_in_database()
archived_pages = [page for page in all_pages if page.get("archived", False)]

if archived_pages:
    print(f"Found {len(archived_pages)} archived notes, unarchiving them...")
    for page in archived_pages:
        notefetcher.unarchive_note(page["id"])
else:
    print("No archived notes found.")

# Step 4: Initialize Tag with Claude API key & synonyms
tagger = Tag(api_key=claude_key, notion_obj=notefetcher, categories_synonyms=categories_synonyms)

# Step 5: Fetch notes from Notion database (unarchived now included)
all_notes = tagger.fetch_notes(notes_amount=None)
if not all_notes:
    print("No notes found in Notion.")
    sys.exit(1)

print("Retrieved notes:")
for title in all_notes.keys():
    print(f"• {title}")

# Step 6: Tagging notes with Claude + synonyms fallback
results = tagger.consolidate_tags(all_notes)

# Step 7: Print tagging results
for tag, items in results.items():
    print(f"\nTag: {tag}")
    for title, note in items:
        print(f"• Title: {title}")
        print(f"  Note: {note}\n")

# Step 8: Restructure notes for Markdown conversion
restructured_notes = {}
for tag, items in results.items():
    for title, note in items:
        if title not in restructured_notes:
            restructured_notes[title] = {"tags": [], "Content": note}
        if tag not in restructured_notes[title]["tags"]:
            restructured_notes[title]["tags"].append(tag)

# Step 9: Convert notes to Markdown format
converter = Convert(restructured_notes)
markdown_output = converter.markNotes()

print("\nMarkdown Output:\n")
for title, md in markdown_output.items():
    print(f"---\n{md}")

# Step 10: Authenticate Google Drive and upload Markdown files
print("Authenticating Google Drive...")
drive_auth = auth_handler.login_drive()
if not drive_auth:
    print("Drive authentication failed. Cannot upload.")
    sys.exit(1)

drive = Drive(tagged_notes=markdown_output, service=drive_auth, folder_id=folder_id)

print("\nUploading individual notes to Google Drive...")
individual_uploads = drive.save_and_upload_individual_notes()

if not individual_uploads:
    print("❌ No files were uploaded to Google Drive.")
else:
    print("\n✅ All files uploaded successfully!")
    print("Here are your Google Drive links:\n")
    for title, file_id in individual_uploads.items():
        print(f"• {title}: https://drive.google.com/file/d/{file_id}/view")

# Optional: Archiving processed notes in Notion (currently disabled)
"""
print("\nArchiving processed notes in Notion...")
for title, data in notefetcher.get_all_notes().items():
    success = notefetcher.del_notes(data["id"])
    if success:
        print(f"✓ Archived '{title}'")
    else:
        print(f"✗ Failed to archive '{title}'")
"""



# Step 13: Archive processed notes in Notion (commented out for now)
"""
print("\nArchiving processed notes in Notion...")
for title, data in notefetcher.get_all_notes().items():
    success = notefetcher.del_notes(data["id"])
    if success:
        print(f"✓ Archived '{title}'")
    else:
        print(f"✗ Failed to archive '{title}'")
"""

        




