#! /usr/bin/env python3

import numpy as np
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc


# force square figure and square axes looks better for polar, IMO
fig = figure(figsize=(8,8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)

N = 1
theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
print (theta)
radii = 10*np.random.rand(N)
radii = [10]
print (radii)
width = np.pi/4*np.random.rand(N)
print(width)
# bars = ax.bar([0], radii, width=width, bottom=0.0)

q = 10
bars = ax.bar(.4, q, width=.3, bottom=0.0)
bars[0].set_facecolor('black')
bars[0].set_alpha(0.5)


show()
