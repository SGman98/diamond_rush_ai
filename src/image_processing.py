import cv2 as cv
import numpy as np
import os

from tkinter import filedialog


def get_image(name):
    name = os.path.join(os.path.dirname(__file__), "..", "images", name)
    return cv.imread(name)


def show_image(image):
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def crop_img(image, cols, rows, top=0, bottom=0, left=0, right=0):
    height, width = image.shape[:2]
    tile_width = width / cols
    tile_height = height / rows
    # remove top and bottom
    image = image[int(top * tile_height):int((rows - bottom) * tile_height), :]
    # remove left and right
    image = image[:, int(left * tile_width):int((cols - right) * tile_width)]

    return image
