# conway's game of life
from asyncore import loop
import numpy as np
import matplotlib.pyplot as plt
import random

DEFAULT_ITERATIONS = 500
DEFAULT_ROWS = 3
DEFAULT_COLS = 3
STABLIZING_PERIOD = 4

NO_REPEAT = -1
UNSTABLE = -2
TOO_SHORT = -3
CON_DECLINE = -4
INVALID = -5


class RunData:
    def extractMinBeforeMax(self, history, maxSizeI):
        min = float('inf')
        minIndex = 0
        for i in range(maxSizeI):
            curr = np.count_nonzero(history[i])
            if min > curr:
                min = curr
                minIndex = i

        return minIndex if np.count_nonzero(history[0]) < np.count_nonzero(history[maxSizeI]) else CON_DECLINE

    def __init__(self, history, repeatI, maxSizeI, minSizeI):
        self.maxSizeI = maxSizeI
        self.minSizeI = minSizeI
        self.maxSize = np.count_nonzero(history[maxSizeI])
        self.minSize = np.count_nonzero(history[minSizeI])
        self.runLength = len(history)
        self.runLengthTillLoop = repeatI
        self.loopLength = len(history) - repeatI - 1
        self.loopConfig = history[repeatI]
        self.startConfig = history[0]
        self.endConfig = history[-1]
        self.minSizeConfig = history[minSizeI]
        self.maxSizeConfig = history[maxSizeI]
        self.minSizeBeforeMaxI = minSizeI if minSizeI < maxSizeI else self.extractMinBeforeMax(history, maxSizeI)
        self.minSizeConfigBeforeMax = history[self.minSizeBeforeMaxI] if self.minSizeBeforeMaxI != CON_DECLINE else CON_DECLINE
        self.minSizeBeforeMax = np.count_nonzero(history[self.minSizeBeforeMaxI]) if self.minSizeBeforeMaxI != CON_DECLINE else CON_DECLINE
        self.increaseTime = maxSizeI - self.minSizeBeforeMaxI if self.minSizeBeforeMaxI != CON_DECLINE else CON_DECLINE
        self.increaseVolume = np.count_nonzero(self.maxSizeConfig) - np.count_nonzero(self.minSizeConfigBeforeMax) if self.minSizeBeforeMaxI != CON_DECLINE else CON_DECLINE
        self.sizes = [np.count_nonzero(c) for c in history]



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
    maxSize = 0
    maxSizeIndex = 0
    minSize = float('inf')
    minSizeIndex = 0
    for i in range(1, iterations):
        nextConfig = gameStep(grid, gridCpy)
        len = np.count_nonzero(nextConfig)
        if i > STABLIZING_PERIOD:
            if maxSize < len:
                maxSize = len
                maxSizeIndex = i
            if minSize > len:
                minSize = len
                minSizeIndex = i
        repeatedConfigIndex = compareHistory(history, nextConfig)
        if(repeatedConfigIndex != NO_REPEAT):
            if(i > STABLIZING_PERIOD):
                return RunData(history, repeatedConfigIndex, maxSizeIndex, minSizeIndex)
            else:
                return TOO_SHORT, startConfig, history
        history.append(nextConfig.copy())


    return UNSTABLE, startConfig, history
    
















res = runRandom(iterations = 500, rows = 7, cols = 7)

# tests
def runRandomTest1():
    res = runRandom(iterations = 500, rows = 7, cols = 7)
    if type(res) == RunData:
        assert(res.maxSizeI > STABLIZING_PERIOD or res.maxSizeI == 0)
        assert(res.minSizeI > STABLIZING_PERIOD or res.minSizeI == 0)
        assert(np.count_nonzero(res.maxSizeConfig) > 0 or res.maxSizeI == 0)
        assert(np.count_nonzero(res.minSizeConfig) < float('inf')or res.minSizeI == 0)
        if res.minSizeBeforeMaxI != CON_DECLINE:
            assert(np.count_nonzero(res.minSizeConfigBeforeMax) <= np.count_nonzero(res.maxSizeConfig))
            assert(np.count_nonzero(res.minSizeConfigBeforeMax) <= np.count_nonzero(res.minSizeConfigBeforeMax))
            assert(res.increaseTime >= 0)
            assert(res.increaseVolume >= 0)

def runRandomTest2():
    res = runRandom(iterations = 500, rows = 7, cols = 7)
    if type(res) == RunData:
        endCnf = res.endConfig.copy()
        endCnfCpy = res.endConfig.copy()
        for i in range(res.loopLength):
            nextCnf = gameStep(endCnf, endCnfCpy)
        assert((nextCnf == res.loopConfig).all())

def runRandomTest3():
    res = runRandom(iterations = 20, rows = 20, cols = 20)
    if type(res) != RunData:
        assert(res[0] == UNSTABLE or (res[0] == TOO_SHORT and len(res[2]) < STABLIZING_PERIOD))

        

runRandomTest1()
runRandomTest2()
runRandomTest3()






# main
pool = []
for i in range(60):
    run = runRandom()
    if type(run) == RunData:
        pool.append()

pool.sort(key=lambda data: data.increaseVolume)
for v in pool:
    print (v.increaseVolume)
    plt.imshow(v.minSizeConfig)
    plt.imshow(v.maxSizeConfig)

