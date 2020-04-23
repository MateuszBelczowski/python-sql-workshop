import sqlite3
import json
import random

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
    return all_songs

def get_song_by_id(song_id):
    get_song_sql = """
    SELECT * FROM songs WHERE id=?;
    """
    one_song = connection.execute(get_song_sql, (song_id, )).fetchone()
    return one_song


def get_random_lyrics():
    all_songs = get_all_songs()
    id, artist, title, lyrics = random.choice(all_songs)
    return id, lyrics

def create_quizzes_table():
    create_quizzes_table_sql = """
    CREATE TABLE IF NOT EXISTS
    quizzes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT,
    total_questions INTEGER
    );
    """
    connection.execute(create_quizzes_table_sql)

def add_quiz():
    pass

def create_answers_table():
    pass

def add_answer():
    pass

def summarize_quiz():
    pass


create_songs_table()
create_quizzes_table()
