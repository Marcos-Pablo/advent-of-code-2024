from collections import deque
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
            for ch in line:
                new_line.append(ch)
                if ch == "S":
                    start_pos = (i, j)
                if ch == "E":
                    end_pos = (i, j)
                j += 1
            i += 1
            map.append(new_line)
    return map, start_pos, end_pos

def print_map(map, start_pos, end_pos):
    for line in map:
        print(" ".join(line))

    print(f"start_pos -> {start_pos}")
    print(f"end_pos -> {end_pos}")

def get_neighbours(map, i, j):
    neighbours = []
    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for m1, m2 in moves:
        new_row, new_col = i + m1, j + m2
        if (
            new_row < 0 or new_row >= len(map) or
            new_col < 0 or new_col >= len(map[0]) or
            map[new_row][new_col] == "#"
        ):
            continue
        neighbours.append((new_row, new_col))
    return neighbours

def fill_map_with_original_time(map, start_pos):
    visited = set([start_pos])
    q = deque([start_pos])
    
    picoseconds = 0
    while q:
        i, j = q.popleft()
        map[i][j] = str(picoseconds)

        for new_row, new_col in get_neighbours(map, i, j):
            if (new_row, new_col) in visited:
                continue
            q.append((new_row, new_col))
            visited.add((new_row, new_col))
        picoseconds += 1

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    map, start_pos, end_pos = extract_map()
    print_map(map, start_pos, end_pos)
    fill_map_with_original_time(map, start_pos)
    print_map(map, start_pos, end_pos)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: ")
    print(f"Response part 2: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

main()
