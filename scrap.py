#! /usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(100,1)

fig, ax = plt.subplots(1,2)
p1 = ax[0].pcolormesh(data)
p2 = ax[1].pcolormesh(data)

plt.colorbar(p1,ax=ax[0])
plt.colorbar(p2,ax=ax[1])

plt.show()
