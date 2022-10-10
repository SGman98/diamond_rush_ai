import cv2 as cv
import numpy as np

from tkinter import filedialog


def get_image():
    return cv.imread(filedialog.askopenfilename())


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
