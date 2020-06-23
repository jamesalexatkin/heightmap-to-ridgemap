import argparse

import matplotlib.pyplot as plt
import numpy as np
from ridge_map import RidgeMap

from heightmap import get_image_dims, read_image
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


HEIGHTMAP_FILE = "heightmaps/hyrule.png"  # input file
OUTPUT_FILE = "output/hyrule.png"  # output file

NUM_LINES = 100  # ideal number of lines to include in ridge map
X_RESOLUTION = 1 # "resolution" in x direction (i.e. for resolution 2, 1 in 2 data points are included)

(Y_DIM, X_DIM) = get_image_dims(HEIGHTMAP_FILE)  # use dims from original file
# (y_dim, x_dim) = (1080, 1920) # custom dims

DPI = 96  # DPI of my monitor, use link to find out: https://www.infobyip.com/detectmonitordpi.php
SCALING_FACTOR = 2  # Factor to scale output image by

fig, ax = plt.subplots(figsize=(X_DIM/DPI, Y_DIM/DPI), dpi=DPI)

rm = RidgeMap()

values = read_image(HEIGHTMAP_FILE, NUM_LINES, X_RESOLUTION)

values = rm.preprocess(values=values,
                       water_ntile=20,
                       lake_flatness=0,
                       vertical_ratio=40)

# Custom matplotlib colormap for BotW
botw_cmap = LinearSegmentedColormap.from_list("botw", 
                            [np.array([39, 29, 5])/255,                            
                            np.array([64, 51, 21])/255,
                            np.array([93, 82, 40])/255,
                            np.array([140, 131, 100])/255,
                            np.array([157, 152, 124])/255,
                            np.array([166, 161, 133])/255,
                            np.array([186, 185, 163])/255,
                            np.array([203, 202, 182])/255])

rm.plot_map(values=values,
            label='',
            label_y=0.2,
            label_x=0.2,
            label_size=20,
            linewidth=1,
            line_color=botw_cmap,
            size_scale=2,
            kind='elevation',
            background_color=np.array([22, 14, 1])/255,
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