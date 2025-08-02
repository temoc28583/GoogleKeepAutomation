Overview
GoogleKeepAutomation is a Python-based project designed to streamline note management by connecting Google Keep, Notion, and Google Drive.
The system allows users to:

Fetch notes from a Notion database

Automatically categorize and tag them using AI

Convert the notes into markdown format

Upload the processed notes to Google Drive

The project leverages Object-Oriented Programming (OOP) principles to maintain clean modularity, enabling reusable authentication sessions and a scalable workflow.

The project consists of:

5 core Python classes (in separate modules) for handling authentication, note fetching, tagging, markdown conversion, and Google Drive uploads

A  Flask backend for processing authentication requests from a simple HTML interface

Key Components
1. Authentication (authenticate.py)
Authenticates with Notion using an Integration Token and Database ID.

Authenticates with Google Drive using OAuth credentials (credentials.json).

Stores and reuses authentication sessions (service objects) to prevent repeated logins.

This is critical for Drive.py, which relies on the Drive service object to upload files efficiently.
2. Notefetching(Notefetch.py)
Key Components
Retrieves both the note properties and block content:

Headers

Bullet points

Rich text content

Returns notes in a structured dictionary format for further processing.

3.Tagging(Tag.py)
Categorizes notes into predefined tags using Anthropic Claude API.

Workflow:

Prepare prompts using est_prompt

Process notes via claude_process

Attach tags to each note

Final format:{
"title":
    {
      "content":,
      "tags": [tag1,tag2]  
    }
}
Utilizes string operations like split() for parsing and formatting note content.

4.Converts the tagged notes dictionary into Markdown format.
Markdown.py
Ensures exported files are neatly formatted with headings while preserving the dictionary format

5. Drive.py
Handles uploading of markdown files to a specified Google Drive folder.
Retrieves folder information and uploads files to the authenticated account using the reusable Drive service object.

Frontend- interface.html
 interface for user authentication.
Backend- app.py
Uses a POST form to send credentials:

A Flask application that:

Processes POST requests from interface.html

Triggers authentication and note processing workflows

Returns success/failure responses for uploads
Security featured
credentials.json and .pkl files are excluded from version control to protect sensitive tokens and session data.

OAuth tokens are securely stored for session reuse.
Object Orientated Program and reusablity
Each functionality (Auth, Fetching, Tagging, Markdown Conversion, Drive Upload) is encapsulated in a dedicated class.

Authentication objects are shared across classes to prevent redundant logins.
