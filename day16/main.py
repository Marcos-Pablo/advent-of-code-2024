from pathlib import Path
import time
import tracemalloc
import heapq

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def extract_maze():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        maze = [[line[i] for i in range(len(line) - 1)] for line in file]
    print(maze)
    return maze

def print_maze(maze):
    for line in maze:
        print(" ".join(line))

def get_reindeer_pos(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                return i, j
    return 0, 0

def get_neighbours(maze, i, j, direction):
    n, m = len(maze), len(maze[0])
    neighbours = []
    cost_up = cost_down = cost_right = cost_left = float("inf")

    if direction == UP:
        cost_up = 1
        cost_left = 1001
        cost_right = 1001
    elif direction == RIGHT:
        cost_right = 1
        cost_up = 1001
        cost_down = 1001
    elif direction == DOWN:
        cost_down = 1
        cost_right = 1001
        cost_left = 1001
    else:
        cost_left = 1
        cost_down = 1001
        cost_up = 1001

    if i - 1 >= 0 and maze[i - 1][j] != "#":
        neighbours.append((i - 1, j, cost_up, UP))

    if j - 1 >= 0 and maze[i][j - 1] != "#":
        neighbours.append((i, j - 1, cost_left, LEFT))

    if j + 1 < m and maze[i][j + 1] != "#":
        neighbours.append((i, j + 1, cost_right, RIGHT))

    if i + 1 < n and maze[i + 1][j] != "#":
        neighbours.append((i + 1, j, cost_down, DOWN))

    return neighbours

def calc_min_score_to_get_out_of_the_maze(maze):
    m = len(maze[0])
    reindeer_row, reindeer_col = get_reindeer_pos(maze)
    visited = set()
    heap = [(0, RIGHT, reindeer_row, reindeer_col)]
    while heap:
        total_cost, direction, i, j = heapq.heappop(heap)
        key = get_hash_key(i, j, direction, m)
        if key in visited:
            continue
        if maze[i][j] == "E":
            return total_cost
        visited.add(key)
        for row, col, cost, direction in get_neighbours(maze, i, j, direction):
            heapq.heappush(heap, (total_cost + cost, direction, row, col))
    return float("inf")

def get_hash_key(row, col, direction, m):
    return (row * m + col) * 4 + direction

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    maze = extract_maze()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    start = time.perf_counter()
    score = calc_min_score_to_get_out_of_the_maze(maze)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {score}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    start = time.perf_counter()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 2: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
main()
