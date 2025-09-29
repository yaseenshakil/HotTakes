from flask import Flask, render_template, jsonify, request, session, redirect, url_for;
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import json
from os import environ as env
import os
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask import Flask, render_template, request, send_from_directory;

from psycopg2.errors import ForeignKeyViolation

from db import setup as db_setup
import db.temp as db_query
from utils import check_db_for_take, check_db_for_user, check_db_for_user_match, convert_dict_keys_to_camelCase

# Flask app setup
app = Flask(__name__)
app.static_folder = "static"

# Setup database
with app.app_context():
    db_setup()

USER_ID = "00000000-0000-0000-0000-000000000001" # TODO: will this be a problem? each time you start your server, this will reset to 1

TAKE_COLS = ["title", "tagId", "description"]

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# to connect to auth0
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

# to connect to DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HOTTAKES_RENDER_DB_URL", "postgresql+psycopg://user:pw@localhost:5432/hottakes")
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

@app.route("/health")
def healthcheck():
    return {
        "version": "0.0.1",
        "message": "Hot Takes Web Server",
    }

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "img/favicon.ico", mimetype="image/vnd.microsoft.icon")

"""
Page Routes
"""
@app.route("/")
def home_page(): # TODO: check if user is in session, if not redirect to signup/login page
    return render_template("index.html", takes=takes, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    print(f"serving log in page")
    return render_template("login.html")

"""
API Routes

- User registration
- Take query and CRUD routes
- Take comment query and CUD routes

Take Response Format:
{
    takeId: string,
    title: string,
    newTitle: string | undefined,
    tag: string,
    description: string,
    author: string,
    createdOn: date,
    updatedOn: date,
}
"""

# User Routes
@app.route("/api/users/new-account", methods=["POST"])
def user_add_account():
    """
    Handle request to add new account user
    """

    pass

@app.route("/api/users/new-session", methods=["POST"])
def user_add_session():
    """
    Handle request to add new session user
    """

    pass

# docs at https://auth0.com/docs/quickstart/webapp/python/interactive
@app.route("/login/callback")
def login_callback():
    print("login/callback")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    print("in callback")
    try:
        token = oauth.auth0.authorize_access_token()
        print(f"token: {json.dumps(token, indent=4, default=str)}")
        session["user"] = token
        # session["signin-time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        basic_user_info = {
            "first_name" : token["userinfo"]["given_name"],
            "last_name" : token["userinfo"]["family_name"],
            "nickname" : token["userinfo"]["nickname"],
            "email" : token["userinfo"]["email"],
            "user_profile_pic" : token["userinfo"]["picture"],
            "user_id" : token["userinfo"]["sub"] # this is the only unique identifier for each google account
        } # TODO: check if this exist inside the DB

        # if check_db_for_user(basic_user_info["user_id"]) == False:
        #     return redirect("/signup") 
        
        return redirect("/")
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return redirect("/signup") # TODO: maybe check if the user exist in the db or else add new user

@app.route("/logout")
def logout():
    print("logging out")
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

# Take Routes
@app.route("/api/takes")
def take_query():
    """
    Handle request to query takes

    Query Parameters:
        query (string): search query
        page (int): page number (1-indexed)
        limit (int): number of takes to query

    Returns:
        dict: number of takes queried and list of takes with HTTP status code 200
    """

    # Get request parameters
    query = request.args.get("query", "")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 25, type=int)

    # Set query offset
    offset = (page - 1) * limit

    # Run database query
    takes = db_query.take_query(limit=limit, offset=offset, search_query=query)

    return {
        "count": len(takes),
        "data": list(map(convert_dict_keys_to_camelCase, takes)),
    }

@app.route("/api/takes", methods=["POST"])
def take_create():
    """
    Handle request to create a new take

    This API endpoint is protected and requires authorization

    Body:
        json: {
            title: string,
            tagId: number,
            description: string | null,
        }

    Returns:
        tuple: created take with status 201, or error message with error HTTP status code

        Status Codes:
        201: creation success
        400: request errors (invalid user ID, invalid tag ID, etc.)
        401: user is not authenticated (logged-out)
    """

    # Get Authorization header and user ID
    userId = request.headers.get("Authorization")
    if userId is None:
        return "Not authenticated", 401
    userId = userId.removeprefix("Bearer ")

    # Check if user exists; return unauthorized to hide whether user exists
    if not check_db_for_user(userId):
        return "User not authenticated", 401

    # Get request body and verify required values
    body = dict(request.get_json())
    bodyKeys = body.keys()
    if "title" not in bodyKeys or "tagId" not in bodyKeys:
        return "Missing values in request body", 400

    # Run database query
    try:
        take = db_query.take_insert(userId, title=body.get("title"), tag_id=body.get("tagId"), description=body.get("description"))
    except ForeignKeyViolation:
        return "Invalid tag ID", 400

    return convert_dict_keys_to_camelCase(take), 201

@app.route("/api/takes/<takeId>")
def take_retrieve(takeId):
    """
    Handle request to retrieve a take

    Args:
        takeId: take UUID

    Returns:
        take: retrieved take with response code 200

        If take is not found, return status code 404
    """

    # Check if take exists
    if not check_db_for_take(takeId):
        return "Take not found", 404

    # Run database query
    take = db_query.take_select(takeId)

    return convert_dict_keys_to_camelCase(take), 200

@app.route("/api/takes/<takeId>", methods=["PATCH"])
def take_update(takeId):
    """
    Handle request to update a take

    This API endpoint is protected and requires authorization

    Args:
        takeId: take UUID

    Body:
        json: {
            title: string | null,
            tagId: string | null,
            description | null,
        }

    Returns:
        tuple: response message and HTTP status code

        Status Codes:
        200: update success
        400: request errors (user not found, no changes requested, etc)
        401: User is not authenticated (logged-out)
        404: take not found
    """

    # Get Authorization header and user ID
    userId = request.headers.get("Authorization")
    if userId is None:
        return "Not authenticated", 401
    userId = userId.removeprefix("Bearer ")

    # Check if user exists; return unauthorized to hide whether user exists
    if not check_db_for_user(userId):
        return "User not authenticated", 401

    # Check if take exists
    if not check_db_for_take(takeId):
        return "Take not found", 404

    # Check if user has perms to update take
    if not check_db_for_user_match(userId, takeId):
        return "Not authorized", 403

    # Get request body and verify updates are requested
    body = dict(request.get_json())
    if not any(key in body.keys() for key in TAKE_COLS):
        return "No values in request body", 400

    # Run database query
    try:
        take = db_query.take_update(USER_ID, takeId, title=body.get("title"), tag_id=body.get("tagId"), description=body.get("description"))
    except ForeignKeyViolation:
        return "Invalid tag ID", 400

    return convert_dict_keys_to_camelCase(take), 200

@app.route("/api/takes/<takeId>", methods=["DELETE"])
def take_delete(takeId):
    """
    Handle request to delete take

    This API endpoint is protected and requires authorization

    Args:
        takeId (str): take UUID

    Returns:
        tuple: response message and HTTP status code

        Status Codes:
        204: if take was deleted
        404: if take was not found
        500: if take was not deleted due to server errors
    """

    # Get Authorization header and user ID
    userId = request.headers.get("Authorization")
    if userId is None:
        return "Not authenticated", 401
    userId = userId.removeprefix("Bearer ")

    # Check if user exists; return unauthorized to hide wheterh user exists
    if not check_db_for_user(userId):
        return "User not authenticated", 401

    # Check if take exists
    if not check_db_for_take(takeId):
        return "Take not found", 404

    # Check if user has perms to delete take
    if not check_db_for_user_match(userId, takeId):
        return "Not authorized", 403

    # Run database query
    res = db_query.take_delete(userId, takeId)

    if not res:
        return "Take not deleted", 500

    return "", 204

# Take Comment Routes
@app.route("/api/takes/<takeId>/comments")
def take_comment_query(takeId):
    # TODO
    # NOTE: default to newest to oldest, but allow filtering?
    pass

@app.route("/api/takes/<takeId>/comments/add")
def take_comment_create(takeId):
    # TODO
    pass

@app.route("/api/takes/<takeId>/comments/<commentId>")
def take_comment_update(takeId, commentId):
    # TODO
    pass

@app.route("/api/takes/<takeId>/comments/<commentId>")
def take_comment_delete(takeId, commentId):
    # TODO
    pass


app.static_folder = "static"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)
