from cv2 import cv2 as cv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils import UP, DOWN, LEFT, RIGHT


class Browser:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.miniplay.com/embed/diamond-rush")

        iframe = self.driver.find_element("css selector", "iframe")
        self.driver.switch_to.frame(iframe)

        self.map_moves = {
            UP: Keys.ARROW_UP,
            DOWN: Keys.ARROW_DOWN,
            LEFT: Keys.ARROW_LEFT,
            RIGHT: Keys.ARROW_RIGHT,
        }

    def close(self):
        self.driver.close()

    def select_level(self, level):
        script = f"window.localStorage.setItem('levelToStart','Level {level}')"
        self.driver.execute_script(script)
        self.driver.refresh()

        iframe = self.driver.find_element("css selector", "iframe")
        self.driver.switch_to.frame(iframe)

    def move(self, movements):
        actions = ActionChains(self.driver)

        for move in movements:
            move = self.map_moves[move]
            actions.key_down(move).pause(0.13).perform()
            actions.key_up(move).pause(0.13).perform()

    def get_board(self):
        canvas = self.driver.find_element("css selector", "canvas")
        screenshot = canvas.screenshot_as_png
        img = np.frombuffer(screenshot, dtype=np.uint8)
        img = cv.imdecode(img, cv.IMREAD_COLOR)
        return img

    def unlock_all_levels(self):
        script = "window.localStorage.setItem('isNewPlayer','false')"
        self.driver.execute_script(script)

        for i in range(1, 20):
            script = f"window.localStorage.setItem('Level {i}','passed')"
            self.driver.execute_script(script)
        self.driver.refresh()

        iframe = self.driver.find_element("css selector", "iframe")
        self.driver.switch_to.frame(iframe)
