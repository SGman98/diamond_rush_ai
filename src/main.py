import sys
import time

import ai
import image_processing as img_proc
from browser import Browser


def start_game(browser, logging=True, optimal=False, show_image=False):
    board = browser.get_board()
    result = img_proc.process_board(board)

    if show_image:
        recreated = img_proc.recreate_board(result, 8, 12)
        img_proc.show_image(recreated)

    movement = ai.get_movement_from_array(result, logging=logging, optimal=optimal)
    browser.move(movement)


def main(lvl, logging=True, optimal=False, show_image=False):
    browser = Browser()
    time.sleep(1)
    if lvl is not None:
        browser.select_level(lvl)
        time.sleep(3)
        start_game(browser, logging, optimal, show_image)
    else:
        browser.unlock_all_levels()
        while True:
            if input("Press enter to start or write exit to close ") == "exit":
                break
            start_game(browser, logging, optimal, show_image)

    browser.close()


if __name__ == "__main__":
    args = sys.argv[1:]

    lvl = next(
        (int(arg) for arg in args if arg.isdigit() and 1 <= int(arg) <= 20),
        None,
    )

    main(
        lvl,
        "--no-logs" not in args,
        "--optimal" in args,
        "--show-image" in args,
    )
