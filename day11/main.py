from pathlib import Path
import time
import tracemalloc

def extract_map_and_trailheads():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        for line in file:
            print(line)

def main():
    tracemalloc.start()
    start = time.perf_counter()
    print("Processing input...")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 1 and 2...")
    start = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Part 1 response: ")
    print(f"Part 2 response: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
