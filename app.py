from flask import Flask, request,render_template #Use this to return a rendered html file via flask
#request from flask is an object that contains data from either get or post methods
from authenticate import AuthHandle
app= Flask(__name__)
@app.route('/')
def index():
    return render_template('interface.html') #returns the content of what is in interface



@app.route('/login', methods= "POST")

def login():
    email=request.form['email']
    password=request.form['password'] #way to access form information in the form of a dictionary when the user enters their username and password via a post request
    
    Auth= AuthHandle()
    Auth.login_gkeep(email,password)
    return "Connected to Google Keep"


if __name__ == '__main__ ':
    app.run(debug=True) #call dev server to make sure the script
        