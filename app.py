import os

from flask import Flask, render_template, request, send_from_directory;

from db import setup as db_setup
import db.temp as db_query

app = Flask(__name__)
app.static_folder = "static"

# with app.app_context():
#     db_setup()

USER_ID = "00000000-0000-0000-0000-000000000000"

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

@app.route("/healthcheck")
def healthcheck():
    return {

    }

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "img/favicon.ico", mimetype="image/vnd.microsoft.icon")

"""
Page Routes
"""
@app.route("/")
def home_page():
    return render_template("index.html", takes=takes)

@app.route("/signup")
def signup():
    return render_template("signup.html")


"""
API Routes

- User registration
- Take query and CRUD routes
- Take comment query and CUD routes
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

# Take Routes
@app.route("/api/takes")
def take_query():
    """
    Handle request to query takes
    """
    # NOTE: pages are 1-indexed [1, 2, ...]

    query = request.args.get("query", "")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 25, type=int)

    offset = (page - 1) * limit

    takes = db_query.take_query(limit=limit, offset=offset, search_query=query)

    return {
        "count": len(takes),
        "data": takes,
    }

@app.route("/api/takes/create", methods=["POST"])
def take_create():
    """
    Handle request to create a new take

    Body Format::

        {
            title: string,
            tags: string,
            description: string | null,
        }
    """

    body = dict(request.get_json())
    print(body)

    take = db_query.take_insert(USER_ID, title=body.get("title"), tag=body.get("tags"), description=body.get("description"))

    return take

@app.route("/api/takes/<uuid:takeId>")
def take_retrieve(takeId):
    """
    Handle request to retrieve a take
    """

    # TODO

    take = db_query.take_select(USER_ID, takeId)

    return take

@app.route("/api/takes/<uuid:takeId>", methods=["PATCH"])
def take_update(takeId):
    """
    Handle request to update take
    """

    # TODO

    body = dict(request.get_json())
    print(body)

    take = db_query.take_update(USER_ID, takeId, title=body.get("title"), tag=body.get("tag"), description=body.get("description"))

    return take

@app.route("/api/takes/<uuid:takeId>", methods=["DELETE"])
def take_delete(takeId):
    """
    Handle request to delete take
    """

    # TODO

    succ = db_query.take_delete(USER_ID, takeId)
    if succ:
        return "", 204
    else:
        return "", 400

# Take Comment Routes
@app.route("/api/takes/<uuid:takeId>/comments")
def take_comment_query(takeId):
    # TODO
    # NOTE: default to newest to oldest, but allow filtering?
    pass

@app.route("/api/takes/<uuid:takeId>/comments/add")
def take_comment_create(takeId):
    # TODO
    pass

@app.route("/api/takes/<uuid:takeId>/comments/<uuid:commentId>")
def take_comment_update(takeId, commentId):
    # TODO
    pass

@app.route("/api/takes/<uuid:takeId>/comments/<uuid:commentId>")
def take_comment_delete(takeId, commentId):
    # TODO
    pass

if __name__ == "__main__":
    app.run(debug=True)
