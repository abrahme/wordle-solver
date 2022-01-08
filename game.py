from utils.common import NUM_LETTERS, ENGLISH_DICTIONARY, COLORS
from utils.filter import Filter
from utils.utils import get_letter_colors
from typing import Dict

class WordleGame(object):
    """
    just a way to play the game
    """

    def __init__(self, target_word: str, round_max: int):
        """

        :param target_word: NUM_LETTERS letter word in english dictionary
        :param round_max: integer greater than 1 for number of rounds
        """
        assert len(target_word) == NUM_LETTERS, f"Only { NUM_LETTERS } letter words allowed"
        assert target_word in ENGLISH_DICTIONARY, "Must be a viable English word"
        assert isinstance(round_max, int), "Number of rounds must be an integer"
        assert round_max >= 1, "Number of rounds must be greater than or equal to 1"
        self.target_word = target_word.lower()
        self.rounds = 0  ## initialize how many rounds have been played
        self.max_rounds = round_max  ### number of total allowed rounds
        self.won = False  ### checks to see if we won
        self.corpus = ENGLISH_DICTIONARY
        self.filter = Filter(target_word, ENGLISH_DICTIONARY)

    def play_round(self, input_word: str):
        input_word = input_word.lower().strip()
        assert len(input_word) == NUM_LETTERS, f"Only { NUM_LETTERS } letter words allowed"
        assert input_word in ENGLISH_DICTIONARY, "Must be a viable English word"
        letter_colors = get_letter_colors(input_word, self.target_word)
        blank_letters = ["_", "_", "_", "_", "_"]
        green_letters = blank_letters.copy()
        yellow_letters = blank_letters.copy()
        grey_letters = blank_letters.copy()

        for letter in letter_colors:
            if COLORS.green in letter_colors[letter]:
                for index in letter_colors[letter][COLORS.green]:
                    green_letters[index] = letter
            elif COLORS.yellow in letter_colors[letter]:
                for index in letter_colors[letter][COLORS.yellow]:
                    yellow_letters[index] = letter
            elif COLORS.grey in letter_colors[letter]:
                for index in letter_colors[letter][COLORS.grey]:
                    grey_letters[index] = letter

        green_letters_str = " ".join(green_letters)
        grey_letters_str = " ".join(grey_letters)
        yellow_letters_str = " ".join(yellow_letters)

        print("Possible words left")
        self.corpus = self.filter.filter_words(letter_colors)
        print(self.corpus)
        print(f"Letters in the correct spot: {green_letters_str}")
        print(f"Common letters: {yellow_letters_str}")
        print(f"Uncommon letters: {grey_letters_str}")

        self.rounds += 1
        print(f"Round {self.rounds}")
        green_letters = 0
        for letter in letter_colors:
            if COLORS.green in letter_colors[letter]:
                green_letters += len(letter_colors[letter][COLORS.green])
        if green_letters == NUM_LETTERS:
            self.won = True
            print("Congrats! You guessed the right word!")

    def play_game(self):
        print("Welcome to wordle!")
        while not self.won and self.rounds < self.max_rounds:
            print("Enter a guess:")
            try:
                self.play_round(input())
            except AssertionError as e:
                print(e)
                print("Try again!")


if __name__ == "__main__":
    wordle_game = WordleGame("banal", 6)
    wordle_game.play_game()
