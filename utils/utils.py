import urllib.request
import re
from typing import List, Dict

english_dictionary = [word for word in urllib.request.urlopen(
    "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt").read().decode().split("\n") if len(word) == 5]


def _check_green(input_word: str, target_word: str) -> List[int]:
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


def color_leters(input_word: str, target_word: str) -> Dict:
    """

    :param input_word: string of word to check
    :param target_word: string of word to check against
    :return: dictionary of color to list of indices
    """
    green_indices = _check_green(input_word, target_word)

    #### color indices
    letter_dict = {}
    input_word_list = list(input_word)
    target_word_list = list(target_word)
    for index in green_indices:
        input_word_list[index] = "_"
        target_word_list[index] = "_"
        if input_word[index] not in letter_dict:
            letter_dict[input_word[index]] = {"green": [index]}
        else:
            letter_dict[input_word[index]]["green"] += [index]

    for ind, character in enumerate(input_word_list):
        if character == "_":
            continue
        if character in letter_dict:
            if character not in target_word_list:
                continue
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


def _unnest(d, keys=[]):
    result = []
    for k, v in d.items():
        if isinstance(v, dict):
            result.extend(_unnest(v, keys + [k]))
        else:
            result.append(tuple(keys + [k, v]))
    return result


def filter_words(input_word: str, target_word: str, corpus: List[str]) -> List[str]:
    """

    :param input_word: string of word to check
    :param target_word: string of word to check against
    :param corpus: list of words to search through
    :return: filtered corpus
    """
    color_checks = color_leters(input_word, target_word)

    color_tuples = [(word, color, index[0]) for (word, color, index) in _unnest(color_checks)]

    reg_builder_list = ["_"] * 5
    ### collect uncommon letters
    grey_letters = []
    for color_tuple in color_tuples:
        if color_tuple[1] == "grey":
            grey_letters.append(color_tuple[0])

    # collect letter which is an extra, but should be yellow for example "anna" vs "banal", the first n in "annal" is extra
    grey_letter_index = []
    for index in range(len(input_word)):
        match = 0
        for color_tuple in color_tuples:
            if color_tuple[2] == index:
                match += 1
                break
        if match == 0:
            grey_letter_index.append((input_word[index], index))

    grey_letters = list(set(grey_letters))

    ## build regex for basic positional filtering
    for index in range(len(input_word)):
        for (character, color, word_index) in color_tuples:
            match = 0
            if index == word_index:
                match += 1
                if color != "green":
                    if color == "grey":
                        reg_builder = "[^" + "".join(grey_letters) + "]"

                    elif color == "yellow":
                        reg_builder = "[^" + "".join(grey_letters + [character]) + "]"
                else:
                    reg_builder = character
            else:
                continue
            if match == 1:
                reg_builder_list[index] = reg_builder
                break
            else:
                reg_builder_list[index] = "[^" + "".join(grey_letters + [input_word[index]]) + "]"

    for (character, index) in grey_letter_index:
        reg_builder_list[index] = "[^" + "".join(grey_letters + [character]) + "]"
    reg_filter = "".join(reg_builder_list)
    match_filter_list = list(filter(lambda word: bool(re.search(reg_filter, word)), corpus))

    ### now filter out words without the correct number of letters of green/yellow vars

    for character in color_checks:
        keep_list = []
        character_count = 0
        for color in color_checks[character]:
            if color != "grey":
                character_count += len(color_checks[character][color])
        for word in match_filter_list:
            word_dict = {}
            for letter in word:
                word_dict[letter] = word_dict.get(letter, 0) + 1
            if character in word_dict:
                if character_count == word_dict[character]:
                    keep_list.append(word)

        if character_count >= 1:
            match_filter_list = keep_list
        else:
            match_filter_list = match_filter_list

    return match_filter_list




if __name__ == "__main__":
    print(filter_words("award", "banal", english_dictionary))
