from pathlib import Path
import time
import tracemalloc
import re

def extract_input(width, height):
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    robots = []
    grid: list[list[int | str]] = [["." for _ in range(width)] for _ in range(height)]
    with open(input_path.resolve(), "r") as file:
        for line in file:
            x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
            robots.append([x, y, vx, vy])
            if grid[y][x] == ".":
                grid[y][x] = 0
            grid[y][x] += 1
    return robots, grid

def calc_new_pos(x, y, vx, vy, width, height):
    new_x = x + vx
    new_y = y + vy
    if new_x < 0:
        new_x = width + new_x
    elif new_x >= width:
        new_x %= width

    if new_y < 0:
        new_y = height + new_y
    elif new_y >= height:
        new_y %= height 
    return new_x, new_y

def move_robots(times, robots, width, height, grid):
    for _ in range(times):
        for i, (x, y, vx, vy) in enumerate(robots):
            new_x, new_y = calc_new_pos(x, y, vx, vy, width, height)
            grid[y][x] -= 1
            if grid[y][x] == 0:
                grid[y][x] = "."
            robots[i][0] = new_x
            robots[i][1] = new_y
            if grid[new_y][new_x] == ".":
                grid[new_y][new_x] = 0
            grid[new_y][new_x] += 1

def calc_safety_factor(robots, width, height):
    top_left_quadrant = 0
    top_right_quadrant = 0
    bottom_left_quadrant = 0
    bottom_right_quadrant = 0
    mid_x = width // 2
    mid_y = height // 2
    for x, y, _, _ in robots:
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            top_left_quadrant += 1
        elif x < mid_x and y > mid_y:
            top_right_quadrant += 1
        elif x > mid_x and y < mid_y:
            bottom_left_quadrant += 1
        else:
            bottom_right_quadrant += 1
    return top_left_quadrant * top_right_quadrant * bottom_left_quadrant * bottom_right_quadrant

def print_grid(grid):
    for row in grid:
        print(" ".join(str(element) for element in row))

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    width = 101
    height = 103
    times = 100
    robots, grid = extract_input(width, height)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")
    start = time.perf_counter()
    move_robots(times, robots, width, height, grid)
    safety_factor = calc_safety_factor(robots, width, height)
    print(f"Response part 1: {safety_factor}")
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
main()
