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
        letter_colors = self.filter.get_letter_colors(input_word)
        blank_letters = ["_", "_", "_", "_", "_"]
        green_letters = blank_letters.copy()
        yellow_letters = blank_letters.copy()
        grey_letters = blank_letters.copy()

        for letter in letter_colors:
            if "green" in letter_colors[letter]:
                for index in letter_colors[letter]["green"]:
                    green_letters[index] = letter
            elif "yellow" in letter_colors[letter]:
                for index in letter_colors[letter]["yellow"]:
                    yellow_letters[index] = letter
            elif "grey" in letter_colors[letter]:
                for index in letter_colors[letter]["grey"]:
                    grey_letters[index] = letter
        self.corpus = self.filter.filter_words(input_word)

        self.rounds += 1
        if self.rounds > self.max_rounds:
            self.game_over = True
        green_letters = 0
        for letter in letter_colors:
            if "green" in letter_colors[letter]:
                green_letters += len(letter_colors[letter]["green"])
        if green_letters == 5:
            self.won = True
            self.game_over = True

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
    wordle_game = WordleGame("arise", 6)
    wordle_game.play_game()
