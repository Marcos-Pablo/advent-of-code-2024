from collections import defaultdict
from pathlib import Path
import time
import tracemalloc

def extract_antennas_and_size():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    antennas = defaultdict(list)
    row = 0
    n, m = 0, 0
    with open(input_path.resolve(), "r") as file:
        for line in file:
            m = len(line) - 1
            for col in range(len(line) - 1):
                if line[col] != ".":
                    antennas[line[col]].append((row, col))
            row += 1
    n = row
    return antennas, n, m

def get_anti_node_pos(x1, y1, x2, y2):
    diff_x, diff_y = abs(x1 - x2), abs(y1 - y2)
    if x1 == x2:
        new_row = x1
    elif x1 < x2:
        new_row = x1 - diff_x
    else:
        new_row = x1 + diff_x

    if y1 == y2:
        new_col = y1
    elif y1 < y2:
        new_col = y1 - diff_y
    else:
        new_col = y1 + diff_y
    return new_row, new_col

def count_anti_nodes(anttenas, n, m):
    anti_nodes_positions = set()
    for positions in anttenas.values():
        for i in range(len(positions)):
            for j in range(len(positions)):
                if i == j:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                new_row, new_col = get_anti_node_pos(x1, y1, x2, y2)
                if 0 <= new_row < n and 0 <= new_col < m:
                    anti_nodes_positions.add((new_row, new_col))
    return len(anti_nodes_positions)

def main():
    start = time.perf_counter()
    tracemalloc.start()
    
    antennas, n, m = extract_antennas_and_size()
    anti_nodes_count = count_anti_nodes(antennas, n, m)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()

    print(f"Part 1 response: {anti_nodes_count}")
    print(f"Part 2 response: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
