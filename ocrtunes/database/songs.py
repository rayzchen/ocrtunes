def get_genres(db):
    # Select unique values
    result = db.execute("SELECT DISTINCT genre FROM songs").fetchall()
    if result is None:
        return None
    return [row[0] for row in result]


def get_average_length(db, genre):
    # Get average of row
    result = db.execute("SELECT AVG(length) FROM songs WHERE genre=?", [genre]).fetchone()
    if result is None:
        return None
    return round(result[0])
