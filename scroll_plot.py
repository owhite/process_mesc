#! /usr/bin/env python3

import sys, getopt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import parse_data # helper script
import random
import time


try:
    opts, args = getopt.getopt(sys.argv[1:],"i:",["ifile="])
except getopt.GetoptError:
    print ('program.py -i <inputfile>')
    sys.exit(2)

fname = ""

for opt, arg in opts:
    if opt in ("-i", "--infile"):
        fname = arg

the_page = parse_data.get_json_file(fname)
title = the_page['title']

data = parse_data.make_frame(the_page['data'])
df = pd.DataFrame(data)

# {"adc1":740,"ehz":0.161,"error":0,"id":0.197,"iq":0.094,"iqreq":0.000,"TMOS":0.000,"TMOT":0.000,"vbus":72.481,"Vd":1.928,"Vq":0.586},

df['phaseA'] = np.sqrt( (df['id'] * df['id']) + (df['iq'] * df['iq']) )

t = np.arange(len(df['ehz']))

fig, host = plt.subplots(figsize=(14,5))
fig.subplots_adjust(right=0.75)
ax1 = host.twinx()
ax2 = host.twinx()
ax3 = host.twinx()
ax2.spines.right.set_position(("axes", 1.1))
ax3.spines.right.set_position(("axes", 1.2))

fig.suptitle(title, fontsize=16)
color = 'tab:red'
host.set_ylim(0, 740)
host.set_xlabel("Samples", color='black')
host.tick_params(axis='y', labelcolor=color)
host.set_ylabel("ehz", color=color)
host.plot(t, df['ehz'], color=color, label = 'ehz')
fig.legend(loc = "upper left")

color = 'tab:blue'
datatype = 'phaseA'
ax1.set_ylabel(datatype, color=color)  
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 300)
ax1.plot(t, df[datatype], color=color, label = datatype)
fig.legend(loc = "upper left")

datatype = 'iqreq'
color = 'tab:green'
ax2.set_ylabel(datatype, color=color)  
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 400)
ax2.plot(t, df[datatype], color=color, label = datatype)
fig.legend(loc = "upper left")

datatype = 'adc1'
color = 'black'
ax3.set_ylabel(datatype, color=color)  
ax3.tick_params(axis='y', labelcolor=color)
ax3.set_ylim(700, 4200)
ax3.plot(t, df[datatype], color=color, label = datatype)
fig.legend(loc = "upper left")

np.random.seed(19680801)

# Compute areas and colors
N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 200 * r**2
colors = theta

ax5 = fig.add_axes([0.1, 0.6, 0.20, 0.20], polar=True)
ax5.set_rticks([])
ax5.set_thetamin(-30)
ax5.set_thetamax(30)
ax5.grid(False)
ax5.tick_params(axis='y', pad=0, left=True, length=6, width=1, direction='inout')

def animate(i,vl, t2, axis):
    degree = random.randint(-30, 30)
    rad = np.deg2rad(degree)
    axis.clear() # each time this is called you have to reset everything else: ticks, etc. 
    ax5.set_rticks([])
    ax5.set_thetamin(-30)
    ax5.set_thetamax(30)
    ax5.grid(False)
    axis.plot([rad,rad], [0,1], color="black", linewidth=2)

    vl.set_xdata([i,i])
    # interval is in millisecs, and seems to be working okay
    #  to test, uncomment:
    # print (int((time.perf_counter() - t2) * 100))
    return vl,

vl = ax1.axvline(0, ls='-', color='r', lw=1, zorder=10)

# number of rows of data we got
frames = len(df['ehz']) # should be generalized, not ehz
freq = 10 # Hz

start = time.perf_counter()

ani = animation.FuncAnimation(fig, animate, frames=frames, fargs=(vl, start, ax5), interval=100) 

plt.show()
