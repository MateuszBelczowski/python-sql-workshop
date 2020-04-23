from db import get_random_lyrics, get_song_by_id

class GuessThatSongQuiz:

    def ask_question(self):
        """
        random lyrics, song_id
        :return:
        """
        song_id, lyrics = get_random_lyrics()
        print(lyrics)
        answer = input("Who's the artist -> ")
        print(f"User's answer was {answer}")
        correct_artist, title = get_song_by_id(song_id)
        if correct_artist == answer:
            print("Congratulations...")
        else:
            print(f"Nope, it was {correct_artist} with the song {title}")





quiz = GuessThatSongQuiz()
quiz.ask_question()
