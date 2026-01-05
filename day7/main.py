from collections import defaultdict
from pathlib import Path
import time
import tracemalloc


def extract_equations():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    equations = defaultdict(list)
    with open(input_path.resolve(), "r") as file:
        for line in file:
            test_value_str, values_str = line.split(":")
            test_value = int(test_value_str)
            values = []
            for val in values_str.split():
                values.append(int(val))
            equations[test_value].append(values)
    return equations


def solve_part_one(test_value, values):
    def backtracking(val, i):
        if i == len(values):
            return val == test_value

        return backtracking(val * values[i], i + 1) or backtracking(
            val + values[i], i + 1
        )

    return backtracking(values[0], 1)


def solve_part_two(test_value, values):
    def backtracking(val, i):
        if i == len(values):
            return val == test_value

        return (
            backtracking(val * values[i], i + 1)
            or backtracking(val + values[i], i + 1)
            or backtracking(int(str(val) + str(values[i])), i + 1)
        )

    return backtracking(values[0], 1)


def validate_equations(equations):
    res1 = 0
    res2 = 0
    for test_value, grouped_values in equations.items():
        for values in grouped_values:
            if solve_part_one(test_value, values):
                res1 += test_value
            if solve_part_two(test_value, values):
                res2 += test_value
    return res1, res2


def main():
    start = time.perf_counter()
    tracemalloc.start()

    equations = extract_equations()
    res1, res2 = validate_equations(equations)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()

    print(f"Part 1 response: {res1}")
    print(f"Part 2 response: {res2}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )


main()
