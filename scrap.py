#! /usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize = (1,4))

array = []
for i in np.arange(0, 1, .04):
    x = []
    x=[i]
    array.append(x)

cmap=plt.cm.jet
plt.pcolormesh(array , cmap = cmap )

plt.show()

