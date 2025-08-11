from collections import defaultdict, deque
from pathlib import Path
import time
import tracemalloc

def extract_map():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    map = []
    start_pos, end_pos = None, None
    with open(input_path.resolve(), "r") as file:
        i = 0
        for line in file:
            j = 0
            new_line = []
            for k in range(len(line) - 1):
                ch = line[k]
                new_line.append(ch)
                if ch == "S":
                    start_pos = (i, j)
                if ch == "E":
                    end_pos = (i, j)
                j += 1
            i += 1
            map.append(new_line)
    return map, start_pos, end_pos

def print_map(map):
    # Calculate max width for each column
    col_widths = [max(len(str(row[i])) for row in map) for i in range(len(map[0]))]
    for line in map:
        print(" ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(line)))

def get_next_pos(map, i, j):
    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for m1, m2 in moves:
        new_row, new_col = i + m1, j + m2
        if (
            0 <= new_row < len(map) and
            0 <= new_col < len(map[0]) and
            (
                map[new_row][new_col] == "." or 
                map[new_row][new_col] == "E"
            )
        ):
            return (new_row, new_col)

    return None

def get_shortcuts(map, i, j):
    shortcuts = []
    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for m1, m2 in moves:
        cheat_start_row, cheat_start_col = i + m1, j + m2
        cheat_end_row, cheat_end_col = cheat_start_row + m1, cheat_start_col + m2
        if (
            cheat_end_row < 0 or cheat_end_row >= len(map) or
            cheat_end_col < 0 or cheat_end_col >= len(map[0]) or
            map[cheat_start_row][cheat_start_col] != "#" or
            map[cheat_end_row][cheat_end_col] == "#"
        ):
            continue

        shortcuts.append((cheat_end_row, cheat_end_col))
    return shortcuts

def calc_original_path(map, start_pos):
    original_path = []
    picoseconds = 0
    next_pos = start_pos
    while next_pos:
        i, j = next_pos
        original_path.append((i, j))
        map[i][j] = str(picoseconds)
        picoseconds += 1
        next_pos = get_next_pos(map, i, j)
    return original_path

def calc_cheats(map, original_path):
    cheats = defaultdict(lambda:0)
    for i, j in original_path:
        shortcuts = get_shortcuts(map, i, j)
        for cheat_end_row, cheat_end_col in shortcuts:
            diff_in_picoseconds = int(map[cheat_end_row][cheat_end_col]) - int(map[i][j]) - 2
            if diff_in_picoseconds > 0:
                cheats[diff_in_picoseconds] += 1
    return cheats

def calc_num_of_cheats_that_saves_at_least_100_picoseconds(cheats):
    num_of_cheats_that_saves_at_least_100_picoseconds = 0
    for picoseconds_saved, count in cheats.items():
        if picoseconds_saved >= 100:
            num_of_cheats_that_saves_at_least_100_picoseconds += count
    return num_of_cheats_that_saves_at_least_100_picoseconds

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    map, start_pos, end_pos = extract_map()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    original_path = calc_original_path(map, start_pos)
    cheats = calc_cheats(map, original_path)
    num_of_cheats_that_saves_at_least_100_picoseconds = calc_num_of_cheats_that_saves_at_least_100_picoseconds(cheats)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {num_of_cheats_that_saves_at_least_100_picoseconds}")
    print(f"Response part 2: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

main()
