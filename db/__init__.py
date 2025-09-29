__all__ = ["temp"]

import os
from contextlib import contextmanager

from flask import current_app, g

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool

    URL = os.environ['DATABASE_URL']

    current_app.logger.info(f"Creating DB connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=URL, sslmode='require')

@contextmanager
def get_db_conn():
    try:
        conn = pool.getconn()
        yield conn
    finally:
        pool.putconn(conn)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_conn() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)

        try:
            yield cursor
            if commit:
                conn.commit()
        finally:
            cursor.close()
