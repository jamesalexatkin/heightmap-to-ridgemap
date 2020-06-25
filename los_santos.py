import argparse

import matplotlib.pyplot as plt
import numpy as np
from ridge_map import RidgeMap

from heightmap import get_image_dims, read_image


HEIGHTMAP_FILE = "heightmaps/los_santos.png"  # input file
OUTPUT_FILE = "output/los_santos_desktop.png"  # output file

NUM_LINES = 80  # ideal number of lines to include in ridge map
X_RESOLUTION = 2 # "resolution" in x direction (i.e. for resolution 2, 1 in 2 data points are included)

# (Y_DIM, X_DIM) = get_image_dims(HEIGHTMAP_FILE)  # use dims from original file
(Y_DIM, X_DIM) = (824, 824) # custom dims

DPI = 96  # DPI of my monitor, use link to find out: https://www.infobyip.com/detectmonitordpi.php
SCALING_FACTOR = 1  # Factor to scale output image by

fig, ax = plt.subplots(figsize=(X_DIM/DPI, Y_DIM/DPI), dpi=DPI)

rm = RidgeMap()

values = read_image(HEIGHTMAP_FILE, NUM_LINES, X_RESOLUTION)

values = rm.preprocess(values=values,
                       water_ntile=40,
                       lake_flatness=2,
                       vertical_ratio=40)

rm.plot_map(values=values,
            label='',
            label_y=0.2,
            label_x=0.2,
            label_size=20,
            linewidth=2,
            line_color=plt.get_cmap('cool'),
            kind='gradient',
            background_color=np.array([65, 74, 76])/255,
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