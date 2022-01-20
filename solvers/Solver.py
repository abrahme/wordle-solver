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
        return choice(corpus, 1)[0]


class LetterCountWordSimilaritySolver(AbstractWordleSolver, ABC):

    def __init__(self, corpus: List[str], is_random=False):
        """

        :param is_random: if we pick the most optimal word with probability
        """
        super().__init__()
        self.corpus = corpus  #### full corpus
        self.corpus_map = {word: index for index, word in enumerate(corpus)}
        self.is_random = is_random
        self.alphabet = {letter: index for index, letter in enumerate(string.ascii_lowercase)}
        print("Initiating similarity matrix ....")
        self.similarity_matrix = self.compute_word_similarity_corpus(self.corpus)

    def choose_word(self, corpus: List[str]) -> str:
        """

        :param corpus: list of possible words to choose from
        :return: best word based on the word which is most similar to all other words
        """
        avg_similarity = np.mean(self.return_word_similarity(corpus), axis=1)
        if self.is_random:
            return choice(corpus, 1, p=avg_similarity)[0]
        else:
            return corpus[np.argmax(avg_similarity)]

    def word_to_vec(self, input_word: str) -> np.array:
        """

        :param input_word: n letter word
        :return: 26 x 1 np.array with entries for count of letter a is index 0 and so zon
        """
        word_vec = np.zeros((26, 1))
        for letter in input_word:
            word_vec[self.alphabet[letter], 0] += 1
        return word_vec

    def compute_word_similarity_corpus(self, corpus: List[str]) -> np.array:
        """

        :param corpus: list of string of possible words
        :return: len(corpus) x len(corpus) np.array of similarity between word and all other words
        """

        ### same size corpus, so first time seeing it as initialized
        n = len(corpus)
        corpus_matrix = np.zeros((26, n))

        for index, word in enumerate(corpus):
            corpus_matrix[:, index] = np.squeeze(self.word_to_vec(word))

        similarity_unnormalized = 1 - cdist(corpus_matrix.T, corpus_matrix.T, "cosine")
        return similarity_unnormalized

    def return_word_similarity(self, corpus: List[str]) -> np.array:
        """

        :param corpus: list of str
        :return: similarities
        """
        keep_indices = [self.corpus_map[word] for word in corpus]
        val = self.similarity_matrix[np.ix_(keep_indices, keep_indices)]
        return val


class PositionalSimilarityWordleSolver(LetterCountWordSimilaritySolver, ABC):
    """
    similarity measure based on position of letter so "black" and "bland" are similar but "black" and "balls" are less
    """

    def compute_word_similarity_corpus(self, corpus: List[str]) -> np.array:
        """

        :param corpus: list of str of words to compute similarity
        :return: len(corpus) * len(corpus) matrix
        """
        n = len(corpus)
        word_length = len(corpus[0])
        sim_mat = np.zeros((n, n))
        for index, word in enumerate(corpus):
            for index_2, word_2 in enumerate(corpus[index+1:]):
                sim_mat[index, index_2 + index +1] = np.sum(self.word_to_vec(word_2) * self.word_to_vec(word)) / word_length
        sim_mat += sim_mat.T
        sim_mat += np.eye(n)
        return sim_mat

    def word_to_vec(self, input_word: str) -> np.array:
        """

        :param input_word: n letter string
        :return: n x 26 binary array representing the word
        """
        n = len(input_word)
        vec = np.zeros((n, 26))
        for index, character in enumerate(input_word):
            vec[index, self.alphabet[character]] = 1
        return vec


class MixedWordleSolver(LetterCountWordSimilaritySolver, ABC):
    def __init__(self, solvers: List[LetterCountWordSimilaritySolver],is_random = False):
        """

        :param solvers: which solvers we are combining
        """
        self.is_random = is_random
        self.solvers = solvers
        self.similarity_matrix = 1
        self.corpus = self.solvers[0].corpus  #### full corpus
        self.corpus_map = self.solvers[0].corpus_map
        self.alphabet = self.solvers[0].alphabet
        for solver in solvers:
            self.similarity_matrix *= solver.similarity_matrix

    def compute_word_similarity_corpus(self, corpus: List[str]) -> np.array:
        """
        not implemented
        :param corpus:
        :return:
        """
        raise AttributeError("MixedWordleSolver has no attribute 'compute_word_similarity_corpus'")

    def word_to_vec(self, input_word: str) -> np.array:
        """
        not implemented
        :param input_word:
        :return:
        """
        raise AttributeError("MixedWordleSolver has no attribute 'word_to_vec'")


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
