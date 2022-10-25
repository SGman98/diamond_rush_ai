
def get_movement(lvl):
    solutions = {
        1: "dddddsssaaaaassdsdddds",
        2: "aaaaasawwwwwwwwwdwdsddssddsaassaas",
        3: "dssssssassdddddddaaawwwwddwdssawaaawwssssssdswwwwwwawwdwddwdassdw",
        4: "ddddssaaaaassddddddassaaaaasdwdsssdswwawddwdsss",
        # ...
    }

    return solutions.get(lvl, "")
