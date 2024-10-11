import sqlite3
import os

def initialise_db():
    # Check if datbase file exists
    if os.path.isfile("ocrtunes.db"):
        # Load database file
        db = sqlite3.connect("ocrtunes.db")
        return db
    else:
        # Database file not found, generating via schema
        db = sqlite3.connect("ocrtunes.db")
        with open("schema.sql") as f:
            db.executescript(f.read())
        return db
