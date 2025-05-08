from pathlib import Path
import time
import tracemalloc
import re

def calc_cost(ax, ay, bx, by, px, py):
    ca = ((px * by) - (py * bx)) / ((ax * by) - (ay * bx))
    cb = (px - (ax * ca)) / bx
    if ca % 1 == cb % 1 == 0:
        price = (ca * 3) + (cb * 1)
        return price
    return 0

def calc_min_tokens_win_every_possible_prize():
    print("Processing input...")
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    price1 = 0
    price2 = 0
    with open(input_path.resolve(), "r") as file:
        for block in file.read().split("\n\n"):
            ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
            price1 += calc_cost(ax, ay, bx, by, px, py)
            price2 += calc_cost(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
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
