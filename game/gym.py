from game.game import WordleGame
from typing import List, Tuple
import random


class WordleGym(object):
    """
    object to mimic open AI gym env for wordle
    """

    def __init__(self, max_rounds: int, corpus: List[str]):
        self.max_rounds = max_rounds
        self.corpus = corpus
        self.wordle_game = None
        self.reset()

    def reset(self):
        """
        resets the gym state by creating a new wordle object
        :return: wordle object
        """
        target_word = random.choice(self.corpus)
        self.wordle_game = WordleGame(target_word, self.max_rounds)

    def step(self, action: int) -> Tuple[List[str], float, bool, dict]:
        """

        :param action: integer representing which index of corpus to pick
        :return:
        """
        self.wordle_game.play_round(self.corpus[action])

        return self.wordle_game.corpus, 0.0, self.wordle_game.game_over, {"result": self.wordle_game.won}