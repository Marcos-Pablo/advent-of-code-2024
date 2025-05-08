from pathlib import Path
import time
import tracemalloc
import re
import math

def calc_cost(ax, ay, bx, by, px, py):
    original_ax = ax
    original_ay = ay
    original_bx = bx
    original_by = by
    original_px = px
    original_py = py

    lcm = math.lcm(bx, by)
    factor1 = lcm // bx
    factor2 = lcm // by

    ax *= (-factor1)
    bx *= (-factor1)
    px *= (-factor1)

    ay *= (factor2)
    by *= (factor2)
    py *= (factor2)

    left_side = ax + ay
    right_side = px + py

    times_pressed_a = right_side / left_side
    if times_pressed_a % 1 != 0:
        return None

    ax = original_ax
    ay = original_ay
    bx = original_bx
    by = original_by
    px = original_px
    py = original_py
    
    ax *= times_pressed_a
    ay *= times_pressed_a

    left_side = bx + by
    right_side = px + py - (ax + ay)

    times_pressed_b = right_side / left_side

    if times_pressed_b % 1 != 0:
        return None

    price = (times_pressed_a * 3) + (times_pressed_b * 1)
    return price

def calc_min_tokens_win_every_possible_prize():
    print("Processing input...")
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    price1 = 0
    price2 = 0
    with open(input_path.resolve(), "r") as file:
        for block in file.read().split("\n\n"):
            ax, ay, bx, by, px, py = map(int ,re.findall(r"\d+", block))

            price = calc_cost(ax, ay, bx, by, px, py)
            if price != None:
                price1 += price

            price = calc_cost(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
            if price != None:
                price2 += price
    return price1, price2

def main():
    tracemalloc.start()
    start = time.perf_counter()
    price1, price2 = calc_min_tokens_win_every_possible_prize()
    print(f"Response part 1: {price1}")
    print(f"Response part 2: {price2:.0f}")
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
main()
