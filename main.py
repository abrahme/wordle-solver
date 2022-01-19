import json
from tqdm import tqdm
from typing import Dict, List
from game.game import WordleGame
from utils.utils import english_dictionary
from solvers.Solver import AbstractWordleSolver, \
    LetterCountWordSimilaritySolver, PositionalSimilarityWordleSolver, MixedWordleSolver


def solve_game(solver: AbstractWordleSolver, game_object: WordleGame) -> Dict:
    """
    :param solver: a type of solver which picks words
    :param game_object: a wordle initiated game
    :return: dictionary of status of game after done playing
    """
    game_dict = {}
    round_dict = {}
    while not game_object.game_over:
        guess_no = game_object.rounds
        guess = solver.choose_word(game_object.corpus)
        game_object.play_round(guess)
        round_dict[guess_no] = guess
    game_dict["solved"] = game_object.won
    game_dict["round_results"] = round_dict
    return game_dict


def solve_all(solvers: Dict, rounds: int, dictionary: List[str], target_word: str) -> Dict:
    """

    :param solvers: dictionary mapping solver name (str) to solver
    :param rounds: integer for num rounds to play
    :param dictionary: list ofwords to play with
    :param target_word: word to try and guess
    :return:
    """
    word_results = {}
    for solver in solvers:
        wordle_game = WordleGame(target_word, rounds, dictionary)
        solver_results = solve_game(solvers[solver], wordle_game)
        word_results[solver] = solver_results
    return word_results


if __name__ == "__main__":
    lcw_solver = LetterCountWordSimilaritySolver(english_dictionary)
    psw_solver = PositionalSimilarityWordleSolver(english_dictionary)
    mix_solver = MixedWordleSolver([psw_solver, lcw_solver])
    solver_dict = {"psw": psw_solver, "mix": mix_solver, "lcw": lcw_solver}
    num_rounds = 6
    results = {}
    for word in tqdm(english_dictionary):
        results[word] = solve_all(solver_dict, num_rounds, english_dictionary, word)

    with open("saved_models/results.json","w") as f:
        json.dump(results,f)
    f.close()
