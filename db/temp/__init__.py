from datetime import datetime, timezone

from db import get_db_cursor

from utils import psycopg2_res_to_dict

TAKE_RETURN = "take_id, title, newtitle, label AS tag, description, username as author, created_on, updated_on"
"""
Columns to return in SQL

Take Return Format:
{
    take_id: string,
    title: string,
    new_title: string | undefined,
    tag: string,
    description: string,
    author: string,
    created_on: date,
    updated_on: date,
}
"""

def take_query(limit, offset, search_query=None):
    """
    Queries database for takes given a search query and query limit and offset

    Args:
        limit (int): number of takes to retrieve
        offset (int): number of takes to offset by
        search_query (str): title search query

    Returns:
        list: A list containing dictionaries of the take

        Takes returned from query are the `offset+1`th take to the `offset+limit+1`th takes
    """

    # Query takes
    if search_query:
        sqlQuery = (f"SELECT {TAKE_RETURN} "
                    "FROM hot_takes.takes "
                    "JOIN hot_takes.tags USING (tag_id) "
                    "JOIN hot_takes.user_accounts ON author_id=user_id "
                    "WHERE title ILIKE %s"
                    "ORDER BY created_on DESC "
                    f"LIMIT {limit} OFFSET {offset};")
        data = (f"%{search_query}%",)
    else:
        sqlQuery = (f"SELECT {TAKE_RETURN} "
                    "FROM hot_takes.takes "
                    "JOIN hot_takes.tags USING (tag_id) "
                    "JOIN hot_takes.user_accounts ON author_id=user_id "
                    "ORDER BY created_on DESC "
                    f"LIMIT {limit} OFFSET {offset};")
        data = ()

    with get_db_cursor() as cursor:
        cursor.execute(sqlQuery, data)
        rows = cursor.fetchall()

    return list(map(psycopg2_res_to_dict, rows))

def take_insert(user_id, title, tag_id, description=None):
    """
    Inserts a new take into the database

    Args:
        user_id (str): User UUID
        title (str): Title of new take
        tag_id (str): Tag ID
        description (str, optional): Description for new take

    Returns:
        dict: created take
    """

    # Insert take
    sqlQuery = ("INSERT INTO hot_takes.takes (author_id, title, tag_id, description) "
                "VALUES (%s, %s, %s, %s) "
                "RETURNING take_id;")
    data = (user_id, title, tag_id, description,)

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sqlQuery, data)
        row = cursor.fetchone()

    # Get created take
    take = take_select(row[0])

    return take

def take_select(take_id):
    """
    Retrieves a take with a given ID from database

    Args:
        take_id (str): Take UUID

    Returns:
        dict: retrieved take
    """

    # Select take
    sqlQuery = (f"SELECT {TAKE_RETURN} "
                "FROM hot_takes.takes "
                "JOIN hot_takes.tags USING (tag_id) "
                "JOIN hot_takes.user_accounts ON author_id=user_id "
                "WHERE take_id=%s;")
    data = (take_id,)

    with get_db_cursor() as cursor:
        cursor.execute(sqlQuery, data)
        row = cursor.fetchone()

    return psycopg2_res_to_dict(row)

def take_update(user_id, take_id, title=None, tag_id=None, description=None):
    """
    Updates a take with a given ID in database

    Args:
        user_id (str): User UUID
        take_id (str): Take UUID
        title (str, optional): New title
        tag_id (str, optional): Tag ID
        description (str, optional): New description

    Returns:
        dict: updated take

    """

    # Update take
    sqlQuery = "UPDATE hot_takes.takes SET updated_on=%s,"
    data = (datetime.now(timezone.utc).astimezone(),)
    updated = False
    if title:
        sqlQuery += " title=%s"
        data += (title,)
        updated = True
    if tag_id:
        if updated: sqlQuery += ","

        sqlQuery += " tag_id=%s"
        data += (tag_id,)
        updated = True

    if description:
        if updated: sqlQuery += ","

        sqlQuery += " description=%s"
        data += (description,)
    sqlQuery += " WHERE author_id=%s AND take_id=%s;"
    data += (user_id, take_id,)

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sqlQuery, data)

    # Get updated take
    take = take_select(take_id)

    return take

def take_delete(user_id, take_id):
    """
    Removes a take from the database

    Args:
        user_id (str): User UUID
        take_id (str): Take UUID

    Returns:
        bool: take deletion success

        `True` on success, `False` on failure

    Raise:
        RuntimeError: If database deletes more than 1 value; this also rollsback any changes
    """

    sqlQuery = ("DELETE FROM hot_takes.takes "
                "WHERE author_id=%s AND take_id=%s;")
    data = (user_id, take_id,)

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sqlQuery, data)

        if cursor.rowcount > 1:
            raise RuntimeError("Database deleted more 1 value")

        if cursor.rowcount == 0:
            return False

    return True

def take_comment_query(take_id):
    return []

def take_comment_insert(user_id, take_id, comment=None):
    pass

def take_comment_update(user_id, take_id, comment_id, comment=None):
    pass

def take_comment_delete(user_id, take_id, comment_id):
    pass
