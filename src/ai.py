import graph


def get_movement_from_array(arr, logging=True, optimal=False):
    start = None
    end = None

    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if arr[row][col] == "#":
                start = (row, col)
            elif arr[row][col] == "E":
                end = (row, col)

    if start is None or end is None:
        print("No start or end found")
        return ""

    player = graph.Node(arr, start, end, logging=logging, optimal=optimal)

    # solve
    result = player.solve()

    # get movement
    if result:
        movement = player.movement
    else:
        movement = ""

    return movement
