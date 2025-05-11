from pathlib import Path
import time
import tracemalloc

def extract_map_and_moves():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    map, moves = [], []
    with open(input_path.resolve(), "r") as file:
        block1, block2 = file.read().split("\n\n")
        map = [[coord for coord in line] for line in block1.split("\n")]
        moves = [move for move in "".join(block2.split("\n"))]
    return map, moves

def get_robot_pos(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "@":
                return i, j
    return 0, 0

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

def process_moves(map, moves):
    row, col = get_robot_pos(map)
    for move in moves:
        if move == "^":
            row, col = move_up(map, row, col)
        elif move == ">":
            row, col = move_right(map, row, col)
        elif move == "v":
            row, col = move_down(map, row, col)
        else:
            row, col = move_left(map, row, col)

def print_map(map):
    for line in map:
        print(" ".join(line))

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    map, moves = extract_map_and_moves()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    start = time.perf_counter()
    process_moves(map, moves)
    sum_coordinates = calc_sum_coordinates(map)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {sum_coordinates}")
    print(f"Response part 2: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
