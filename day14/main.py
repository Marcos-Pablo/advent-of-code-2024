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
            x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
            robots.append([x, y, vx, vy])
    return robots


def solve(times, robots, width, height):
    min_safety_factor = float("inf")
    safety_factor_after_100_seconds = 0
    number_of_seconds_to_draw_tree = 0

    for second in range(times):
        for i, (x, y, vx, vy) in enumerate(robots):
            new_x = (x + (1 * vx)) % width
            new_y = (y + (1 * vy)) % height
            robots[i][0] = new_x
            robots[i][1] = new_y
        safety_factor = calc_safety_factor(robots, width, height)
        if safety_factor < min_safety_factor:
            min_safety_factor = safety_factor
            number_of_seconds_to_draw_tree = second
        if second == 99:
            safety_factor_after_100_seconds = safety_factor

    return safety_factor_after_100_seconds, number_of_seconds_to_draw_tree + 1


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
    return (
        top_left_quadrant
        * top_right_quadrant
        * bottom_left_quadrant
        * bottom_right_quadrant
    )


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    width = 101
    height = 103
    times = 10000

    robots = extract_input()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    start = time.perf_counter()
    safety_factor_after_100_seconds, number_of_seconds_to_draw_tree = solve(
        times, robots, width, height
    )

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {safety_factor_after_100_seconds}")
    print(f"Response part 2: {number_of_seconds_to_draw_tree}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )


main()
