import multiprocessing
import time
import argparse
from multiprocessing.pool import Pool
from utils.train_utils import solve_game_wrapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play Wordle')
    parser.add_argument("--word", type=str, action="store")
    parser.add_argument("--num_trials", type=int, action="store")

    args = parser.parse_args()
    trials = args.num_trials
    word = args.word
    print(f"Target word is {word}")
    print(f"We will simulate {trials} trials")
    words = [word] * trials
    cpus = multiprocessing.cpu_count()
    print(f"There are {cpus} cpus")
    p = Pool(cpus - 1)
    start = time.time()
    results = p.map(solve_game_wrapper, words)
    p.close()
    p.join()
    end = time.time()
    print(results)
    print(f"That took {end - start} seconds")
