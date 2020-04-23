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
    SELECT artist,title FROM songs WHERE id=?;
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

def add_quiz(nickname, total_questions):
    add_quiz_sql = """
    INSERT INTO quizzes(nickname, total_questions) VALUES (?, ?);
    """
    with connection:
        res = connection.execute(add_quiz_sql, (nickname, total_questions))
    return res.lastrowid

def create_answers_table():
    create_answers_sql = """
    CREATE TABLE IF NOT EXISTS
    answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id INTEGER,
    quiz_id INTEGER,
    answer TEXT,
    given_lyrics TEXT,
    FOREIGN KEY(song_id) REFERENCES songs(id),
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
    );
    """
    connection.execute(create_answers_sql)

def add_answer(song_id, quiz_id, answer, given_lyrics):
    add_answer_sql = """
    INSERT INTO answers(song_id, quiz_id, answer, given_lyrics)
    VALUES (?, ?, ?, ?);
    """
    with connection:
        connection.execute(add_answer_sql, (song_id, quiz_id, answer, given_lyrics))

def summarize_quiz(quiz_id):
    summary_sql = """
    SELECT songs.artist, answers.answer FROM answers JOIN songs ON songs.id=answers.song_id
    WHERE quiz_id=?
    """
    summary = connection.execute(summary_sql, (quiz_id, )).fetchall()
    return summary


# create_songs_table()
# create_quizzes_table()
# quiz_id = add_quiz("Mateusz", 4)
# print(f"Utworzony quiz ma id {quiz_id}")
# create_answers_table()
# for i in range(1, 6):
#     add_answer(i, quiz_id, "Adele", "blabla")
#
# print(summarize_quiz(quiz_id))


