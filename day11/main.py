from pathlib import Path
import time
import tracemalloc

def extract_stones():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        stones = file.read().split()
        return stones

def count_stones_after_blinks(stones, times):
    cache = {}
    def blink(stone, times):
        if times == 0:
            return 1

        if (stone, times) in cache:
            return cache[(stone, times)]
        
        if stone == "0":
            cache[(stone, times)] = blink("1", times - 1)
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            left, right = stone[:mid], stone[mid:]
            right = str(int(right))
            cache[(stone, times)] = blink(left, times - 1) + blink(right, times - 1)
        else:
            new_stone = str(int(stone) * 2024)
            cache[(stone, times)] = blink(new_stone, times - 1)
        return cache[(stone, times)]
    
    number_of_stones = 0
    for stone in stones:
        number_of_stones += blink(stone, times)
    return number_of_stones

def main():
    tracemalloc.start()
    print("Processing input...")
    start = time.perf_counter()
    stones = extract_stones()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 1...")
    start = time.perf_counter()
    number_of_stones_25_blinks = count_stones_after_blinks(stones, 25)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 1: {number_of_stones_25_blinks}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 2...")
    start = time.perf_counter()
    number_of_stones_75_blinks = count_stones_after_blinks(stones, 75)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 2: {number_of_stones_75_blinks}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
