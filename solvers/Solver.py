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

        avg_similarity_unnormalized = np.mean(1 - cdist(corpus_matrix.T, corpus_matrix.T, "cosine"), axis=1,
                                              keepdims=True)
        return avg_similarity_unnormalized / np.sum(avg_similarity_unnormalized)


class FrequencyMaxWordleSolver(AbstractWordleSolver, ABC):

    def __init__(self):
        super().__init__()
        self.letters = np.asarray(list(string.ascii_lowercase))

    def freq_generator(self, corpus: List[str]) -> np.array:
        letter_frequencies = np.zeros([5, 26])  # initialize
        for i in corpus:
            for j in np.arange(len(i)):
                letter_frequencies[j, np.where(i[j] == self.letters)] += 1
        return letter_frequencies

    def word_scorer(self, corpus: List[str], letter_frequencies: np.array) -> str:
        scores_array = []
        for i in corpus:
            total_score = 0
            for j in np.arange(len(i)):
                letter_score = letter_frequencies[j, np.where(i[j] == self.letters)]
                total_score = total_score + letter_score
            scores_array.append(total_score)
        best_word_index = np.argmax(scores_array)
        return corpus[best_word_index]

    def choose_word(self, corpus: List[str]) -> str:
        freq = self.freq_generator(corpus)
        output = self.word_scorer(corpus, freq)
        return output
