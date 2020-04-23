import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, TEXT, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///music_quiz_orm.db")

Base = declarative_base()

class Song(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist = Column(TEXT)
    title = Column(TEXT)
    lyrics = Column(TEXT)

    __tablename__ = 'songs'
    __table_args__ = (UniqueConstraint('artist', 'title', name='_artist_title_uc'),)

class Quiz(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nick = Column(TEXT)
    total_points = Column(Integer)

    __tablename__ = 'quizzes'

class Answer(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(TEXT)
    given_lyrics = Column(TEXT)
    song_id = Column(Integer, ForeignKey("songs.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    song = relationship('Song', back_populates='answers')
    quiz = relationship('Quiz', back_populates='answers')

    __tablename__ = 'answers'

Song.answers = relationship('Answer', back_populates='song')
Quiz.answers = relationship('Answer', back_populates='quiz')


Base.metadata.create_all(engine)
