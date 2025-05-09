from pathlib import Path
import time
import tracemalloc
import re

def extract_input():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    robots = []
    with open(input_path.resolve(), "r") as file:
        for line in file:
            px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
            robots.append([px, py, vx, vy])
    return robots

def calc_new_pos(px, py, vx, vy, n, m):
    new_px = px + vx
    new_py = py + vy
    if new_px < 0:
        new_px = n + new_px
    elif new_px >= n:
        new_px %= n

    if new_py < 0:
        new_py = m + new_py
    elif new_py >= m:
        new_py %= m 
    return new_px, new_py

def move_robots(times, robots, n, m):
    for _ in range(times):
        for i, (px, py, vx, vy) in enumerate(robots):
            new_px, new_py = calc_new_pos(px, py, vx, vy, n, m)
            robots[i][0] = new_px
            robots[i][1] = new_py

def calc_safety_factor(robots, n, m):
    top_left_quadrant = 0
    top_right_quadrant = 0
    bottom_left_quadrant = 0
    bottom_right_quadrant = 0
    mid_x = n // 2
    mid_y = m // 2
    for px, py, _, _ in robots:
        if px == mid_x or py == mid_y:
            continue
        if px < mid_x and py < mid_y:
            top_left_quadrant += 1
        elif px < mid_x and py > mid_y:
            top_right_quadrant += 1
        elif px > mid_x and py < mid_y:
            bottom_left_quadrant += 1
        else:
            bottom_right_quadrant += 1
    return top_left_quadrant * top_right_quadrant * bottom_left_quadrant * bottom_right_quadrant

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    robots = extract_input()
    n = 101
    m = 103
    times = 100
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")
    start = time.perf_counter()
    move_robots(times, robots, n, m)
    safety_factor = calc_safety_factor(robots, n, m)
    print(f"Response part 1: {safety_factor}")
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
main()
