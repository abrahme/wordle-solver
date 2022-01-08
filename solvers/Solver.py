import random
from abc import ABC, abstractmethod
from typing import List
import numpy as np

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


class FrequencyMaxWordleSolver(AbstractWordleSolver, ABC):

    def __init__(self):
        super().__init__()
        self.letters=np.asarray(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n","o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"])

    def freq_generator(self, corpus: List[str])-> List[int]: 
        letter_frequencies=np.zeros([5,26]) #initialize
        for i in corpus:
            for j in np.arange(len(i)):
                letter_frequencies[j,np.where(i[j] == self.letters)] +=1 
        return letter_frequencies
        
    def word_scorer(self, corpus: List[str], letter_frequencies: List[int]) -> str:
        scores_array=[]
        for i in corpus:
            total_score=0
            for j in np.arange(len(i)):
                letter_score=letter_frequencies[j,np.where(i[j] == self.letters)]
                total_score=total_score+letter_score
            scores_array.append(total_score)
        best_word_index=np.argmax(scores_array)
        return corpus[best_word_index]
    
    def choose_word(self, corpus: List[str]) -> str:
        freq=self.freq_generator(corpus)
        output=self.word_scorer(corpus,freq)
        return output