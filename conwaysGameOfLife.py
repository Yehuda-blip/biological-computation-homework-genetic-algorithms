# conway's game of life
from asyncore import loop
import numpy as np
import matplotlib.pyplot as plt
import random

DEFAULT_ITERATIONS = 200
DEFAULT_ROWS = 30
DEFAULT_COLS = 30
STABLIZING_PERIOD = 4

NO_REPEAT = -1
UNSTABLE = -2
TOO_SHORT = -3
CON_DECLINE = -4
INVALID = -5



def start(rows, cols):
    grid = np.full((rows, cols), False)
    gridCpy = np.full((rows, cols), False)
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            grid[i,j] = random.choice([True, False])
    return grid, gridCpy

def gameStep(grid, gridCpy):
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            cellStep(i, j, grid, gridCpy)
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            grid[i,j] = gridCpy[i,j]
    return grid

def cellStep(i, j, grid, gridCpy):
    c = count(i, j, grid)
    if grid[i, j]:
        gridCpy[i, j] = (c == 3 or c == 2)
    else:
        gridCpy[i, j] = (c == 3)

def count(i , j, grid):
    c = 0
    for k in range(-1, 2, 1):
        for l in range(-1, 2, 1):
            if grid[i + k,j + l] and not (k==0 and l == 0):
                c += 1
    return c

def compareHistory(history, current):
    for i in range(len(history)):
        equalIndices = history[i] == current
        if equalIndices.all():
            return i
    
    return NO_REPEAT

def runRandom(iterations = DEFAULT_ITERATIONS, rows = DEFAULT_ROWS, cols = DEFAULT_COLS):
    history = []
    grid, gridCpy = start(rows, cols)
    startConfig = grid.copy()
    history.append(startConfig)
    for i in range(1, iterations):
        nextConfig = gameStep(grid, gridCpy)
        repeatedConfigIndex = compareHistory(history, nextConfig)
        if(repeatedConfigIndex != NO_REPEAT):
            return processGame(history)

        history.append(nextConfig.copy())


    return UNSTABLE, startConfig, history

def run(grid, iterations):
    history = []
    gridCpy = grid.copy()
    startConfig = grid.copy()
    history.append(startConfig)
    for i in range(1, iterations):
        nextConfig = gameStep(grid, gridCpy)
        repeatedConfigIndex = compareHistory(history, nextConfig)
        if(repeatedConfigIndex != NO_REPEAT):
            return processGame(history)

        history.append(nextConfig.copy())


    return UNSTABLE, startConfig, history


class RunData:
    def __init__(self, history, sizes, maxI, minI, maxIncrease, maxIncreaseStart, maxIncreaseEnd, relMaxIncrease):
        self.history = history
        self.sizes = sizes
        self.maxI = maxI
        self.minI = minI
        self.maxIncrease = maxIncrease
        self.maxIncreaseStart = maxIncreaseStart
        self.maxIncreaseEnd = maxIncreaseEnd
        self.relMaxIncrease = relMaxIncrease
        
    
def processGame(history):
    sizes = [np.count_nonzero(c) for c in history]
    maxI = 0
    max = 0
    minI = 0
    min = float('inf')
    maxIncrease = 0
    relMaxIncrease = 0
    maxIncreaseStart = 0
    maxIncreaseEnd = 0

    for i in range(len(sizes)):
        increase = sizes[i] - min
        if increase > maxIncrease:
            maxIncrease = increase
            maxIncreaseStart = minI
            maxIncreaseEnd = i
        if sizes[i] > max:
            max = i
            maxI = i
        if sizes[i] < min:
            min = sizes[i]
            minI = i

    relMaxIncrease = np.count_nonzero(history[maxIncreaseEnd]) / np.max([np.count_nonzero(history[maxIncreaseStart]), 1])

    return RunData(history, sizes, maxI, minI, maxIncrease, maxIncreaseStart, maxIncreaseEnd, relMaxIncrease)
    














# tests
def runRandomTest1():
    res = runRandom(iterations = 500, rows = 7, cols = 7)
    if type(res) == RunData:
        assert(res.maxIncrease >= 0)
        assert(res.maxIncreaseStart <= res.maxIncreaseEnd)
    else:
        assert(res[0] == UNSTABLE)
        assert (len(res[2] == 500)) # assert all iterations were saved

def runRandomTest2():
    res = runRandom(iterations = 5, rows = 7, cols = 7)
    if type(res) == RunData:
        assert(res.maxIncrease >= 0)
        assert(res.maxIncreaseStart <= res.maxIncreaseEnd)
    else:
        assert(res[0] == UNSTABLE)
        assert(len(res[2]) == 5) # assert all iterations were saved


def runRandomTest3():
    res = runRandom(iterations = 5, rows = 7, cols = 7)
    if type(res) == RunData:
        history = res.history
    else:
        history = res[2]
    for c in history:
        for i in range(0, len(c)):
            assert(c[i, 0] == 0)
            assert(c[i, len(c) - 1] == 0)
        for j in range(0, len(c[0])):
            assert(c[0, j] == 0)
            assert(c[len(c[0]) - 1, j] == 0)
        

runRandomTest1()
runRandomTest2()
runRandomTest3()

