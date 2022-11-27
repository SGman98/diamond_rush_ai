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

    start_time = time.perf_counter()
    movement = ai.get_movement_from_array(result, logging=logging, optimal=optimal)
    end_time = time.perf_counter()

    hours = int((end_time - start_time) // 3600)
    minutes = int((end_time - start_time) // 60)
    seconds = int((end_time - start_time) % 60)
    milliseconds = int((end_time - start_time) * 1000 % 1000)

    if movement != "":
        print(
            f"Found path in {hours}:{minutes}:{seconds}.{milliseconds} with length {len(movement)}"
        )
        print(f"Path: {movement}")
    else:
        print(f"No path found in {hours}:{minutes}:{seconds}.{milliseconds}")

    browser.move(movement)


def help():
    print("'no-logs' to disable logs")
    print("'optimal' to find optimal solution")
    print("'show-image' to show recreated board")
    print("'exit' to close")
    print("'help' to show this message")


def main(lvl, logging=True, optimal=False, show_image=False):
    browser = Browser()
    time.sleep(1)
    if lvl is not None:
        browser.select_level(lvl)
        time.sleep(3)
        start_game(browser, logging, optimal, show_image)
    else:
        browser.unlock_all_levels()
        help()
        while True:
            user_input = input("Write your options separated by space: ")

            if "exit" in user_input:
                break

            if "help" in user_input:
                help()
                continue

            logging = "no-logs" not in user_input
            optimal = "optimal" in user_input
            show_image = "show-image" in user_input

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
