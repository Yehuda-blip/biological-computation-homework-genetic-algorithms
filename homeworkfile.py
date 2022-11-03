import numpy as np
import ConwaysGameOfLife as gol
import matplotlib.pyplot as plt
config = np.asarray(
[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
)

res = gol.run(config, gol.DEFAULT_ITERATIONS)

for i in range(len(res.history)):
    plt.imshow(res.history[i])
    plt.pause(0.25)
