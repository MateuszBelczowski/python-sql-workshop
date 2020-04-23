import sqlite3

DATABASE_NAME = "sqlite_example2.db"

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




create_songs_table()
add_song("James Blunt", "Monster3", "nananana2")