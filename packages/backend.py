from packages import app
from flask import request, g, jsonify
from flask_cors import cross_origin
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
import os
import sqlite3
from dateutil import parser
import random
import time

DATABASE_DIR = 'databases/'
DATABASE_NAME = 'app.db'
DATABASE_SCHEMA = 'app.sql'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("packages", "")


def get_db() -> sqlite3.Connection:
    """
    Retrieves the SQLite database connection.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Raises:
        sqlite3.Error: If there is an issue connecting to the database.

    Usage:
        Use this function to obtain a connection to the SQLite database for executing queries.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(
            f'{ROOT_DIR}{DATABASE_DIR}{DATABASE_NAME}')
    return db


def get_cursor() -> sqlite3.Cursor:
    """
    Retrieves a cursor object connected to the database.

    Returns:
        sqlite3.Cursor: A cursor object linked to the database.

    Raises:
        RuntimeError: If the application context is not available.
        sqlite3.Error: If there is an issue connecting to the database or creating a cursor.

    Usage:
        Use this function to obtain a cursor for executing SQL queries on the database.
    """
    return get_db().cursor()


def init_db():
    """
    Initializes the database by running the SQL schema script if the database is empty or if changes were made to ksiazki.sql.

    Note:
        This function should be run only when necessary, such as when the database is empty or when changes have been made to the database schema.

    Raises:
        RuntimeError: If the application context is not available.
        sqlite3.Error: If there is an issue executing the SQL script or committing the changes to the database.

    Usage:
        Call this function to ensure the database is set up with the latest schema.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource(f'{ROOT_DIR}{DATABASE_DIR}{DATABASE_SCHEMA}', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
@cross_origin()
def index():
    return 'test'



@app.teardown_appcontext
def close_connection(exception):
    """
    Closes the database connection when the application context is torn down.

    Args:
        exception (Exception): An exception that might have occurred during the application context tear down.

    Usage:
        This function is automatically called by Flask when the application context is torn down.
        It ensures that the database connection is properly closed to prevent resource leaks.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
