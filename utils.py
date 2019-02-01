import matplotlib.pyplot as plt
import numpy as np

def plot(Z, pause_time=0.2):
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.draw()
    # plt.pause(0.001)
    plt.pause(pause_time)


def save_plot(Z, path="./maze.png"):
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(path)


def to_tuple(x):
    l = []
    for r in range(x.shape[0]):
        l.append(tuple(x[r]))
    return tuple(l)


def to_array(x):
    return np.asarray(x)