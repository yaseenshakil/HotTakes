from flask import Flask, render_template, jsonify, request, session;
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as google_oauth_requests
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

load_dotenv()
google_client_id = os.environ.get('GOOGLE_CLIENT_ID')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hottakes_users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

takes = [
    {
        "title": "Hotdogs are a taco", 
        "author": "yaseenshakil"
    }, 
    {
        "title": "Golf isn't a real sport", 
        "author": "the anti golf association"
    }, 
    {
        "title": "Friends is highly overrated",
        "author": "everyone"
    },
    {
        "title": "Crunchy peanut butter over creamy peanut butter",
        "author": "reception lady"
    }
]

@app.route('/')
def home_page():
    return render_template("index.html", takes=takes)

@app.route('/signup')
def signup():
    return render_template("signup.html", GOOGLE_CLIENT_ID=google_client_id) # its fine to send the id to the front end. its just a public identifier for your app to use google auth

@app.route('/auth/google', methods=['POST'])
def google_auth():
    # print("Google auth endpoint hit: /auth/google")

    data = request.get_json()
    # print(f"data: {data}")
    
    if not data or data["token"] == None:
        return jsonify({"success": False, "message": "No token provided"}), 400
    
    token = data['token']

    try:
        # gotten from https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.id_token.html#module-google.oauth2.id_token
        print("Verifying token...")
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_oauth_requests.Request(), 
            google_client_id
        )
        print(f"idinfo: {idinfo}")

        user_google_id = idinfo.get('sub', '')
        email = idinfo.get('email', '')
        name = idinfo.get('name', '')
        
        # TODO: Check if user exists in database and decide signup or login
        # returning account info from DB upon successful auth
        return jsonify({
            "success": True, 
            "message": "Authentication successful",
            "user": {
                "id": user_google_id,
                "email": email,
                "name": name
            }
        })
        
    except ValueError as e:
        print(f"Error verifying token: {e}")
        return jsonify({"success": False, "message": f"auth failed"}), 401

@app.after_request
def add_security_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    return response

app.static_folder = "static"

if __name__ == "__main__":
    app.run(debug=True)