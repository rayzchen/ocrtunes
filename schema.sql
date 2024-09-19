DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    dob TEXT,
    fav_artist TEXT,
    fav_genre TEXT,
    playlists TEXT
);

DROP TABLE IF EXISTS playlists;

CREATE TABLE playlists (
    id INTEGER PRIMARY KEY,
    name TEXT,
    songs TEXT
);

DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    id INTEGER PRIMARY KEY,
    title TEXT,
    artist TEXT,
    genre TEXT,
    length INTEGER
);
