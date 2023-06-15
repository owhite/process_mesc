#! /usr/bin/env python3

import sys, getopt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import parse_data # helper script

# {"adc1":740,"ehz":0.161,"error":0,"id":0.197,"iq":0.094,"iqreq":0.000,"TMOS":0.000,"TMOT":0.000,"vbus":72.481,"Vd":1.928,"Vq":0.586},

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
df_scaled = df.copy()

df['phaseA'] = np.sqrt( (df['id'] * df['id']) + (df['iq'] * df['iq']) )

y = the_page['bar_displays']
for item in the_page['bar_displays']:
    max = the_page['max_vals'][item]
    min = the_page['min_vals'][item]
    df_scaled[item] = (df[item] - min) / (max - min) 

data_max_vals = df.max(axis = 0)

data_length = len(df) - 1

bar_width = .8

y = the_page['bar_displays']

# groom these
data_types = {}
for n in the_page['bar_displays']:
    data_types[n] = n
    if n == 'iqreq':
        data_types[n] = 'req'
    if n == 'phaseA':
        data_types[n] = 'amp'

def create_plot(ax, row):
    count = 0
    labels = []
    values = []
    widths = []
    names = []
    for item in the_page['bar_displays']:
        if the_page['bar_displays'][item]:
            widths.append(bar_width)
            names.append(data_types[item])
            values.append(df_scaled[item][row])
            labels.append(int(df[item][row]))
            count = count + 1

    b = ax.bar(names, values, width = widths)
    ax.set(ylabel='', title='', ylim=(0, 1))
    ax.set_axis_off()

    fig.colorbar(b, ax=ax)
    

    rects = ax.patches
    count = 0

    for rect in rects:
        label = labels[count]
        height = rect.get_height() + .02
        ax.text(count, height, label, ha = 'center', fontsize=12)
        ax.text(count, -.1, names[count], ha = 'center', fontsize=12, color = 'black')
        count = count + 1


def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def create_throttle(ax, value):
    # Throttle
    ax.tick_params(axis='y', pad=0, left=True, length=6, width=1, direction='inout')
    rad = np.deg2rad(map_range(value, 740, 3994, -30, 90))
    ax.set_xticklabels(['', '',])
    ax.set_rticks([])
    ax.set_thetamin(90)
    ax.set_thetamax(-30)
    ax.grid(False)
    ax.plot([rad,rad], [0,1], color="black", linewidth=2)
    ax.set_title("Spread")
    
fig = plt.figure()
fig.set_figheight(7)
fig.set_figwidth(3)
ax1 = plt.subplot2grid(shape=(2, 2), loc=(0, 0), colspan=2)
ax2 = plt.subplot2grid(shape=(2, 2), loc=(1, 0), colspan=1, polar=True)

create_plot(ax1, 133)
create_throttle(ax2, df['adc1'][133])

# n =  "image{:05d}.png".format(row)
# print (row, data_length, n)
# fig.savefig(n, transparent = True)

plt.show()
