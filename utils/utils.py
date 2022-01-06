from typing import List


def check_green(input_word: str, target_word: str) -> List[int]:
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


def check_yellow(input_word: str, target_word: str) -> List[int]:
    """
    input_word: "balls"
    target_word: "blues"
    output: [0,2,3,4]
    :param input_word: string of word to check
    :param target_word: string of word to check against
    :return: list of which indices are common
    """
    common_indices = []
    for index, character in enumerate(input_word):
        if character in target_word:
            common_indices.append(index)
    return common_indices


def check_grey(input_word: str, target_word: str) -> List[int]:
    """
    returns complement of check_yellow
    input_word: "balls"
    target_word: "blues"
    output: [1]
    :param input_word: string to check
    :param target_word: string to check against
    :return: list of indices are not common
    """
    common_indices = check_yellow(input_word, target_word)
    return list(set(range(len(input_word))).difference(set(common_indices)))


if __name__ == "__main__":
    print(check_grey("banal", "banal"))
    print(check_green("banal", "banal"))
    print(check_yellow("banal", "banal"))
