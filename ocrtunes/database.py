import sqlite3
import os

directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database"
)
database_file = os.path.join(directory, "ocrtunes.db")
schema_file = os.path.join(directory, "schema.sql")
song_file = os.path.join(directory, "songs.sql")

def initialise_db():
    # Check if datbase file exists
    if os.path.isfile(database_file):
        # Load database file
        db = sqlite3.connect(database_file)
        return db
    else:
        # Database file not found, generating via schema
        db = sqlite3.connect(database_file)
        with open(schema_file) as f:
            db.executescript(f.read())
        with open(song_file) as f:
            db.executescript(f.read())
        return db
