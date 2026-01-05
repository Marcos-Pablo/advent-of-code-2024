import re
from pathlib import Path
import time
import tracemalloc


def extract_valid_instructions():
    matches = []
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        for line in file:
            matches += re.findall(
                "mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don't\\(\\)", line
            )
    return matches


def process_instructions(instructions):
    res = 0
    res_with_tokens = 0
    is_enabled = True
    for instruction in instructions:
        if instruction == "do()":
            is_enabled = True
        elif instruction == "don't()":
            is_enabled = False
        else:
            num1, num2 = re.findall("\\d{1,3}", instruction)
            product = int(num1) * int(num2)
            res += product
            if is_enabled:
                res_with_tokens += product

    return res, res_with_tokens


def main():
    start = time.perf_counter()
    tracemalloc.start()
    instructions = extract_valid_instructions()
    res, res_with_tokens = process_instructions(instructions)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()

    print(f"result without considering tokens -> {res}")
    print(f"result considering tokens -> {res_with_tokens}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )


main()
