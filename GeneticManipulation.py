
import ConwaysGameOfLife as gol
import numpy as np
import random
import matplotlib.pyplot as plt
import time

GENERATION_SIZE = 60
VERTICAL = "VERTICAL"
HORIZONTAL = "HORIZONTAL"
IN_OUT = "IN_OUT"
SWITCH_RND_RANGE = 1000000
SWITCH_RANGE = 1000000 / 100
PARTITIONS = [
    VERTICAL,
    HORIZONTAL,
    IN_OUT
]
ALPHA = (1 / np.sqrt(2)) # solution to ai * aj = ij - ai * ai

def getNextGen(pool):
    lottery = []
    for i in range(len(pool)):
        increase = int(pool[i].relMaxIncrease)
        lottery += increase * [i]
    
    nextGen = []
    for i in range(GENERATION_SIZE):
        nextGen.append(generateIndividual(pool, lottery))

    return nextGen

def generateIndividual(pool, lottery):
    parent1 = random.choice(lottery)
    parent2 = random.choice(lottery)
    parent1Root = pool[parent1].history[pool[parent1].maxIncreaseStart]
    parent2Root = pool[parent2].history[pool[parent2].maxIncreaseStart]
    child = parent1Root.copy()
    partition =  random.choice(PARTITIONS)
    if partition == VERTICAL:
            for i in range(len(parent2Root)):
                for j in range(int(len(parent2Root[0]) / 2), len(parent2Root[0])):
                    child[i,j] = parent2Root[i, j]

    elif partition == HORIZONTAL:
            for i in range(int(len(parent2Root) / 2), len(parent2Root)):
                for j in range(len(parent2Root[0])):
                    child[i,j] = parent2Root[i, j]

    elif partition == IN_OUT:
            midRows = int(ALPHA * len(parent1Root))
            midCols = int(ALPHA * len(parent1Root[0]))
            startI = int((len(child) - midRows) / 2)
            startJ = int((len(child[0]) - midCols) / 2)
            for i in range(startI, startI + midRows):
                for j in range(startJ, startJ + midCols):
                    child[i, j] = parent2Root[i, j]
    
    else:
            raise Exception("What did you put in that dictionary?")

    for i in range(1, len(child) - 1):
        for j in range(1, len(child[0]) - 1):
            if random.randrange(SWITCH_RND_RANGE) < SWITCH_RANGE:
                child[i, j] = not child[i, j]

    return child

relMaxIncreaseStats = []

pool = []
for i in range(GENERATION_SIZE):
    run = gol.runRandom()
    if type(run) == gol.RunData:
        pool.append(run)

relMaxIncreaseStats.append(np.mean([run.relMaxIncrease for run in pool]))

pool.sort(key=lambda data: data.relMaxIncrease)

for i in range(20):
    nextGen = getNextGen(pool)
    pool = []
    for g in nextGen:
        run = gol.run(g, gol.DEFAULT_ITERATIONS)
        if type(run) == gol.RunData:
            pool.append(run)
    
    
    relMaxIncreaseStats.append( np.mean([run.relMaxIncrease for run in pool]))

best = 0
max = 0
for v in pool:
    if v.relMaxIncrease > max:
        max = v.relMaxIncrease
        best = v

with open("best_configuration", 'w') as file:
    file.write(str(best.history[best.maxIncreaseStart]))

plt.plot(relMaxIncreaseStats)
plt.show()

for i in range(len(best.history)):
    plt.imshow(best.history[i])
    plt.pause(0.25)

#plt.show()
