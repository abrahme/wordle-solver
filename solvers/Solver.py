import string
import numpy as np
from numpy.random import choice
from scipy.spatial.distance import cdist
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
        return choice(corpus, 1)


class LetterCountWordSimilaritySolver(AbstractWordleSolver, ABC):
    def __init__(self, is_random=False):
        """

        :param is_random: if we pick the most optimal word with probability
        """
        super().__init__()
        self.is_random = is_random
        self.alphabet = {letter: index for index, letter in enumerate(string.ascii_lowercase)}

    def choose_word(self, corpus: List[str]) -> str:
        """

        :param corpus: list of possible words to choose from
        :return: best word based on the word which is most similar to all other words
        """
        avg_similarity = np.squeeze(self.__compute_word_similarity_corpus(corpus))
        if self.is_random:
            return choice(corpus, 1, p=avg_similarity)[0]
        else:
            return corpus[np.argmax(avg_similarity)]

    def __word_to_vec(self, input_word: str) -> np.array:
        """

        :param input_word: n letter word
        :return: 26 x 1 np.array with entries for count of letter a is index 0 and so zon
        """
        word_vec = np.zeros((26, 1))
        for letter in input_word:
            word_vec[self.alphabet[letter], 0] += 1
        return word_vec

    def __compute_word_similarity_corpus(self, corpus: List[str]) -> np.array:
        """

        :param corpus: list of string of possible words
        :return: len(corpus) x 1 np.array of average similarity between word and all other words
        """

        n = len(corpus)
        corpus_matrix = np.zeros((26, n))

        for index, word in enumerate(corpus):
            corpus_matrix[:, index] = np.squeeze(self.__word_to_vec(word))

        avg_similarity_unnormalized = np.mean(1 - cdist(corpus_matrix.T, corpus_matrix.T, "cosine"), axis=1, keepdims=True)
        return avg_similarity_unnormalized / np.sum(avg_similarity_unnormalized)
