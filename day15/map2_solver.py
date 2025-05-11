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
    def can_move(i, j):
        if map[i][j] == "#":
            return False
        
        if map[i][j] == ".":
            return True
        
        if map[i][j] == "[":
            return can_move(i - 1, j) and can_move(i - 1, j + 1)
        else:
            return can_move(i - 1, j) and can_move(i - 1, j - 1)

    def move(i, j):
        if map[i][j] == "[":
            move(i - 1, j)
            move(i - 1, j + 1)
        elif map[i][j] == "]":
            move(i - 1, j)
            move(i - 1, j - 1)

        map[i][j] = map[i + 1][j]
        map[i + 1][j] = "."

    if can_move(row - 1, col):
        move(row - 1, col)
        map[row][col] = "."
        return row - 1, col
    return row, col

def move_down(map, row, col):
    def can_move(i, j):
        if map[i][j] == "#":
            return False
        
        if map[i][j] == ".":
            return True
        
        if map[i][j] == "[":
            return can_move(i + 1, j) and can_move(i + 1, j + 1)
        else:
            return can_move(i + 1, j) and can_move(i + 1, j - 1)

    def move(i, j):
        if map[i][j] == "[":
            move(i + 1, j)
            move(i + 1, j + 1)
        elif map[i][j] == "]":
            move(i + 1, j)
            move(i + 1, j - 1)

        map[i][j] = map[i - 1][j]
        map[i - 1][j] = "."

    if can_move(row + 1, col):
        move(row + 1, col)
        map[row][col] = "."
        return row + 1, col
    return row, col

def move_right(map, row, col):
    j = col + 1
    while map[row][j] == "[" or map[row][j] == "]":
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
    while map[row][j] == "[" or map[row][j] == "]":
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
            if map[i][j] == "[":
                res += 100 * i + j
    return res
