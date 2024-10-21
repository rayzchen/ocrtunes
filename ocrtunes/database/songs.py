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


def get_all_songs(db):
    result = db.execute("SELECT id, title, artist, length FROM songs ORDER BY title").fetchall()
    return result


def get_song_info(db, song):
    # Fetch by id
    result = db.execute("SELECT title, artist, genre, length FROM songs WHERE id = ?", [song]).fetchone()
    return result


def get_artist_count(db, artist):
    # Count number of rows
    result = db.execute("SELECT COUNT(artist) FROM songs WHERE artist = ?", [artist]).fetchone()
    if result is None:
        return 0
    return result[0]


def get_genre_count(db, genre):
    # Count number of rows
    result = db.execute("SELECT COUNT(genre) FROM songs WHERE genre = ?", [genre]).fetchone()
    if result is None:
        return 0
    return result[0]