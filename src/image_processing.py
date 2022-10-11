import cv2 as cv
import numpy as np
import os

from tkinter import filedialog


def get_image(name=None):
    if name is None:
        name = filedialog.askopenfilename()
    else:
        name = os.path.join(os.path.dirname(__file__), "..", "images", name)

    return cv.imread(name)


def show_image(image):
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def crop_black_borders(image):
    # apply filters
    blurred = cv.blur(image, (3, 3))
    canny = cv.Canny(blurred, 100, 200)

    # find the non-zero min-max coords of canny
    pts = np.argwhere(canny > 0)
    y1, x1 = pts.min(axis=0)
    y2, x2 = pts.max(axis=0)

    return image[y1:y2, x1:x2]


def crop_img(image, cols, rows, top=0, bottom=0, left=0, right=0):
    height, width = image.shape[:2]
    tile_width = width / cols
    tile_height = height / rows
    # remove top and bottom
    image = image[int(top * tile_height):int((rows - bottom) * tile_height), :]
    # remove left and right
    image = image[:, int(left * tile_width):int((cols - right) * tile_width)]

    return image
