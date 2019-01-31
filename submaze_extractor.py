import numpy
from numpy.random import randint as rand
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
from copy import deepcopy
from maze_generator import maze

DIM = 10
def extract_submazes(size=3, n=100):
    total_size = DIM - 2
    maze_dict = dict()
    count = 0
    while len(maze_dict) < n and count < 200:
        count += 1
        z = maze(DIM, DIM)
        for i in range(0, total_size - size):
            for j in range(0, total_size - size):
                x = z[i:i + size, j:j + size]
                dfs = run_dfs(x, i, j)
                if dfs is not None:
                    m = to_tuple(x)
                    if m not in maze_dict:
                        maze_dict[m] = dfs
                        
        print("Maze explored:", count, " | SubMazes approved:", len(maze_dict))
                
    return maze_dict


def to_tuple(x):
    l = []
    for r in range(x.shape[0]):
        l.append(tuple(x[r]))
    return tuple(l)


def run_dfs(graph, i=None, j=None, start=(0, 0)):
    size = graph.shape[0]
    if graph[0, 0] == 1 or graph[-1, -1] == 1 or sum(sum(graph)) > size*size-size:
        return None
    visited, stack = set(), [start]
    dfs = []
    exists_path = False
    while stack:
        node = stack.pop()
        if node not in visited:
            dfs.append(node)
            visited.add(node)
            i, j = node
            if i == size-1 and j == size-1:
                exists_path = True
            if j > 0 and not graph[i, j-1]:
                stack.append((i, j-1))
            if i < size-1 and not graph[i+1, j]:
                stack.append((i+1, j))
            if j < size-1 and not graph[i, j+1]:
                stack.append((i, j+1))
            if i > 0 and not graph[i-1, j]:
                stack.append((i-1, j))
    return dfs if exists_path else None

# TODO tuple to array
# TODO plot mazes to check
if __name__ == '__main__':
    maze_dict = extract_submazes(size=3, n=100)
    print(len(maze_dict))

