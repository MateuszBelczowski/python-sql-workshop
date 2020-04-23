import sqlite3
import json

DATABASE_NAME = "music_quiz.db"

connection = sqlite3.connect(DATABASE_NAME)

def create_songs_table():
    create_songs_table_sql = """
    CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT,
    title TEXT,
    lyrics TEXT,
    UNIQUE(artist, title)
    );
    """
    connection.execute(create_songs_table_sql)

def add_song(artist, title, lyrics):
    insert_song_sql = """
    INSERT INTO 
    songs(artist, title, lyrics)
    VALUES (?, ?, ?);
    """
    with connection:
        connection.execute(insert_song_sql, (artist, title, lyrics))

def add_all_songs():
    with open("final_songs.json", encoding="utf-8") as file_with_songs:
        songs = json.load(file_with_songs)
    for song in songs:
        add_song(song['artist'], song['title'], song['lyrics'])

def get_all_songs():
    get_songs_sql = """
    SELECT * FROM songs;
    """
    all_songs = connection.execute(get_songs_sql).fetchall()
    print(f"There are {len(all_songs)} in the database")


create_songs_table()
add_all_songs()
get_all_songs()
