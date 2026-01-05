from collections import defaultdict
from pathlib import Path
import time
import tracemalloc


def extract_matrix_and_starting_point():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    matrix = []
    starting_point = None
    with open(input_path.resolve(), "r") as file:
        for line in file:
            matrix.append([])
            for i in range(len(line) - 1):
                c = line[i]
                if c == "^":
                    starting_point = (len(matrix) - 1, i)
                    matrix[-1].append(".")
                else:
                    matrix[-1].append(c)
    return matrix, starting_point


def get_new_position(i, j, direction):
    if direction == 0:
        return i - 1, j
    elif direction == 1:
        return i, j + 1
    elif direction == 2:
        return i + 1, j
    else:
        return i, j - 1


def has_cycle(matrix, i, j, direction):
    n, m = len(matrix), len(matrix[0])
    visited = defaultdict(set)
    while True:
        new_row, new_col = get_new_position(i, j, direction)
        if new_row < 0 or new_row >= n or new_col < 0 or new_col >= m:
            return False
        if (new_row, new_col) in visited and direction in visited[(new_row, new_col)]:
            return True

        visited[(i, j)].add(direction)
        if matrix[new_row][new_col] == ".":
            i, j = new_row, new_col
        else:
            direction = (direction + 1) % 4


def trace_patrol_path(matrix, starting_point):
    n, m = len(matrix), len(matrix[0])
    i, j = starting_point
    visited = set()
    direction = 0
    cycles = 0

    while True:
        visited.add((i, j))
        new_row, new_col = get_new_position(i, j, direction)
        if new_row < 0 or new_row >= n or new_col < 0 or new_col >= m:
            break

        if matrix[new_row][new_col] == ".":
            matrix[new_row][new_col] = "#"
            if (new_row, new_col) not in visited and has_cycle(
                matrix, i, j, (direction + 1) % 4
            ):
                cycles += 1
            matrix[new_row][new_col] = "."
            i, j = new_row, new_col
        else:
            direction = (direction + 1) % 4
    return len(visited), cycles


def main():
    start = time.perf_counter()
    tracemalloc.start()

    matrix, starting_point = extract_matrix_and_starting_point()
    positions_visited, cycles = trace_patrol_path(matrix, starting_point)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()

    print(f"Part 1 response: {positions_visited}")
    print(f"Part 2 response: {cycles}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )


main()
