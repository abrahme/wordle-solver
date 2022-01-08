import re

from collections import defaultdict
from utils.common import NUM_LETTERS, COLORS
from typing import List, Dict

def __check_green(input_word: str, target_word: str) -> List[int]:
    """
    input_word: "balls"
    target_word: "blues"
    output: [0,4]
    :param input_word: string of word to check
    :param target_word: string of word to check against
    :return: list of where letters match along index for the input word
    """
    match_index = []
    for index, character in enumerate(input_word):
        if character == target_word[index]:
            match_index.append(index)
    return match_index


def get_letter_colors(input_word: str, target_word: str) -> Dict:
    """

    :param input_word: string of word to check
    :param target_word: string of word to check against
    :return: dictionary of letter to color to list of indices
    """
    green_indices = __check_green(input_word, target_word)

    #### color indices
    letter_dict = {}
    input_word_list = list(input_word)
    target_word_list = list(target_word)
    for index in green_indices:
        input_word_list[index] = "_"
        target_word_list[index] = "_"
        if input_word[index] not in letter_dict:
            letter_dict[input_word[index]] = {COLORS.green : [index]}
        else:
            letter_dict[input_word[index]][COLORS.green] += [index]

    for ind, character in enumerate(input_word_list):
        if character == "_":
            continue
        if character in letter_dict:
            if character not in target_word_list:
                if COLORS.grey in letter_dict[character]:
                    letter_dict[character][COLORS.grey] += [ind]
                else:
                    letter_dict[character][COLORS.grey] = [ind]
            else:
                if COLORS.yellow in letter_dict[character]:
                    letter_dict[character][COLORS.yellow] += [ind]
                else:
                    letter_dict[character][COLORS.yellow] = [ind]
                target_word_list[target_word_list.index(character)] = "_"
        else:
            if character not in target_word_list:
                letter_dict[character] = {COLORS.grey: [ind]}
            else:
                letter_dict[character] = {COLORS.yellow: [ind]}
                target_word_list[target_word_list.index(character)] = "_"
    return letter_dict


def _unnest(d, keys=[]):
    result = []
    for k, v in d.items():
        if isinstance(v, dict):
            result.extend(_unnest(v, keys + [k]))
        else:
            result.append(tuple(keys + [k, v]))
    return result
