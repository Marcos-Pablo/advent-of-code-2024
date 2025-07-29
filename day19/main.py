from pathlib import Path
import time
import tracemalloc

def process_input():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        blocks = file.read().split("\n\n")
        available_patterns = set(blocks[0].split(", "))
        designs = blocks[1].strip().split("\n")
        return available_patterns, designs

def find_combinations(target_design, available_patterns):
    cache = {}
    def find_combinations_r(target_design):
        if target_design in cache:
            return cache[target_design]

        if not target_design:
            return 1

        combinations = 0
        for i in range(len(target_design)):
            pattern = target_design[:i + 1]
            if pattern in available_patterns:
                new_target_design = target_design[i + 1:]
                combinations += find_combinations_r(new_target_design)
        cache[target_design] = combinations
        return combinations
    return find_combinations_r(target_design)

def find_answers(designs, available_patterns):
    number_of_possible_patterns = 0
    number_of_possible_combinations = 0
    for design in designs:
        combinations = find_combinations(design, available_patterns)
        if combinations:
            number_of_possible_patterns += 1
            number_of_possible_combinations += combinations
    return number_of_possible_patterns, number_of_possible_combinations

def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    available_patterns, designs = process_input()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()
    number_of_possible_patterns, number_of_possible_combinations = find_answers(designs, available_patterns)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {number_of_possible_patterns}")
    print(f"Response part 2: {number_of_possible_combinations}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

main()
