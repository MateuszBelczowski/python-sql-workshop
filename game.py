from db import get_random_lyrics, get_song_by_id, add_quiz, add_answer, summarize_quiz

class GuessThatSongQuiz:

    def __init__(self):
        username = input("What's your username? ->")
        total_questions = input("How many questions do you want? ->")
        quiz_id = add_quiz(username, total_questions)
        self.quiz_id = quiz_id
        self.total_questions = int(total_questions)
        self.points = 0

    def play(self):
        for i in range(self.total_questions):
            self.ask_question()



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
            self.points += 5
            print("Congratulations...")
        else:
            print(f"Nope, it was {correct_artist} with the song {title}")
            self.points -= 10

        add_answer(song_id, self.quiz_id, answer, lyrics)





quiz = GuessThatSongQuiz()
quiz.play()
print(summarize_quiz(quiz.quiz_id))
print(f"Total points {quiz.points}")

# 1) sprawdzanie po feat.
# 2) [DONE] punktacja
# 3) leaderboard
# 4) mniej tekstu, im dalsze pytanie
