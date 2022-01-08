from solvers.Solver import AbstractWordleSolver, RandomMethodWordleSolver
from typing import Dict
from game import WordleGame


def solve_game(solver: AbstractWordleSolver, game_object: WordleGame) -> Dict:
    """

    :param solver: a type of solver which picks words
    :param game_object: a wordle initiated game
    :return: dictionary of status of game after done playing
    """
    game_dict = {}
    while not game_object.game_over:
        guess_no = game_object.rounds
        guess = solver.choose_word(game_object.corpus)
        game_object.play_round(guess)
        game_dict[guess_no] = guess
    game_dict["solved"] = game_object.won
    return game_dict


if __name__ == "__main__":
    wordle_game = WordleGame("slump",6)
    wordle_solver = RandomMethodWordleSolver()
    print(solve_game(wordle_solver, wordle_game))
