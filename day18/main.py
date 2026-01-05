from pathlib import Path
from collections import deque
import time
import tracemalloc

NUM_ROWS = 71
NUM_COLS = 71
NUM_BYTES = 1024


def find_answers():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    matrix = [["." for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    with open(input_path.resolve(), "r") as file:
        for _ in range(NUM_BYTES):
            coords = file.readline().split(",")
            j, i = int(coords[0]), int(coords[1])
            matrix[i][j] = "#"

        shortest_path = find_shortest_path(matrix)
        while True:
            coords = file.readline().split(",")
            j, i = int(coords[0]), int(coords[1])
            matrix[i][j] = "#"
            curr_best_path = find_shortest_path(matrix)
            if curr_best_path == None:
                return shortest_path, (j, i)


def print_matrix(matrix):
    for line in matrix:
        print(" ".join(line))


def get_neighbours(i, j, matrix):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    neighbours = []

    for m1, m2 in moves:
        new_row, new_col = i + m1, j + m2
        if (
            new_row < 0
            or new_row >= NUM_ROWS
            or new_col < 0
            or new_col >= NUM_COLS
            or matrix[new_row][new_col] == "#"
        ):
            continue
        neighbours.append((new_row, new_col))

    return neighbours


def find_shortest_path(matrix):
    q = deque([(0, 0)])
    visited = set([(0, 0)])
    dist = 0
    while q:
        for _ in range(len(q)):
            i, j = q.popleft()

            if i == NUM_ROWS - 1 and j == NUM_COLS - 1:
                return dist

            for new_row, new_col in get_neighbours(i, j, matrix):
                if (new_row, new_col) in visited:
                    continue
                q.append((new_row, new_col))
                visited.add((new_row, new_col))

        dist += 1


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    shortest_path, first_blocking_byte = find_answers()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Response part 1: {shortest_path}")
    print(f"Response part 2: {first_blocking_byte[0]},{first_blocking_byte[1]}")

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
