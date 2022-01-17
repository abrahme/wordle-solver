import re
import numpy as np
from utils.utils import english_dictionary
from typing import List, Dict


class Filter(object):
    def __init__(self, target_word: str, corpus: List[str]):
        self.target_word = target_word
        self.corpus = corpus

    def assign_colors(self, input_word: str) -> np.array:
        """

        :param input_word: string to check against
        :return: numpy array of 0 1 2 of no match, match no spot, match spot
        """
        input_word_vec = np.asarray(list(input_word))
        target_word_vec = np.asarray(list(self.target_word))
        exact = 2 * (input_word_vec == target_word_vec)
        inexact = np.where(input_word_vec != target_word_vec)[0]  ### indices of where we didn't match

        for i in inexact:
            for j in inexact:
                wrong_spot = input_word[i] == self.target_word[j]
                if wrong_spot:
                    exact[i] = 1
                    inexact = inexact[inexact != j]
                    break

        return exact

    @staticmethod
    def update(input_word: str, assigned_colors: np.array) -> Dict:
        """

        :param input_word: word to check against
        :param assigned_colors: numpy array of 0,1,2
        :return: dictionary of information
        """
        min_count = dict()
        known_count = dict()
        letters = np.asarray(list(input_word))
        n = len(input_word)
        exact = np.asarray(["."] * n)
        wrong_spot = np.asarray([""] * n)
        ### update exact characters
        exact[assigned_colors == 2] = letters[assigned_colors == 2]
        wrong_spot[assigned_colors == 1] = letters[assigned_colors == 1]

        for letter in set(list(input_word)):
            letter_response = assigned_colors[letters == letter]
            if len(letter_response) == 1:
                if letter_response[0] == 0:
                    known_count[letter] = 0
                else:
                    min_count[letter] = max(min_count[letter], 1) if letter in min_count else 1
            else:
                if np.sum(letter_response) == 0:
                    known_count[letter] = 0
                elif len(letter_response) == np.sum(letter_response >= 1):
                    #### either green or yellow
                    min_count[letter] = max(min_count[letter], len(letter_response)) if letter in min_count else \
                        len(letter_response)
                else:
                    known_count[letter] = np.sum(letter_response != 0)
        return {"min_count": min_count, "exact_count": known_count, "exact": exact, "wrong_spot": wrong_spot}

    def filter_words(self, update_dict: Dict) -> List[str]:
        """

        :param update_dict: output of update function
        :return: new list of possible words
        """

        wrong_spot = update_dict["wrong_spot"]
        wrong_spot_regex = []
        for letter in wrong_spot.tolist():
            if len(letter) == 0:
                wrong_spot_regex.append(".")
            else:
                wrong_spot_regex.append(f"[^{letter}]")

        final_regex = update_dict["exact"].tolist().copy()
        for index, letter in enumerate(final_regex):
            if letter == ".":
                final_regex[index] = wrong_spot_regex[index]
        regex = "^" + "".join(final_regex) + "$"
        regex_filter_list = [word for word in self.corpus if bool(re.search(regex, word))]
        min_count = update_dict["min_count"]
        for letter in min_count:
            regex_filter_list = [word for word in regex_filter_list if word.count(letter) >= min_count[letter]]

        exact_count = update_dict["exact_count"]
        for letter in exact_count:
            regex_filter_list = [word for word in regex_filter_list if word.count(letter) == exact_count[letter]]

        self.corpus = regex_filter_list
        return regex_filter_list


if __name__ == "__main__":
    test_filter = Filter("banal", english_dictionary)
    colors = test_filter.assign_colors("canal")
    print(colors)
    update_dict = test_filter.update("canal", colors)
    print(update_dict)
    print(test_filter.filter_words(update_dict))
