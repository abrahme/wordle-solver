import re

from utils.utils import english_dictionary, _unnest, _check_green
from typing import List, Dict


class Filter(object):
    def __init__(self, target_word: str, corpus: List[str]):
        self.target_word = target_word
        self.corpus = corpus

    def get_letter_colors(self, input_word: str) -> Dict:
        """

        :param input_word: string of word to check
        :return: dictionary of color to list of indices
        """
        target_word = self.target_word
        green_indices = _check_green(input_word, target_word)

        #### color indices
        letter_dict = {}
        input_word_list = list(input_word)
        target_word_list = list(target_word)
        for ind in green_indices:
            input_word_list[ind] = "_"
            target_word_list[ind] = "_"
            if input_word[ind] not in letter_dict:
                letter_dict[input_word[ind]] = {"green": [ind]}
            else:
                letter_dict[input_word[ind]]["green"] += [ind]

        for ind, character in enumerate(input_word_list):
            if character == "_":
                continue
            if character in letter_dict:
                if character not in target_word_list:
                    if "grey" in letter_dict[character]:
                        letter_dict[character]["grey"] += [ind]
                    else:
                        letter_dict[character]["grey"] = [ind]
                else:
                    if "yellow" in letter_dict[character]:
                        letter_dict[character]["yellow"] += [ind]
                    else:
                        letter_dict[character]["yellow"] = [ind]
                    target_word_list[target_word_list.index(character)] = "_"
            else:
                if character not in target_word_list:
                    letter_dict[character] = {"grey": [ind]}
                else:
                    letter_dict[character] = {"yellow": [ind]}
                    target_word_list[target_word_list.index(character)] = "_"
        return letter_dict

    def perform_positional_filtering(self, letter_colors: Dict) -> List[str]:
        """
        Performs the first filtering step based on letter position.

        :param letter_colors: Dict mapping letters to colors to index
        :return: result of positional filter
        """

        ### Sort tuples by index in input word
        indexed_letter_colors = [(word, color, i) for (word, color, index) in _unnest(letter_colors) for i in index]
        indexed_letter_colors.sort(key=lambda tup: tup[2])

        ### Initialize regex as five sections, one for each character in the word
        reg_builder_list = ["."] * 5

        ### Collect uncommon letters
        grey_letters = []
        for character in letter_colors:
            if "grey" in letter_colors[character] and "yellow" not in letter_colors[character]:
                grey_letters.append(character)
        grey_letters = list(set(grey_letters))
        ### Build regex for basic positional filtering
        ### Note that this does not yet account for the presence of yellow letters
        for (letter, color, index) in indexed_letter_colors:
            if color == "green":
                ### Index must be green letter
                reg_builder = letter
            elif color == "yellow":
                ### Index must NOT be grey or yellow letters
                reg_builder = "[^" + "".join(grey_letters + [letter]) + "]"
            elif color == "grey":
                ### Index must NOT be grey letters
                reg_builder = "[^" + "".join(grey_letters if grey_letters else grey_letters + [letter]) + "]"

            reg_builder_list[index] = reg_builder

        ### Perform filter and return result
        regex_string = "".join(reg_builder_list)
        positional_filter_result = list(filter(lambda word: bool(re.search(regex_string, word)), self.corpus))
        return positional_filter_result

    def perform_letter_count_filtering(self, letter_colors: Dict, positional_filter_result: List[str]) -> List[str]:
        """
        Performs the second filtering step based on letter count.

        :param positional_filter_result: list of result of positional filter

        :param letter_colors: Dict mapping letters to colors to index
        :return: result of letter count filter
        """
        letter_count_filter_result = positional_filter_result.copy()

        ### Filter out words without the correct number of letters of green/yellow letters
        for character in letter_colors:
            keep_list = []
            character_count_yellow = 0
            character_count_green = 0
            character_count_grey = 0
            for color in letter_colors[character]:
                if color == "yellow":
                    character_count_yellow += len(letter_colors[character][color])
                elif color == "green":
                    character_count_green += len(letter_colors[character][color])
                elif color == "grey":
                    character_count_grey += len(letter_colors[character][color])

            for word in letter_count_filter_result:
                word_dict = {}
                for letter in word:
                    word_dict[letter] = word_dict.get(letter, 0) + 1
                if character in word_dict:
                    if character_count_yellow > 0 and character_count_green > 0:
                        if character_count_yellow + character_count_green == word_dict[character]:
                            keep_list.append(word)
                    elif character_count_green > 0 and character_count_yellow == 0:
                        if 1 <= character_count_green <= word_dict[character]:
                            keep_list.append(word)
                    elif character_count_yellow > 0 and character_count_green == 0:
                        if character_count_yellow <= word_dict[character]:
                            keep_list.append(word)

            if len(keep_list) >= 1:
                letter_count_filter_result = keep_list
            else:
                letter_count_filter_result = letter_count_filter_result

        return letter_count_filter_result

    def filter_words(self, input_word: str) -> List[str]:
        """
        Filters out all words in corpus based on information from an input word.

        :param input_word: string for filtering against
        :return: filtered corpus
        """
        letter_colors = self.get_letter_colors(input_word)
        positional_filter_result = self.perform_positional_filtering(letter_colors)
        letter_count_filter_result = self.perform_letter_count_filtering(letter_colors, positional_filter_result)
        self.corpus = letter_count_filter_result
        return letter_count_filter_result


if __name__ == "__main__":
    test_filter = Filter("banal", english_dictionary)
    print(test_filter.filter_words("canal"))
