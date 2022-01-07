from typing import Dict
from utils.utils import check_green, check_grey, check_yellow, english_dictionary


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

    def check_word(self, input_word: str) -> Dict:
        """

        :param input_word: string of word to check
        :return: dictionary of green, yellow, and grey indices
        """
        return {"green": check_green(input_word, self.target_word),
                "yellow": check_yellow(input_word, self.target_word),
                "grey": check_grey(input_word, self.target_word)}

    def play_round(self, input_word: str):
        input_word = input_word.lower()
        color_checks = self.check_word(input_word)
        blank_letters = ["_", "_", "_", "_", "_"]
        green_letters = blank_letters.copy()
        yellow_letters = blank_letters.copy()
        grey_letters = blank_letters.copy()

        for green_index in color_checks["green"]:
            green_letters[green_index] = input_word[green_index]
        green_letters_str = " ".join(green_letters)

        for grey_index in color_checks["grey"]:
            grey_letters[grey_index] = input_word[grey_index]
        grey_letters_str = " ".join(grey_letters)

        for yellow_index in color_checks["yellow"]:
            yellow_letters[yellow_index] = input_word[yellow_index]
        yellow_letters_str = " ".join(yellow_letters)

        print(f"Letters in the correct spot: {green_letters_str}")
        print(f"Common letters: {yellow_letters_str}")
        print(f"Uncommon letters: {grey_letters_str}")

        self.rounds += 1
        print(f"Round {self.rounds}")
        if len(color_checks["green"]) == 5:
            self.won = True
            print("Congrats! You guessed the right word!")

    def play_game(self):
        print("Welcome to wordle!")
        while not self.won and self.rounds < self.max_rounds:
            print("Enter a guess:")
            self.play_round(input())


if __name__ == "__main__":
    wordle_game = WordleGame("banal", 6)
    wordle_game.play_game()
