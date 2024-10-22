def get_all_playlists(db, user):
    # Stored as comma separated string
    result = db.execute("SELECT playlists FROM users WHERE id = ?", [user]).fetchone()
    if not result[0]:
        return []
    return [int(id) for id in result[0].split(",")]


def get_playlist_name(db, playlist):
    # Query by id
    result = db.execute("SELECT name FROM playlists WHERE id = ?", [playlist]).fetchone()
    return result[0]


def get_playlist_size(db, playlist):
    result = db.execute("SELECT songs FROM playlists WHERE id = ?", [playlist]).fetchone()
    if not result[0]:
        return 0
    return len(result[0].split(","))


def get_playlist_length(db, playlist):
    result = db.execute("SELECT songs FROM playlists WHERE id = ?", [playlist]).fetchone()
    if not result[0]:
        return 0
    songs = [int(id) for id in result[0].split(",")]
    result = db.execute("SELECT SUM(length) FROM songs WHERE id IN ?", [songs]).fetchone()
    return result[0]


def create_playlist(db, user, name):
    db.execute("INSERT INTO playlists VALUES(NULL, ?, '')", [name])
    result = db.execute("SELECT id FROM playlists WHERE name = ? ORDER BY id DESC LIMIT 1", [name]).fetchone()
    id = result[0]
    result = db.execute("SELECT playlists FROM users WHERE id = ?", [user]).fetchone()
    if result[0]:
        new_playlists = result[0] + "," + str(id)
    else:
        new_playlists = str(id)
    db.execute("UPDATE users SET playlists = ? WHERE id = ?", [new_playlists, user])
    db.commit()
    return id


def get_playlist_songs(db, id):
    result = db.execute("SELECT songs FROM playlists WHERE id = ?", [id]).fetchone()
    if not result[0]:
        return []
    songs = [int(id) for id in result[0].split(",")]
    result = db.execute("SELECT id, title, artist, length FROM songs WHERE id IN ? ORDER BY title", [songs]).fetchall()
    return result


def rename_playlist(db, id, name):
    db.execute("UPDATE playlists SET name = ? WHERE id = ?", [name, id])
    db.commit()


def delete_playlist(db, id):
    filters = [f"{id}", f"{id},%", f"%,{id},%", f"%,{id}"]
    result = db.execute("SELECT id, playlists FROM users WHERE playlists = ? OR playlists LIKE ? OR playlists LIKE ? OR playlists LIKE ?", filters).fetchall()
    for user, playlists in result:
        playlists = playlists.split(",")
        playlists.remove(str(id))
        new_playlists = ",".join(playlists)
        db.execute("UPDATE users SET playlists = ? WHERE id = ?", [new_playlists, user])
    db.commit()
