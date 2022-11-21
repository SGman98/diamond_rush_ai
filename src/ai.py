import graph


def get_movement(lvl):
    solutions = {
        1: "dddddsssaaaaassdsdddds",
        2: "aaaaasawwwwwwwwwdwdsddssddsaassaas",
        3: "dssssssassdddddddaaawwwwddwdssawaaawwssssssdswwwwwwawwdwddwdassdw",
        4: "ddddssaaaaassddddddassaaaaasdwdsssdswwawddwdsss",
        # ...
    }

    return solutions.get(lvl, "")


def get_movement_from_array(arr):
    start = None
    end = None

    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if arr[row][col] == "#":
                start = (row, col)
            elif arr[row][col] == "E":
                end = (row, col)

    # movement = graph.get_path(arr, start, end)
    player = graph.Node(arr, start, end)

    # solve
    result = player.solve()

    # get movement
    if result:
        movement = player.movement
    else:
        movement = []

    return "".join(movement)
