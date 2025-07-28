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

def can_form_pattern(rem, available_patterns):
    if not rem:
        return True
    for i in range(len(rem)):
        pattern = rem[:i + 1]
        if pattern in available_patterns and can_form_pattern(rem[i + 1:], available_patterns):
            return True
    return False

def find_answer_part1(designs, available_patterns):
    number_of_possible_patterns = 0
    for design in designs:
        if can_form_pattern(design, available_patterns):
            number_of_possible_patterns += 1
    return number_of_possible_patterns

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
    number_of_possible_patterns = find_answer_part1(designs, available_patterns)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {number_of_possible_patterns}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print(f"Response part 2: ")
main()
