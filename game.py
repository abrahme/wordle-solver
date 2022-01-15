import numpy as np
from utils.filter import Filter
from utils.utils import english_dictionary


class WordleGame(object):
    """
    just a way to play the game
    """

    def __init__(self, target_word: str, round_max: int):
        """

        :param target_word: 5 letter word in english dictionary
        :param round_max: integer greater than 1 for number of rounds
        """

        assert len(target_word) == 5, "Only 5 letter words allowed"
        assert target_word in english_dictionary, "Must be a viable English word"
        assert isinstance(round_max, int), "Number of rounds must be an integer"
        assert round_max >= 1, "Number of rounds must be greater than or equal to 1"
        self.target_word = target_word.lower()
        self.rounds = 0  ## initialize how many rounds have been played
        self.max_rounds = round_max  ### number of total allowed rounds
        self.won = False  ### checks to see if we won
        self.game_over = False  ### check to see if game is over
        self.corpus = english_dictionary.copy()
        self.filter = Filter(target_word, english_dictionary)

    def play_round(self, input_word: str):
        input_word = input_word.lower()
        assert len(input_word) == 5, "Only 5 letter words allowed"
        assert input_word in english_dictionary, "Must be a viable English word"
        input_word_vec = np.asarray(list(input_word))
        letter_colors = self.filter.assign_colors(input_word)
        blank_letters = np.asarray(["_"] * len(input_word))
        green_letters = blank_letters.copy()
        yellow_letters = blank_letters.copy()
        grey_letters = blank_letters.copy()

        green_letters[letter_colors == 2] = input_word_vec[letter_colors == 2]
        grey_letters[letter_colors == 0] = input_word_vec[letter_colors == 0]
        yellow_letters[letter_colors == 1] = input_word_vec[letter_colors == 1]
        green_letters_str = " ".join(green_letters.tolist())
        grey_letters_str = " ".join(grey_letters.tolist())
        yellow_letters_str = " ".join(yellow_letters.tolist())

        print("Possible words left")
        self.corpus = self.filter.filter_words(self.filter.update(input_word, letter_colors))
        print(self.corpus)
        print(f"Letters in the correct spot: {green_letters_str}")
        print(f"Common letters: {yellow_letters_str}")
        print(f"Uncommon letters: {grey_letters_str}")
        self.rounds += 1
        if self.rounds > self.max_rounds:
            self.game_over = True
        print(f"Round {self.rounds}")
        if np.sum(letter_colors == 2) == 5:
            self.won = True
            self.game_over = True
            print("Congrats! You guessed the right word!")

    def play_game(self):
        print("Welcome to wordle!")
        while not self.game_over:
            print("Enter a guess:")
            try:
                self.play_round(input())
            except AssertionError as e:
                print(e)
                print("Try again!")


if __name__ == "__main__":
    wordle_game = WordleGame("sissy", 6)
    wordle_game.play_game()
