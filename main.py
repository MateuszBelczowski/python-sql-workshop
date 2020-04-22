# from db import *
from db_using_orm import *


class Kolory:
    ROZOWY = '\033[95m'
    NIEBIESKI = '\033[94m'
    ZIELONY = '\033[92m'
    ZOLTY = '\033[93m'
    CZERWONY = '\033[91m'
    ENDC = '\033[0m'
    BIALY = '\033[1m'
    PODKRESLENIE = '\033[4m'


class GuessThatSongQuiz:

    def __init__(self, number_of_questions, quiz_id, nickname):
        if number_of_questions <= 0:
            raise Exception("No need to play")
        self.questions_total = number_of_questions
        self.guessed = 0
        self.quiz_id = quiz_id
        self.nickname = nickname


    def ask_question(self, characters_total=200):
        print("Guess the artist of the following lyrics")
        id, lyrics = get_random_lyrics(characters_total)
        self.pretty_print_lyrics(lyrics)
        return id, lyrics

    def pretty_print_lyrics(self, lyrics):
        print("======================")
        print()
        print(f"{Kolory.NIEBIESKI}{lyrics}{Kolory.ENDC}")
        print("======================")
        print()

    def check_answer(self, song_id, lyrics):
        answer = input(f"{Kolory.PODKRESLENIE}What's your guess? {Kolory.ENDC} ->")
        save_answer(quiz_id=self.quiz_id, song_id=song_id, user_answer=answer, given_lyrics=lyrics)
        artist, title = get_song_by_id(song_id)
        if artist.lower() == answer.lower():
            self.guessed += 1
            print(f"{Kolory.ZIELONY}Congrats ...{Kolory.ENDC}")
        else:
            print(f"{Kolory.CZERWONY}Nope...{Kolory.ENDC}")
            print(f"{Kolory.CZERWONY}The answer was: {artist} ({title}){Kolory.ENDC}")


    def play(self):
        for question_number in range(self.questions_total):
            print(f"{question_number + 1} out of {self.questions_total}")
            character_count = (self.questions_total - question_number + 1) * 100
            song_id, lyrics = self.ask_question(character_count)
            self.check_answer(song_id, lyrics)

        print(f"total score: {self.guessed}/{self.questions_total}")


def ask_user_for_number():
    while True:
        number_of_songs = input("""How many songs would you like to guess?""")
        try:
            number_of_songs = int(number_of_songs)
            if number_of_songs <= 0:
                continue
            return number_of_songs
        except ValueError:
            continue

def ask_user_for_nickname():
    return input("What's your nickname")


def main():
    try:

        nickname = ask_user_for_nickname()
        number_of_songs = ask_user_for_number()
        quiz_id = add_quiz(nickname, number_of_songs)
        quiz = GuessThatSongQuiz(number_of_songs, quiz_id, nickname)
        quiz.play()
        summarize_quiz(quiz_id)

    except KeyboardInterrupt:
        print("We're sad to see you leave, bye...")
    pass


if __name__ == '__main__':
    main()