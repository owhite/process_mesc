#! /usr/bin/env python3

import moviepy.editor as mp
import sys, getopt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
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
mname = the_page['movie']
start_sec = the_page['start_sec']
data_collection_period = the_page['data_collection_period']

data = parse_data.make_frame(the_page['data'])

video = mp.VideoFileClip(mname)
duration = video.duration
fps = video.fps

data = parse_data.pad_data_set(data, data_collection_period, start_sec, duration)

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

def create_bargraph(ax, row, place_box):
    labels = []
    values = []
    widths = []
    names = []
    count = 0
    ax.clear() 
    for item in the_page['bar_displays']:
        if the_page['bar_displays'][item]:
            widths.append(bar_width)
            names.append(data_types[item])
            values.append(df_scaled[item][row])
            labels.append(int(df[item][row]))
            count = count + 1

    b = ax.bar(names, values, width = widths, color = 'black', edgecolor='yellow', linewidth=3)
    ax.set(ylabel='', title='', ylim=(0, 1))
    ax.set_axis_off()

    rects = ax.patches
    count = 0
    for rect in rects:
        label = labels[count]
        height = rect.get_height() + .02
        ax.text(count, height, label, ha = 'center', fontsize=12)
        ax.text(count, -.1, names[count], ha = 'center', fontsize=12, color = 'black')
        count = count + 1
    if place_box:
        bound_box(ax)


def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def create_throttle(ax, value, place_box):
    rad = np.deg2rad(map_range(value, 740, 3994, -30, 90))
    ax.set_theta_zero_location('SE')
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.set_rticks([])
    ax.set_thetamin(120)
    ax.set_thetamax(0)
    ax.grid(False)
    q = 20
    bars = ax.bar(rad/2, q, width=rad, color='red')

    # ax.plot([rad,rad], [0,1], color='black', linewidth=2)
    ax.set_title("Throttle")
    if place_box:
        bound_box(ax)
    
def create_temp(ax, temp, min, max, place_box):
    array = []
    rows = 25
    for i in np.arange(0, 1, 1 / rows):
        x = []
        x=[i]
        array.append(x)

    cmap=plt.cm.jet

    ax.set_yticks((0, rows))
    ax.set_yticklabels((min, max))

    p = map_range(temp, min, max, 0, rows)

    ax.pcolor(array , cmap = cmap )
    t = ax.text(-0.1, p, " ",
                ha="center", va="center", rotation=0, size=10,
                bbox=dict(boxstyle="rarrow,pad=0.3",
                          fc="lightblue", ec="steelblue", lw=2))   
    ax.set_title('MOS')
    ax.xaxis.set_tick_params(labelbottom=False)
    if place_box:
        bound_box(ax)


def create_elevation(ax, value, place_box):
    rad = np.deg2rad(value)
    ax.set_theta_zero_location('E')
    # ax.xaxis.set_tick_params(labelbottom=False)
    ax.set_rticks([])
    ax.set_thetamin(30)
    ax.set_thetamax(-30)
    ax.grid(False)
    ax.plot([rad,rad], [0,1], color="black", linewidth=2)
    ax.set_title("Elevation")
    if place_box:
        bound_box(ax)

def bound_box(ax):
    bbox = ax.get_tightbbox(fig.canvas.get_renderer())
    x0, y0, width, height = bbox.transformed(fig.transFigure.inverted()).bounds
    # slightly increase the very tight bounds:
    xpad = 0.05 * width
    ypad = 0.05 * height
    fig.add_artist(plt.Rectangle((x0-xpad, y0-ypad), width+2*xpad, height+2*ypad, edgecolor='red', linewidth=3, fill=False))

def animate(i, total, a0, a1, a2, a3, show_box):
    print(i, total)
    # create_bargraph(a0, i, show)
    # create_temp(a1, 75, the_page['min_temp'], the_page['max_temp'], show)
    # create_throttle(a2, df['adc1'][i], show)
    # create_elevation(a3, 20, show)

fig = plt.figure()
fig.set_figheight(7)
fig.set_figwidth(4)

gs = gridspec.GridSpec(ncols=3, nrows=2,
                         width_ratios=[10, 10, 3], wspace=.5, hspace = .5,
                         height_ratios=[3, 1])

ax0 = fig.add_subplot(gs[0,:-1])
ax1 = fig.add_subplot(gs[0,2])
ax2 = fig.add_subplot(gs[1,0], polar=True)
ax3 = fig.add_subplot(gs[1,1], polar=True)

show = False

key = list(data.keys())[0]
frames = len(data[key])

ani = animation.FuncAnimation(fig, animate, frames=frames,
                              fargs=(frames, ax0, ax1, ax2, ax3, show),
                              interval=100, repeat=False) 

# writervideo = animation.FFMpegWriter(fps=60)
# ani.save('dummy.mp4', writer=writervideo)
plt.show()
plt.close()

