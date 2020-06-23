import cv2
import numpy as np


def read_image(img_file, num_lines, x_resolution):
    img = cv2.imread(img_file, 0)
    
    height = img.shape[0]

    line_interval = int(height / num_lines)

    image_values = []

    for i in reversed(range(img.shape[0])):
        # if (i % line_interval) == 0 and len(image_values) < num_lines:
        if (i % line_interval) == 0:
            row_values = []
            for j in range(img.shape[1]):
                if (j % x_resolution) == 0:
                    row_values.append(img[i][j])
            image_values.append(row_values)

    return np.array(image_values)

def get_image_dims(img_file):
    img = cv2.imread(img_file, 0)

    return img.shape
