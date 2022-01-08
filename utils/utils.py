from typing import List

with open("utils/words.txt",'rb') as f:
    english_dictionary = [word for word in f.read().decode().strip().split("\n") if len(word) == 5]
f.close()


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


def _unnest(d, keys=[]):
    result = []
    for k, v in d.items():
        if isinstance(v, dict):
            result.extend(_unnest(v, keys + [k]))
        else:
            result.append(tuple(keys + [k, v]))
    return result
