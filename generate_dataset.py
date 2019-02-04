import numpy as np
import time
import pickle
from numpy.random import randint as rand
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
from copy import deepcopy

from utils import *
from maze_generator import generate_maze


# Generate Datasets with configuration:
# (size, n_mazes, size_source_maze, time_limit)
# CONFIG = [
#     (3, 1000, 15, 60),
#     (4, 2000, 20, 360),
#     (5, 5000, 20, 1200),
#     (7, 10000, 25, 3600),
#     (9, 30000, 25, 3600),
# ]

# Night
CONFIG = [
    (3, 1000, 15, 180),
    (4, 5000, 20, 1200),
    (5, 10000, 20, 3600),
    (7, 500000, 25, 14400),
    (9, 1000000, 25, 28800),
]


def extract_submazes(size=3, n=100, size_source_maze=20, time_limit=1000, unique_CC=False, verbose=False):
    start_time = time.time()
    maze_dict = dict()
    count = 0
    print("Started generating Dataset with maze size: {:.0f}, timelimit: {:.0f}".format(size, time_limit))
    while len(maze_dict) < n and time.time() - start_time < time_limit:
        count += 1
        z = generate_maze(size_source_maze + 2, size_source_maze + 2)
        for i in range(0, size_source_maze - size):
            for j in range(0, size_source_maze - size):
                x = z[i:i + size, j:j + size]
                dfs_coordinates, dfs_ids, dfs_edges = run_dfs(x, unique_CC=unique_CC)
                if dfs_coordinates is not None:
                    m = to_tuple(x)
                    if m not in maze_dict:
                        maze_dict[m] = {
                            "dfs_coordinates": dfs_coordinates,
                            "dfs_ids": dfs_ids,
                            "dfs_edges": dfs_edges,
                        }
        
        if verbose:
            print("Mazes explored:", count, " | SubMazes approved:", len(maze_dict))

    print("Generated Dataset with maze size: {:.0f} | # Mazes: {:.0f} | Time: {:.1f}\n".format(
        size, len(maze_dict), time.time() - start_time)
    )
    return maze_dict


def generate_dataset(size, n, size_source_maze, time_limit=1000, unique_CC=False, verbose=False):
    data = []
    maze_dict = extract_submazes(size, n, size_source_maze, time_limit, unique_CC, verbose)
    for z, dfs in maze_dict.items():
        data.append((to_array(z), dfs))

    with open("./dataset/maze_" + str(size) + ".pickle", 'wb') as pfile:
        pickle.dump(data, pfile, protocol=pickle.HIGHEST_PROTOCOL)
    with open("./dataset/description.txt", 'a') as dfile:
        dfile.write("maze_{:.0f}.pickle | mazes: {:.0f} | size_source_maze: {:.0f} | time_limit: {:.0f} | "
                    "is_unique_CC: {}\n".format(size, len(maze_dict), size_source_maze, time_limit, unique_CC))


def test_extract_submazes():
    maze_dict = extract_submazes(size=9, n=100, size_source_maze=20, time_limit=60, unique_CC=True, verbose=True)
    for z, dfs in maze_dict.items():
        # print(to_array(z))
        plot_maze(to_array(z), pause_time=.5)
    

if __name__ == '__main__':
    np.random.seed(42)
    
    # maze_dict = extract_submazes(size=9, n=100, size_source_maze=20, time_limit=20, unique_CC=True, verbose=True)
    # tot = sum([sum(sum(to_array(x))) for x in maze_dict.keys()])
    
    print("Total experiment time in minutes:", str(sum([time_limit for _, _, _, time_limit in CONFIG])//60))
    
    for params in CONFIG:
        generate_dataset(*params, unique_CC=True, verbose=True)
        

