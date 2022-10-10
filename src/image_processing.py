import cv2 as cv

from tkinter import filedialog


def get_image():
    return cv.imread(filedialog.askopenfilename())


def show_image(image):
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()
