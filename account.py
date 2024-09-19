def create_account(db, name, dob):
    db.execute("INSERT INTO users VALUES(NULL, ?, ?, 'None', 'None', '')", [name, dob])
    db.commit()
    return login_account(db, name)

def login_account(db, name):
    result = db.execute("SELECT id FROM users WHERE name=?", [name]).fetchone()
    if result is None:
        return None
    return result[0]

def get_name(db, user):
    result = db.execute("SELECT name FROM users WHERE id=?", [user]).fetchone()
    if result is None:
        return None
    return result[0]
