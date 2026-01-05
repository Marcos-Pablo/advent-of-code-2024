from pathlib import Path
import time
import tracemalloc
from day15 import map1_solver
from day15 import map2_solver


def extract_maps_and_moves():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    map1, map2 = [], []
    with open(input_path.resolve(), "r") as file:
        block1, block2 = file.read().split("\n\n")
        for line in block1.split("\n"):
            map1.append([])
            map2.append([])
            for tile in line:
                map1[-1].append(tile)
                if tile == "#":
                    map2[-1].append("#")
                    map2[-1].append("#")
                elif tile == "O":
                    map2[-1].append("[")
                    map2[-1].append("]")
                elif tile == ".":
                    map2[-1].append(".")
                    map2[-1].append(".")
                else:
                    map2[-1].append("@")
                    map2[-1].append(".")
        moves = [move for move in "".join(block2.split("\n"))]
    return map1, map2, moves


def get_robot_pos(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "@":
                return i, j
    return 0, 0


def print_map(map):
    for line in map:
        print(" ".join(line))


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    map1, map2, moves = extract_maps_and_moves()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    start = time.perf_counter()
    robot_row, robot_col = get_robot_pos(map1)
    sum_coordinates_map1 = map1_solver.solve(map1, moves, robot_row, robot_col)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {sum_coordinates_map1}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    start = time.perf_counter()
    robot_row, robot_col = get_robot_pos(map2)
    sum_coordinates_map2 = map2_solver.solve(map2, moves, robot_row, robot_col)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 2: {sum_coordinates_map2}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )


main()
