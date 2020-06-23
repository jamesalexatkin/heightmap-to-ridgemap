import argparse

import matplotlib.pyplot as plt
import numpy as np
from ridge_map import RidgeMap

from heightmap import get_image_dims, read_image


heightmap_file = "heightmaps/europe.png"
output_file = "output/europe.png"

num_lines = 80
x_resolution = 2

(y_dim, x_dim) = get_image_dims(heightmap_file)

DPI = 96
SCALING_FACTOR = 1

fig, ax = plt.subplots(figsize=(x_dim/DPI, y_dim/DPI), dpi=DPI)

rm = RidgeMap()

values = read_image(heightmap_file, num_lines, x_resolution)

values=rm.preprocess(values=values,
                    water_ntile=40,
                    lake_flatness=2,
                    vertical_ratio=40)

rm.plot_map(values=values,
            label='',
            label_y=0.2,
            label_x=0.2,
            label_size=20,
            linewidth=1,
            line_color=plt.get_cmap('summer'),
            kind='gradient',
            background_color=np.array([65,74,76])/255,
            ax=ax)

# Remove margins around image
# Solution found from discussions here: https://stackoverflow.com/questions/11837979/removing-white-space-around-a-saved-image-in-matplotlib
# plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0,0)
# plt.gca().xaxis.set_major_locator(plt.NullLocator())
# plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.savefig(output_file, bbox_inches = 'tight',
    pad_inches = 0, dpi=DPI*SCALING_FACTOR)

plt.show()
