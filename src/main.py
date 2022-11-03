import time

import ai
import image_processing as img_proc
from browser import Browser


def start_game(lvl, browser):
    browser.select_level(lvl)

    time.sleep(3)

    board = browser.get_board()
    result = img_proc.process_board(board)

    movement = ai.get_movement_from_array(result)
    browser.move(movement)


def main():
    browser = Browser()

    while True:
        user_input = input("Select level (1-20) or (q)uit: ")

        if user_input == "q":
            break

        if not user_input.isdigit():
            print("Invalid input")
            continue

        user_input = int(user_input)

        if user_input not in range(1, 21):
            print("Invalid level")
            continue

        start_game(user_input, browser)

    browser.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        assert sys.argv[1].isdigit(), "Invalid input"

        level = int(sys.argv[1])

        assert level in range(1, 21), "Invalid level"

        browser = Browser()
        time.sleep(3)
        start_game(level, browser)
        browser.close()
    else:
        main()
