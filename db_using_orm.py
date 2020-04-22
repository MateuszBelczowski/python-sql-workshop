import json
import random

from sqlalchemy import create_engine, Column, Integer, String, TEXT, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///music_quiz_orm.db')

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    artist = Column(TEXT)
    title = Column(TEXT)
    lyrics = Column(TEXT)
    __table_args__ = (UniqueConstraint('artist', 'title', name='_artist_title_uc'),
                      )

class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    nick = Column(TEXT)
    questions_total = Column(Integer)


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    song = relationship("Song", back_populates="answers")
    answer = Column(TEXT)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", back_populates="answers")
    given_lyrics = Column(TEXT)

Song.answers = relationship("Answer", back_populates='song')
Quiz.answers = relationship("Answer", back_populates='quiz')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

def create_multiple_songs():
    with open("final_songs.json") as f:
        songs = json.load(f)
    for song in songs:
        song_obj = Song(artist=song['artist'], title=song['title'], lyrics=song['lyrics'])
        session.add(song_obj)
    session.commit()

"""
get_random_lyrics, check_if_correct, get_artist_and_title_from_lyrics, save_answer, add_quiz, \
    summarize_quiz
"""

def get_random_lyrics(characters_total=200):
    all_songs = session.query(Song).all()
    random_song = random.choice(all_songs)
    return random_song.id, random_song.lyrics[:characters_total]

def get_song_by_id(song_id):
    song = session.query(Song).filter(Song.id == song_id).first()
    return song.artist, song.title

def save_answer(quiz_id, song_id, user_answer, given_lyrics):
    answer = Answer(song_id=song_id, quiz_id=quiz_id, answer=user_answer, given_lyrics=given_lyrics)
    session.add(answer)
    session.commit()

def add_quiz(username, questions_total):
    quiz = Quiz(nick=username, questions_total=questions_total)
    session.add(quiz)
    session.commit()

def summarize_quiz(quiz_id):
    print("Your answer, Correct answer")
    for answer in session.query(Answer).join(Song).filter(Answer.quiz_id == quiz_id):
        print(answer.answer, answer.song.artist)

# create_multiple_songs()




