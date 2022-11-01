import time

import browser
import ai
import image_processing as img_proc


def main(lvl):
    browser.select_level(lvl)

    time.sleep(3)

    board = browser.get_board()
    result = img_proc.process_board(board)

    # browser.move(ai.get_movement(lvl))
    browser.move(ai.get_movement_from_array(result))


if __name__ == "__main__":
    browser.connect()

    while True:
        user_input = input("Select level (1-20) or (q)uit: ")

        if user_input == "q":
            break

        if not user_input.isdigit():
            print("Invalid input")
            continue

        if int(user_input) not in range(1, 21):
            print("Invalid level")
            continue

        main(int(user_input))

    browser.close()
    exit()
