import numpy as np
import cv2 as cv

from selenium import webdriver

driver = webdriver.Firefox()


def connect():
    driver.get("https://www.miniplay.com/embed/diamond-rush")
    driver.switch_to.frame(driver.find_element("css selector", "iframe"))


def remove_help():
    driver.execute_script("window.localStorage.setItem('isNewPlayer','false')")
    driver.refresh()
    driver.switch_to.frame(driver.find_element("css selector", "iframe"))


def get_board():
    canvas = driver.find_element("css selector", "canvas")
    screenshot = canvas.screenshot_as_png
    img = np.frombuffer(screenshot, dtype=np.uint8)
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    return img


def close():
    driver.close()
