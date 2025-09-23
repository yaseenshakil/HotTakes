from datetime import datetime, timezone

from db import get_db_cursor

# TODO: make function to check if user exists
# TODO: make function to check if take exists
# TODO: catch Integrity Errors
#   - user id not found
#   - tag id not found in tag table (insert or update)

def take_query(limit, offset, search_query=None):
    """
    Queries database for takes given a search query and query limit and offset

    Args:
        limit (int): number of takes to retrieve
        offset (int): number of takes to offset by
        search_query (str): title search query

    Returns:
        takes: Return list of takes in query

        Takes returned from query are the `offset+1`th take to the `offset+limit+1`th takes
    """

    # Query takes
    data = ()
    if search_query:
        sqlQuery = f"SELECT * FROM takes WHERE title LIKE '%' || %s || '%' LIMIT {limit} OFFSET {offset};"
        data = (search_query,)
    else:
        sqlQuery = f"SELECT * FROM takes LIMIT {limit} OFFSET {offset};"

    print(sqlQuery)

    # TODO: catch Integrity
    takes = []

    return takes

def take_insert(userId, title, tag, description=None):
    """
    Inserts a new take into the database

    Args:
        userId (str): User UUID
        title (str): Title of new take
        tag (str): Tag given to new take
        description (str, optional): Description for new take

    Returns:
        take: Return new take
    """

    # Insert take
    sqlQuery = f"INSERT * INTO takes VALUES (user_id=%s, title=%s, description=%s, tag=%s);"
    data = (userId, title, tag, description,)
    print(sqlQuery)

    return {}

def take_select(userId, takeId):
    """
    Retrieves a take with a given ID from database

    Args:
        userId (str): User UUID
        takeId (str): Take UUID

    Returns:
        take: If exists, return take
        None: Else, return None
    """

    # Select take
    sqlQuery = f"SELECT * FROM takes WHERE user_id=%s AND take_id=%s;"
    data = (userId, takeId,)
    print(sqlQuery)

    take = {}

    return take

def take_update(userId, takeId, title=None, tag=None, description=None):
    """
    Updates a take with a given ID in database

    Args:
        userId (str): User UUID
        takeId (str): Take UUID
        title (str, optional): New title
        tag (str, optional): New tag
        description (str, optional): New description

    Returns:
        take: If exists and changes are made, return updated take
        None: else, return None
    """

    updatedOn = datetime.now(timezone.utc).astimezone()
    print(updatedOn)

    if not title and not tag and not description:
        return None

    # Update take
    sqlQuery = f"UPDATE takes SET updated_on=%s,"
    data = (updatedOn,)
    if title:
        sqlQuery += " title=%s"
        data += (title,)
    if tag:
        sqlQuery += " tag=%s"
        data += (tag,)
    if description:
        sqlQuery += " description=%s"
        data += (description,)
    sqlQuery += " WHERE user_id=%s AND take_id=%s;"
    data += (userId, takeId,)
    print(sqlQuery)

    take = {}

    return take

def take_delete(userId, takeId):
    """
    Removes a take from the database

    Args:
        userId (str): User UUID
        takeId (str): Take UUID

    Returns:
        boolean: `True` on success; `False` on failure
        None: If take does not exist
    """

    sqlQuery = f"DELETE FROM takes WHERE user_id=%s AND take_id=%s"
    data = (userId, takeId,)
    print(sqlQuery)

    return True

def take_comment_query(takeId):
    return []

def take_comment_insert(userId, takeId, comment=None):
    pass

def take_comment_update(userId, takeId, commentId, comment=None):
    pass

def take_comment_delete(userId, takeId, commentId):
    pass
