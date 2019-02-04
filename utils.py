import matplotlib.pyplot as plt
import numpy as np


def plot_maze(Z, pause_time=0.2, cmap=plt.cm.binary):
    plt.imshow(Z, cmap=cmap, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.draw()
    plt.pause(pause_time)
    plt.clf()


def save_plot(Z, path="./maze.png"):
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(path)
    

def visualize_dfs(z, dfs):
    x = np.array(z, copy=True, dtype=float)
    for i, j in dfs:
        x[i, j] = .5
        plot_maze(x, pause_time=.5 / x.shape[0], cmap=plt.cm.Greys)


def to_tuple(x):
    l = []
    for r in range(x.shape[0]):
        l.append(tuple(x[r]))
    return tuple(l)


def to_array(x):
    return np.asarray(x)


def run_dfs(graph, start=(0, 0), unique_CC=False):
    size = graph.shape[0]
    n_ones = sum(sum(graph))
    n_zeros = size * size - n_ones
    
    if graph[0, 0] == 1 or graph[-1, -1] == 1 or n_ones > size * size - size:
        # heuristic to prune DFS
        return None, None, None
    
    visited, stack = set(), [(None, start)]
    edges = set()
    dfs_coordinates = []
    dfs_ids = []
    dfs_edges = []
    exists_path = False
    
    while stack:
        parent, node = stack.pop()
        i, j = node
        p_i, p_j = parent if parent is not None else (0, 0)
        n_id, p_id = i * size + j, p_i * size + p_j
        if node not in visited:
            dfs_coordinates.append(node)
            dfs_ids.append(n_id)
            visited.add(node)
            if parent is not None:
                dfs_edges.append((p_id, n_id))
                edges.update([(p_id, n_id), (n_id, p_id)])
            
            if i == size - 1 and j == size - 1:
                exists_path = True
            if j > 0 and not graph[i, j - 1]:
                stack.append((node, (i, j - 1)))
            if i < size - 1 and not graph[i + 1, j]:
                stack.append((node, (i + 1, j)))
            if j < size - 1 and not graph[i, j + 1]:
                stack.append((node, (i, j + 1)))
            if i > 0 and not graph[i - 1, j]:
                stack.append((node, (i - 1, j)))
        elif (p_id, n_id) not in edges and parent is not None:
            dfs_edges.append((p_id, n_id))
            edges.update([(p_id, n_id), (n_id, p_id)])
    
    if unique_CC:
        is_unique_CC = len(dfs_coordinates) == n_zeros
        # if is_unique_CC:
        #     plot(graph)
        assert not is_unique_CC or exists_path, "unique_CC should imply exists_path"
        return (dfs_coordinates, dfs_ids, dfs_edges) if is_unique_CC else (None, None, None)
    else:
        return (dfs_coordinates, dfs_ids, dfs_edges) if exists_path else (None, None, None)