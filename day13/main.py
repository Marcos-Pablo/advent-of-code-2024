from pathlib import Path
import time
import tracemalloc
import re
from day13.machine import Machine

def extract_machines():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    machines = []
    with open(input_path.resolve(), "r") as file:
        for block in file.read().split("\n\n"):
            machine = Machine()
            x1, y1, x2, y2, x3, y3 = re.findall(r"\d+", block)
            machine.buttom_a.x = int(x1)
            machine.buttom_a.y = int(y1)
            machine.buttom_b.x = int(x2)
            machine.buttom_b.y = int(y2)
            machine.prize.x = int(x3)
            machine.prize.y = int(y3)
            machines.append(machine)
    return machines

def calc_min_cost1(machine):
    cache = {}
    def press_buttom(x, y, times_pressed_a, times_pressed_b):
        if x == machine.prize.x and y == machine.prize.y:
            return 0
        if (x, y) in cache:
            return cache[(x, y)]
        if x > machine.prize.x or y > machine.prize.y:
            return float("inf")
        
        if times_pressed_a <= 100:
            press_a = 3 + press_buttom(x + machine.buttom_a.x, y + machine.buttom_a.y, times_pressed_a + 1, times_pressed_b)
        else:
            press_a = float("inf")

        if times_pressed_b <= 100:
            press_b = 1 + press_buttom(x + machine.buttom_b.x, y + machine.buttom_b.y, times_pressed_a, times_pressed_b + 1)
        else:
            press_b = float("inf")
        cache[(x, y)] = min(press_a, press_b)
        return cache[(x, y)]
    return press_buttom(0, 0, 0, 0)

def calc_min_tokens_to_win_prizes1(machines):
    tokens = 0
    for machine in machines:
        cost = calc_min_cost1(machine)
        if cost != float("inf"):
            tokens += cost
    return tokens

def calc_min_cost2(machine):
    cache = {}
    def press_buttom(x, y):
        if x == machine.prize.x + 10000000000000 and y == machine.prize.y + 10000000000000:
            return 0
        if (x, y) in cache:
            return cache[(x, y)]
        if x > machine.prize.x + 10000000000000 or y > machine.prize.y + 10000000000000:
            return float("inf")
        
        press_a = 3 + press_buttom(x + machine.buttom_a.x, y + machine.buttom_a.y)

        press_b = 1 + press_buttom(x + machine.buttom_b.x, y + machine.buttom_b.y)
        cache[(x, y)] = min(press_a, press_b)
        return cache[(x, y)]
    return press_buttom(0, 0)

def calc_min_tokens_to_win_prizes2(machines):
    tokens = 0
    for machine in machines:
        cost = calc_min_cost2(machine)
        if cost != float("inf"):
            tokens += cost
    return tokens

def main():
    tracemalloc.start()
    print("Processing input...")
    start = time.perf_counter()
    machines = extract_machines()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 1...")
    start = time.perf_counter()
    tokens1 = calc_min_tokens_to_win_prizes1(machines)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 1: {tokens1}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 2...")
    start = time.perf_counter()
    tokens2 = calc_min_tokens_to_win_prizes2(machines)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 2: {tokens2}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
main()
