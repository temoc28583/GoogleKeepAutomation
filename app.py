from flask import Flask, request, render_template
from authenticate import AuthHandle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')  # A simple HTML form

@app.route('/login', methods=["POST"])
def login():
    notion_token = request.form.get('Notion_Token')
    database_id = request.form.get('Database_ID')

    auth = AuthHandle()
    client = auth.login_notion(notion_token, database_id)

    if client is None:
        return "Login failed: Missing Notion token or Database ID", 400

    return "Login successful!"









