from flask import Flask, render_template, jsonify, request, session, redirect, url_for;
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import json
from os import environ as env
import os


app = Flask(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

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
    return render_template("index.html", takes=takes, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/signup')
def signup():
    return render_template("signup.html") # its fine to send the id to the front end. its just a public identifier for your app to use google auth

# docs at https://manage.auth0.com/dashboard/us/dev-85r5qhl2gueunsj4/applications/ktRpbCI56rJ6ohiAHHwvf33riy9u0w65/quickstart/webapp/python
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# @app.after_request
# def add_security_headers(response):
#     response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
#     return response

app.static_folder = "static"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)
