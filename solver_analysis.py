import json
from tqdm import tqdm
from utils.train_utils import solve_all
from utils.utils import english_dictionary
from solvers.Solver import LetterCountWordSimilaritySolver, PositionalSimilarityWordleSolver, MixedWordleSolver

if __name__ == "__main__":
    lcw_solver = LetterCountWordSimilaritySolver(english_dictionary)
    psw_solver = PositionalSimilarityWordleSolver(english_dictionary)
    mix_solver = MixedWordleSolver([psw_solver, lcw_solver])
    solver_dict = {"psw": psw_solver, "mix": mix_solver, "lcw": lcw_solver}
    num_rounds = 6
    results = {}
    for word in tqdm(english_dictionary):
        results[word] = solve_all(solver_dict, num_rounds, english_dictionary, word)
    with open("saved_models/results.json", "w") as f:
        json.dump(results, f)
    f.close()
