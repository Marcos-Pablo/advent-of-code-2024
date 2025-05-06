from pathlib import Path
import time
import tracemalloc
import re

class Machine:
    def __init__(self):
        self.buttom_a_x = -1
        self.buttom_a_y = -1
        self.buttom_b_x = -1
        self.buttom_b_y = -1
        self.prize_x = -1
        self.prize_y = -1

def extract_machines():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    machines = []
    with open(input_path.resolve(), "r") as file:
        label = 0
        machine = Machine()
        for line in file:
            if label == 0:
                x, y = re.findall("\\d\\d", line)
                machine.buttom_a_x = int(x)
                machine.buttom_a_y = int(y)
                label += 1
            elif label == 1:
                x, y = re.findall("\\d\\d", line)
                machine.buttom_b_x = int(x)
                machine.buttom_b_y = int(y)
                label += 1
            elif label == 2:
                x, y = re.findall("\\d{3,7}", line)
                machine.prize_x = int(x)
                machine.prize_y = int(y)
                label += 1
                machines.append(machine)
            elif label == 3:
                label = 0
                machine = Machine()
    return machines

def calc_min_cost1(machine):
    cache = {}
    def press_buttom(x, y, times_pressed_a, times_pressed_b):
        if x == machine.prize_x and y == machine.prize_y:
            return 0
        if (x, y) in cache:
            return cache[(x, y)]
        if x > machine.prize_x or y > machine.prize_y:
            return float("inf")
        
        if times_pressed_a <= 100:
            press_a = 3 + press_buttom(x + machine.buttom_a_x, y + machine.buttom_a_y, times_pressed_a + 1, times_pressed_b)
        else:
            press_a = float("inf")

        if times_pressed_b <= 100:
            press_b = 1 + press_buttom(x + machine.buttom_b_x, y + machine.buttom_b_y, times_pressed_a, times_pressed_b + 1)
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
        if x == machine.prize_x + 10000000000000 and y == machine.prize_y + 10000000000000:
            return 0
        if (x, y) in cache:
            return cache[(x, y)]
        if x > machine.prize_x + 10000000000000 or y > machine.prize_y + 10000000000000:
            return float("inf")
        
        press_a = 3 + press_buttom(x + machine.buttom_a_x, y + machine.buttom_a_y)

        press_b = 1 + press_buttom(x + machine.buttom_b_x, y + machine.buttom_b_y)
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
