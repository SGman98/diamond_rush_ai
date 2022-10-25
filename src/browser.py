import numpy as np
import cv2 as cv

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = None


def connect():
    global driver
    driver = webdriver.Firefox()
    driver.get("https://www.miniplay.com/embed/diamond-rush")
    driver.switch_to.frame(driver.find_element("css selector", "iframe"))
    return driver


def select_level(level):
    driver.execute_script(
        f"window.localStorage.setItem('levelToStart','Level {level}')")
    driver.refresh()
    driver.switch_to.frame(driver.find_element("css selector", "iframe"))
    return driver


def get_board():
    canvas = driver.find_element("css selector", "canvas")
    screenshot = canvas.screenshot_as_png
    img = np.frombuffer(screenshot, dtype=np.uint8)
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    return img


def close():
    driver.close()


def move(movements):
    map_moves = {"a": Keys.ARROW_LEFT, "d": Keys.ARROW_RIGHT,
                 "w": Keys.ARROW_UP, "s": Keys.ARROW_DOWN}

    actions = ActionChains(driver)

    for move in movements:
        actions.key_down(map_moves[move]).pause(0.13).perform()
        actions.key_up(map_moves[move]).pause(0.13).perform()
        print(f"Moved {move}")
