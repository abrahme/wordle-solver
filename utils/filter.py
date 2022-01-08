import re

from utils.common import NUM_LETTERS, COLORS
from utils.utils import get_letter_colors, _unnest
from typing import List, Dict

class Filter(object):
    def __init__(self, target_word: str, corpus: List[str]):
	    self.target_word = target_word
	    self.corpus = corpus

    def perform_positional_filtering(self, letter_colors: Dict) -> List[str]:
	    """
	    Performs the first filtering step based on letter position.

	    :param letter_colors: Dict mapping letters to colors to index
	    :return: result of positional filter
	    """

	    ### Sort tuples by index in input word
	    indexed_letter_colors = [(word, color, i) for (word, color, index) in _unnest(letter_colors) for i in index]
	    indexed_letter_colors.sort(key=lambda tup: tup[2])

	    ### Initialize regex as NUM_LETTERS sections, one for each character in the word
	    reg_builder_list = ["."] * NUM_LETTERS

	    ### Collect uncommon letters
	    grey_letters = []
	    for (character, color, _) in indexed_letter_colors:
	        if color == COLORS.grey:
	            grey_letters.append(character)
	    grey_letters = list(set(grey_letters))

	    ### Build regex for basic positional filtering
	    ### Note that this does not yet account for the presence of yellow letters
	    for (letter, color, index) in indexed_letter_colors:
	        if color == COLORS.green:
	        	### Index must be green letter
	        	reg_builder = letter
	        elif color == COLORS.yellow:
	        	### Index must NOT be grey or yellow letters
	        	reg_builder = "[^" + "".join(grey_letters + [letter]) + "]"
	        else:
	        	### Index must NOT be grey letters
	            reg_builder = "[^" + "".join(grey_letters) + "]"

	        reg_builder_list[index] = reg_builder

	    ### Perform filter and return result
	    regex_string = "".join(reg_builder_list)
	    positional_filter_result = list(filter(lambda word: bool(re.search(regex_string, word)), self.corpus))
	    return positional_filter_result

    def perform_letter_count_filtering(self, letter_colors: Dict, positional_filter_result: List[str]) -> List[str]:
	    """
	    Performs the second filtering step based on letter count.

	    :param letter_colors: Dict mapping letters to colors to index
	    :return: result of letter count filter
	    """
	    letter_count_filter_result = positional_filter_result.copy()

	    ### Filter out words without the correct number of letters of green/yellow letters
	    for character in letter_colors:
	        keep_list = []
	        character_count = 0
	        for color in letter_colors[character]:
	            if color != COLORS.grey:
	                character_count += len(letter_colors[character][color])
	        for word in letter_count_filter_result:
	            word_dict = {}
	            for letter in word:
	                word_dict[letter] = word_dict.get(letter, 0) + 1
	            if character in word_dict:
	                if character_count == word_dict[character]:
	                    keep_list.append(word)

	        if character_count >= 1:
	            letter_count_filter_result = keep_list
	        else:
	            letter_count_filter_result = letter_count_filter_result

	    return letter_count_filter_result

    def filter_words(self, letter_colors: Dict) -> List[str]:
	    """
	    Filters out all words in corpus based on information from an input word.

	    :param letter_colors: Dict mapping letters to colors to index of input word
	    :return: filtered corpus
	    """
	    positional_filter_result = self.perform_positional_filtering(letter_colors)
	    letter_count_filter_result = self.perform_letter_count_filtering(letter_colors, positional_filter_result)
	    self.corpus = letter_count_filter_result
	    return letter_count_filter_result

if __name__ == "__main__":
	test_filter = Filter("banal")
	print(test_filter.filter_words("alarm"))




