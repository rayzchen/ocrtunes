def create_account(db, name, dob):
    # Insert new record
    db.execute("INSERT INTO users VALUES(NULL, ?, ?, 'None', 'None', '')", [name, dob])
    db.commit()
    return login_account(db, name)


def login_account(db, name):
    # Get first selection
    result = db.execute("SELECT id FROM users WHERE name=?", [name]).fetchone()
    if result is None:
        return None
    return result[0]


def get_name(db, user):
    # Select by id
    result = db.execute("SELECT name FROM users WHERE id=?", [user]).fetchone()
    if result is None:
        return None
    return result[0]


def get_fav_artist(db, user):
    # Select by id
    result = db.execute("SELECT fav_artist FROM users WHERE id=?", [user]).fetchone()
    return result[0]


def set_fav_artist(db, user, artist):
    # Select by id
    db.execute("UPDATE users SET fav_artist=? WHERE id=?", [artist, user])
    db.commit()


def get_fav_genre(db, user):
    # Select by id
    result = db.execute("SELECT fav_genre FROM users WHERE id=?", [user]).fetchone()
    return result[0]


def set_fav_genre(db, user, genre):
    # Select by id
    db.execute("UPDATE users SET fav_genre=? WHERE id=?", [genre, user])
    db.commit()
