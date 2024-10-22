def get_all_playlists(db, user):
    # Stored as comma separated string
    result = db.execute("SELECT playlists FROM users WHERE id = ?", [user]).fetchone()
    if not result[0]:
        return []
    return [int(id) for id in result[0].split(",")]


def get_playlist_name(db, playlist):
    # Query by id
    result = db.execute(
        "SELECT name FROM playlists WHERE id = ?", [playlist]
    ).fetchone()
    return result[0]


def get_playlist_size(db, playlist):
    result = db.execute(
        "SELECT songs FROM playlists WHERE id = ?", [playlist]
    ).fetchone()
    if not result[0]:
        return 0
    return len(result[0].split(","))


def get_playlist_length(db, playlist):
    result = db.execute(
        "SELECT songs FROM playlists WHERE id = ?", [playlist]
    ).fetchone()
    if not result[0]:
        return 0
    songs = [int(id) for id in result[0].split(",")]
    result = db.execute(
        "SELECT SUM(length) FROM songs WHERE id IN (" + result[0] + ")"
    ).fetchone()
    return result[0]


def create_playlist(db, user, name, songs=""):
    db.execute("INSERT INTO playlists VALUES(NULL, ?, ?)", [name, songs])
    result = db.execute(
        "SELECT id FROM playlists WHERE name = ? ORDER BY id DESC LIMIT 1", [name]
    ).fetchone()
    id = result[0]
    result = db.execute("SELECT playlists FROM users WHERE id = ?", [user]).fetchone()
    if result[0]:
        new_playlists = result[0] + "," + str(id)
    else:
        new_playlists = str(id)
    db.execute("UPDATE users SET playlists = ? WHERE id = ?", [new_playlists, user])
    db.commit()
    return id


def create_genre_playlist(db, user, name, genre):
    result = db.execute(
        "SELECT id FROM songs WHERE genre = ? ORDER BY RANDOM() LIMIT 5", [genre]
    ).fetchall()
    songs = ",".join(str(row[0]) for row in result)
    return create_playlist(db, user, name, songs)


def create_duration_playlist(db, user, name, duration):
    total_duration = duration * 60
    songs = []
    while True:
        result = db.execute(
            "SELECT id, length FROM songs WHERE length < ? AND id NOT IN ("
            + ",".join(songs)
            + ") ORDER BY RANDOM() LIMIT 1",
            [total_duration],
        ).fetchone()
        if result is not None:
            songs.append(str(result[0]))
            total_duration -= result[1]
        else:
            break
    songs = ",".join(songs)
    return create_playlist(db, user, name, songs)


def get_playlist_songs(db, id):
    result = db.execute("SELECT songs FROM playlists WHERE id = ?", [id]).fetchone()
    if not result[0]:
        return []
    songs = [int(id) for id in result[0].split(",")]
    result = db.execute(
        "SELECT id, title, artist, length FROM songs WHERE id IN ("
        + result[0]
        + ") ORDER BY title"
    ).fetchall()
    return result


def rename_playlist(db, id, name):
    db.execute("UPDATE playlists SET name = ? WHERE id = ?", [name, id])
    db.commit()


def delete_playlist(db, id):
    filters = [f"{id}", f"{id},%", f"%,{id},%", f"%,{id}"]
    result = db.execute(
        "SELECT id, playlists FROM users WHERE playlists = ? OR playlists LIKE ? OR playlists LIKE ? OR playlists LIKE ?",
        filters,
    ).fetchall()
    for user, playlists in result:
        playlists = playlists.split(",")
        playlists.remove(str(id))
        new_playlists = ",".join(playlists)
        db.execute("UPDATE users SET playlists = ? WHERE id = ?", [new_playlists, user])
    db.commit()


def check_song_in_playlist(db, playlist, song):
    result = db.execute(
        "SELECT songs FROM playlists WHERE id = ?", [playlist]
    ).fetchone()
    if not result[0]:
        return False
    songs = [int(id) for id in result[0].split(",")]
    return song in songs


def add_song_to_playlist(db, playlist, song):
    result = db.execute(
        "SELECT songs FROM playlists WHERE id = ?", [playlist]
    ).fetchone()
    if result[0]:
        songs = result[0].split(",")
        songs.append(str(song))
        new_songs = ",".join(songs)
    else:
        new_songs = str(song)
    db.execute("UPDATE playlists SET songs = ? WHERE id = ?", [new_songs, playlist])
    db.commit()
