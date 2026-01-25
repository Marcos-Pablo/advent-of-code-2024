from pathlib import Path
import time
import tracemalloc


def extract_heights():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        lock_heights = []
        key_heights = []
        pattern = []
        for line in file:
            if line == "\n":
                if pattern[0][0] == "#":
                    lock_heights.append(extract_lock_height(pattern))
                else:
                    key_heights.append(extract_key_height(pattern))
                pattern = []
                continue

            pattern.append(line.strip())
        if pattern[0][0] == "#":
            lock_heights.append(extract_lock_height(pattern))
        else:
            key_heights.append(extract_key_height(pattern))
        return lock_heights, key_heights


def extract_lock_height(pattern):
    heights = []
    for col in range(0, len(pattern[0])):
        height = 0
        for row in range(1, len(pattern)):
            if pattern[row][col] != "#":
                break
            height += 1
        heights.append(height)
    return heights


def extract_key_height(pattern):
    heights = []
    for col in range(0, len(pattern[0])):
        height = 0
        for row in range(len(pattern) - 2, 0, -1):
            if pattern[row][col] != "#":
                break
            height += 1
        heights.append(height)
    return heights


def check_fitable_keys(lock_heights, key_heights):
    fits = 0
    for lock_height in lock_heights:
        for key_height in key_heights:
            if not overlaps(lock_height, key_height):
                fits += 1
    return fits


def overlaps(lock_height, key_height):
    for h1, h2 in zip(lock_height, key_height):
        if h1 + h2 > 5:
            return True

    return False


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    lock_heights, key_heights = extract_heights()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    fits = check_fitable_keys(lock_heights, key_heights)

    print(f"Response part 1: {fits}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    print(f"Response part 2: ")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
