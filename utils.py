from db import get_db_cursor

def psycopg2_res_to_dict(res):
    """
    Converts psycopg2 row list into formatted dict

    Args:
        res (list): list of postgres db row columns

    Returns:
        dict: dictionary/object of take elements
    """

    return {
        "take_id": res[0],
        "title": res[1],
        "new_title": res[2],
        "tag": res[3],
        "description": res[4],
        "author": res[5],
        "created_on": res[6],
        "updated_on": res[7],
    }

def check_db_for_user(user_id):
    """
    Queries database for the existance of a user with a given UUID

    Args:
        user_id (str): user UUID

    Returns:
        boolean: `True` if user exists, `False` if user does not exist

    Raises:
        RuntimeError: if database returns more than 1 user
    """

    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM hot_takes.users WHERE user_id=%s", (user_id,))

        if cursor.rowcount == 0:
            return False

    return True

def check_db_for_take(take_id):
    """
    Queries database for the existance of a take with a given UUID

    Args:
        take_id (str): take UUID

    Returns:
        boolean: `True` if take exists, `False` if take does not exist
    """

    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM hot_takes.takes WHERE take_id=%s", (take_id,))

        if cursor.rowcount == 0:
            return False

    return True

def check_db_for_user_match(user_id, take_id):
    """
    Queries database to see if the take was created by the user

    Args:
        user_id (str): user UUID
        take_id (str): take UUID

    Returns:
        boolean: `True` if user owns the take, `False` if user does not own take
    """

    with get_db_cursor() as cursor:
        cursor.execute("SELECT author_id FROM hot_takes.takes WHERE take_id=%s", (take_id,))

        row = cursor.fetchone()

    if row[0] != user_id:
        return False

    return True

def convert_dict_keys_to_camelCase(dictionary):
    """
    Converts all keys of a Python dict from snake_case to camelCase

    Args:
        dict (dict): Python dictionary with keys in snake_case

    Returns:
        dict: input dictionary with keys in camelCase
    """

    ret = {}
    for val in dictionary:
        ret[snake_to_camelCase(val)] = dictionary.get(val)

    return ret

def snake_to_camelCase(string):
    """
    Converts a snake_case string into a camelCase string

    Args:
        string (str): string in snake_case
    """
    tokens = string.split('_')
    out = tokens[0]
    for tok in tokens[1:]:
        out += tok.capitalize()

    return out
