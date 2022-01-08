import random
from abc import ABC, abstractmethod
from typing import List


class AbstractWordleSolver(ABC):
    """
    abc for wordle solver
    """

    def __init__(self):
        pass

    @abstractmethod
    def choose_word(self, corpus: List[str]) -> str:
        pass


class RandomMethodWordleSolver(AbstractWordleSolver, ABC):
    def __init__(self):
        super().__init__()

    def choose_word(self, corpus: List[str]) -> str:
        return random.choice(corpus)
