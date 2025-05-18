from pathlib import Path
import time
import tracemalloc
import heapq
from collections import deque

UP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

def extract_maze():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        maze = [[line[i] for i in range(len(line) - 1)] for line in file]
    return maze

def print_maze(maze):
    for line in maze:
        print(" ".join(line))

def get_origin(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                return i, j
    return 0, 0

def get_destination(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "E":
                return i, j
    return 0, 0

def get_costs(direction):
    cost_up = cost_bottom = cost_right = cost_left = float("inf")
    if direction == UP:
        cost_up = 1
        cost_left = 1001
        cost_right = 1001
    elif direction == RIGHT:
        cost_right = 1
        cost_up = 1001
        cost_bottom = 1001
    elif direction == BOTTOM:
        cost_bottom = 1
        cost_right = 1001
        cost_left = 1001
    else:
        cost_left = 1
        cost_bottom = 1001
        cost_up = 1001
    return cost_up, cost_right, cost_bottom, cost_left

def get_neighbours(maze, i, j, direction):
    n, m = len(maze), len(maze[0])
    neighbours = []
    cost_up, cost_right, cost_bottom, cost_left = get_costs(direction)

    if i - 1 >= 0 and maze[i - 1][j] != "#" and direction != BOTTOM:
        neighbours.append((i - 1, j, cost_up, UP))

    if j - 1 >= 0 and maze[i][j - 1] != "#" and direction != RIGHT:
        neighbours.append((i, j - 1, cost_left, LEFT))

    if j + 1 < m and maze[i][j + 1] != "#" and direction != LEFT:
        neighbours.append((i, j + 1, cost_right, RIGHT))

    if i + 1 < n and maze[i + 1][j] != "#" and direction != UP:
        neighbours.append((i + 1, j, cost_bottom, BOTTOM))

    return neighbours

def calc_min_score_to_get_out_of_the_maze(maze):
    m = get_log_base_two(get_next_pow_of_two(len(maze[0])))
    origin_row, origin_col = get_origin(maze)
    heap = [(0, RIGHT, origin_row, origin_col)]
    key = get_hash_key(origin_row, origin_col, RIGHT, m)
    cache = { key: 0 }
    min_score = float("inf")
    while heap:
        cost_so_far, direction, i, j = heapq.heappop(heap)
        if cost_so_far > min_score:
            continue
        if maze[i][j] == "E":
            min_score = min(min_score, cost_so_far)
        for row, col, cost, direction in get_neighbours(maze, i, j, direction):
            neighbour_key = get_hash_key(row, col, direction, m)
            if neighbour_key not in cache or cost_so_far + cost < cache[neighbour_key]:
                cache[neighbour_key] = cost_so_far + cost
                heapq.heappush(heap, (cost_so_far + cost, direction, row, col))
    return min_score, cache

def get_up_states(i, j, maze, cache):
    if i - 1 < 0:
        return []

    m = get_log_base_two(get_next_pow_of_two(len(maze[0])))
    states = {}
    row, col = i - 1, j
    for direction in [UP, RIGHT,BOTTOM, BOTTOM]:
        key = get_hash_key(row, col, direction, m)
        if key in cache:
            states[(row, col, direction)] = cache[key]
    return states

def get_right_states(i, j, maze, cache):
    if j + 1 >= len(maze[0]):
        return []

    m = get_log_base_two(get_next_pow_of_two(len(maze[0])))
    states = {}
    row, col = i, j + 1
    for direction in [UP, RIGHT,BOTTOM, BOTTOM]:
        key = get_hash_key(row, col, direction, m)
        if key in cache:
            states[(row, col, direction)] = cache[key]
    return states

def get_bottom_states(i, j, maze, cache):
    if i + 1 >= len(maze):
        return []

    m = get_log_base_two(get_next_pow_of_two(len(maze[0])))
    states = {}
    row, col = i + 1, j
    for direction in [UP, RIGHT,BOTTOM, BOTTOM]:
        key = get_hash_key(row, col, direction, m)
        if key in cache:
            states[(row, col, direction)] = cache[key]
    return states

def get_left_states(i, j, maze, cache):
    if j - 1 < 0:
        return []

    m = get_log_base_two(get_next_pow_of_two(len(maze[0])))
    states = {}
    row, col = i, j - 1
    for direction in [UP, RIGHT,BOTTOM, BOTTOM]:
        key = get_hash_key(row, col, direction, m)
        if key in cache:
            states[(row, col, direction)] = cache[key]
    return states

def get_neighbours_with_min_cost(i, j, maze, cache):
    states_cost = {}
    states_cost.update(get_up_states(i, j, maze, cache))
    states_cost.update(get_right_states(i, j, maze, cache))
    states_cost.update(get_bottom_states(i, j, maze, cache))
    states_cost.update(get_left_states(i, j, maze, cache))
    min_cost = min(states_cost.values())
    states = []
    for (row, col, _), cost in states_cost.items():
        if cost == min_cost:
            states.append((row, col))
    return states

def get_number_of_best_seats(maze, cache):
    dest_row, dest_col = get_destination(maze)
    visited = set()
    q = deque([(dest_row, dest_col)])
    while q:
        i, j = q.popleft()
        if (i, j) in visited:
            continue
        visited.add((i, j))
        states = get_neighbours_with_min_cost(i, j, maze, cache)
        q.extend(states)
    return len(visited)

def get_next_pow_of_two(x):
    pow = 1
    while pow < x:
        pow <<= 1
    return pow

def get_log_base_two(x):
    log = 1
    while log << 1 < x:
        log <<= 1
    return log

def get_hash_key(row, col, direction, m):
    return (((row << m) | col) << 2) | direction

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
    score, cache = calc_min_score_to_get_out_of_the_maze(maze)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {score}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    start = time.perf_counter()
    number_of_best_seats = get_number_of_best_seats(maze, cache)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 2: {number_of_best_seats}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
main()
