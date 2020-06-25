import argparse

import matplotlib.pyplot as plt
import numpy as np
from ridge_map import RidgeMap
import matplotlib.colors as colors
from heightmap import get_image_dims, read_image
import palettable


HEIGHTMAP_FILE = "heightmaps/middle_earth.png"  # input file
OUTPUT_FILE = "output/middle_earth2.png"  # output file

NUM_LINES = 150  # ideal number of lines to include in ridge map
X_RESOLUTION = 1 # "resolution" in x direction (i.e. for resolution 2, 1 in 2 data points are included)

(Y_DIM, X_DIM) = get_image_dims(HEIGHTMAP_FILE)  # use dims from original file
# (y_dim, x_dim) = (1080, 1920) # custom dims

DPI = 96  # DPI of my monitor, use link to find out: https://www.infobyip.com/detectmonitordpi.php
SCALING_FACTOR = 1  # Factor to scale output image by

fig, ax = plt.subplots(figsize=(X_DIM/DPI, Y_DIM/DPI), dpi=DPI)

rm = RidgeMap()

values = read_image(HEIGHTMAP_FILE, NUM_LINES, X_RESOLUTION)

values = rm.preprocess(values=values,
                       water_ntile=20,
                       lake_flatness=2,
                       vertical_ratio=30)

# Function to crop a colormap between two points
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

cmap = palettable.cmocean.sequential.Turbid_3_r.mpl_colormap
new_cmap = truncate_colormap(cmap, 0.3, 0.6)

rm.plot_map(values=values,
            label='',
            label_y=0.2,
            label_x=0.2,
            label_size=20,
            linewidth=1,
            # line_color=np.array([114, 90, 52])/255, # light brown
            # line_color=plt.get_cmap('pink'),
            line_color=new_cmap,
            kind='elevation',
            # background_color=np.array([65, 74, 76])/255, # dark grey
            background_color=np.array([224, 209, 168])/255, # light brown
            # background_color=np.array([114, 90, 52])/255, # dark brown
            # background_color=np.array([243, 243, 243])/255,
            ax=ax)

# Remove margins around image
# Solution found from discussions here: https://stackoverflow.com/questions/11837979/removing-white-space-around-a-saved-image-in-matplotlib
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

plt.savefig(OUTPUT_FILE,
            bbox_inches='tight',
            pad_inches=0,
            dpi=DPI*SCALING_FACTOR)

plt.show()