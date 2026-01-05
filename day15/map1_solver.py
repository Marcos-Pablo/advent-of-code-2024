def solve(map, moves, robot_row, robot_col):
    for move in moves:
        if move == "^":
            robot_row, robot_col = move_up(map, robot_row, robot_col)
        elif move == ">":
            robot_row, robot_col = move_right(map, robot_row, robot_col)
        elif move == "v":
            robot_row, robot_col = move_down(map, robot_row, robot_col)
        else:
            robot_row, robot_col = move_left(map, robot_row, robot_col)
    return calc_sum_coordinates(map)


def move_up(map, row, col):
    i = row - 1
    while map[i][col] == "O":
        i -= 1
    if map[i][col] == ".":
        while i < row:
            map[i][col] = map[i + 1][col]
            i += 1
        map[row][col] = "."
        return row - 1, col
    return row, col


def move_down(map, row, col):
    i = row + 1
    while map[i][col] == "O":
        i += 1
    if map[i][col] == ".":
        while i > row:
            map[i][col] = map[i - 1][col]
            i -= 1
        map[row][col] = "."
        return row + 1, col
    return row, col


def move_right(map, row, col):
    j = col + 1
    while map[row][j] == "O":
        j += 1
    if map[row][j] == ".":
        while j > col:
            map[row][j] = map[row][j - 1]
            j -= 1
        map[row][col] = "."
        return row, col + 1
    return row, col


def move_left(map, row, col):
    j = col - 1
    while map[row][j] == "O":
        j -= 1
    if map[row][j] == ".":
        while j < col:
            map[row][j] = map[row][j + 1]
            j += 1
        map[row][col] = "."
        return row, col - 1
    return row, col


def calc_sum_coordinates(map):
    res = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "O":
                res += 100 * i + j
    return res
