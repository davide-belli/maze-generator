import pickle
import numpy as np
import matplotlib
matplotlib.use("Qt5agg")
import matplotlib.pyplot as plt

from utils import *


SIZE = 4
DFS = False
DFS = True


if __name__ == '__main__':
    size = SIZE
    
    with open("./dataset/maze_" + str(size) + ".pickle", "rb") as input_file:
        dataset = pickle.load(input_file)
    
    for datapoint in dataset:
        z, dfs = datapoint
        plot_maze(z, pause_time=.5)
        
        plot_dfs = DFS
        if plot_dfs:
            visualize_dfs(z, dfs["dfs_coordinates"])

