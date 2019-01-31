import numpy
from numpy.random import randint as rand
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt


def maze(width=51, height=51, complexity=1., density=10, intermediate_plots=False, fig=None):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))  # number of components
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))  # size of components
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    
    if intermediate_plots:
        fig = plt.figure(figsize=(5, 5))
    
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2  # pick a random position
        # print(x, y)
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
                    if intermediate_plots:
                        plot(Z)
    
    return Z[1:-1, 1:-1]
    # return Z


def plot(Z):
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.draw()
    # plt.pause(0.001)
    plt.pause(1)


def plot_save(Z):
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.savefig("./maze.png")


def experiment_maze(n):
    fig = plt.figure(figsize=(5, 5))
    for i in range(n):
        Z = maze(10, 10)
        plot(Z, fig)
    return


if __name__ == '__main__':
    # experiment_maze(1)
    Z = maze(40, 40)
    plot_save(Z)
