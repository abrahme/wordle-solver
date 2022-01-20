from typing import Dict, List
from game.game import WordleGame
from utils.utils import english_dictionary
from solvers.Solver import AbstractWordleSolver, RandomMethodWordleSolver


def solve_game_wrapper(target_word: str) -> Dict:
    """
    wrapper around solve game method that creates a new game object
    :param target_word:
    :return:
    """
    wordle_game = WordleGame(target_word, 6, english_dictionary)
    solver = RandomMethodWordleSolver()
    return solve_game(solver, wordle_game)


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
