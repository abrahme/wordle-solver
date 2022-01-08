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
        # print(guess)
        game_object.play_round(guess)
        game_dict[guess_no] = guess
    game_dict["solved"] = game_object.won
    return game_dict


if __name__ == "__main__":

    simulation_results = []
    num_simulations = 100000
    solved = 0
    path_length = []
    for _ in range(num_simulations):
        wordle_game = WordleGame("ladle", 6)
        wordle_solver = RandomMethodWordleSolver()
        game_solution = solve_game(wordle_solver, wordle_game)
        if game_solution["solved"]:
            solved += 1
        path_length.append(len(game_solution)-1)
        simulation_results.append(game_solution)

    print(f"Percentage solved: {solved/num_simulations}")
    print(f"Average path length: {sum(path_length)/num_simulations}")


