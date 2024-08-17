from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

CREATE_DB = "CREATE DATABASE IF NOT EXISTS workshop2;"

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    username varchar(255) UNIQUE NOT NULL,
    hashed_passowrd varchar(80)
    )"""

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id serial,
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    text varchar(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """

DB_USER = "postgres"
DB_PASSWORD = "coderslab"
DB_HOST = "127.0.0.1"

try:
    conn = connect (user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(CREATE_DB)
        print("DB created")
    except DuplicateDatabase as e:
        print("Database exists: %s" % e)
    conn.close()
except OperationalError as e:
    print("Connection failed: %s" % e)

try:
    conn = connect (database="workshop2", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(CREATE_USERS_TABLE)
        print("Users table created")
    except DuplicateTable as e:
        print("Table exists: %s" % e)

    try:
        cursor.execute(CREATE_MESSAGES_TABLE)
        print("Messages table created")
    except DuplicateTable as e:
        print("Table exists: %s" % e)
    conn.close()
except OperationalError as e:
    print("Connection failed: %s" % e)
