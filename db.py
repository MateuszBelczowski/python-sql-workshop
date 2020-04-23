import json
import random
import sqlite3

DATABASE_NAME = "music_quiz_test6.db"


connection = sqlite3.connect(DATABASE_NAME)

def create_songs_table():
    create_songs_table_stmt = """
    CREATE TABLE IF NOT EXISTS
    songs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT,
    title TEXT,
    lyrics TEXT,
    UNIQUE (artist, title)
    );
    """
    connection.execute(create_songs_table_stmt)

def create_quiz_table():
    create_quiz_table_stmt = """
    CREATE TABLE IF NOT EXISTS
    quizzes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nick TEXT,
    questions_total INTEGER
    );
    """
    connection.execute(create_quiz_table_stmt)


def create_answer_table():
    create_answer_table_stmt = """
    CREATE TABLE IF NOT EXISTS
    answers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id INTEGER,
    answer TEXT,
    quiz_id INTEGER,
    given_lyrics TEXT,
    FOREIGN KEY(song_id) REFERENCES songs(id),
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
    );
    """
    connection.execute(create_answer_table_stmt)


def add_song():
    song = {
        "artist": "test_artist3",
        "title": "test_title3",
        "lyrics": "lananana"
    }
    insert_song_stmt = f"""
    INSERT INTO songs(artist, title, lyrics)
    VALUES ('{song['artist']}', '{song['title']}', '{song['lyrics']}');
    """

    with connection:
        connection.execute(insert_song_stmt)

def add_multiple_songs():
    with open("final_songs.json", encoding="utf-8") as f:
        songs = json.load(f)
    for song in songs:
        insert_song_stmt = f"""
        INSERT INTO songs (artist, title, lyrics)
        VALUES (?,?,?);
        """

        print(insert_song_stmt)
        with connection:
            connection.execute(insert_song_stmt, (song['artist'], song['title'], song['lyrics']))


def add_multiple_songs_faster():
    with open("final_songs.json", encoding="utf-8") as f:
        songs = json.load(f)
    insert_songs_stmt = f"""
    INSERT INTO songs (artist, title, lyrics)
    VALUES (?,?,?);
    """
    songs_tuples = [(song['artist'], song['title'], song['lyrics']) for song in songs]
    with connection:
        connection.executemany(insert_songs_stmt, songs_tuples)


def get_list_of_lyrics():
    select_stmt = """
    SELECT id, lyrics from songs; 
    """
    return connection.execute(select_stmt).fetchall()

def get_random_lyrics(characters_count=200):
    all_songs = get_list_of_lyrics()
    idx, lyrics = random.choice(all_songs)
    return idx, lyrics[:characters_count]


def get_song_by_id(song_id):
    select_stmt = f"""
    SELECT artist, title FROM songs where song_id=?
    """
    artist, title = connection.execute(select_stmt, (song_id, )).fetchone()
    return artist, title


def add_quiz(username, questions_total):
    insert_quiz_stmt = f"""
    INSERT INTO quizzes(nick, questions_total)
    VALUES (?,?);
    """
    with connection:
        res = connection.execute(insert_quiz_stmt, (username, questions_total))
    return res.lastrowid

def save_answer(quiz_id, song_id, user_answer, given_lyrics):
    insert_answer_stmt = f"""
    INSERT INTO answers(quiz_id, song_id, answer, given_lyrics)
    VALUES (?,?,?,?);
    """
    with connection:
        res = connection.execute(insert_answer_stmt, (quiz_id, song_id, user_answer, given_lyrics))
    pass

def summarize_quiz(quiz_id):
    select_stmt = f"""
    SELECT answers.answer as your_answer, songs.artist as correct_answer from answers
    LEFT JOIN songs ON
        songs.id = answers.song_id
    LEFT JOIN quizzes ON
        quizzes.id = answers.quiz_id
    WHERE quiz_id=?;
    """
    data = connection.execute(select_stmt, (quiz_id, ))
    print(data.description)
    print(data.fetchall())

def setup():
    create_songs_table()
    add_multiple_songs_faster()
    create_quiz_table()
    create_answer_table()

# setup()
#
# quiz_id = add_quiz("test", 10)
#
#
# for i in range(1, 10):
#     save_answer(1, i, "Adele")
#
# summarize_quiz(quiz_id)





