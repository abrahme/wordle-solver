from solvers.Solver import AbstractWordleSolver, LetterCountWordSimilaritySolver, PositionalSimilarityWordleSolver
from typing import Dict
from game import WordleGame


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


if __name__ == "__main__":

    from utils.utils import english_dictionary
    full_corpus = english_dictionary
    wordle_solver = PositionalSimilarityWordleSolver(english_dictionary)
    solutions = {}
    for word in english_dictionary:
        wordle_game = WordleGame(word, 6)

        game_solution = solve_game(wordle_solver, wordle_game)
        print(game_solution)
        solutions[word] = game_solution
        break






