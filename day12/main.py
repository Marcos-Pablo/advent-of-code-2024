from pathlib import Path
import time
import tracemalloc

def extract_matrix():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    matrix = []
    with open(input_path.resolve(), "r") as file:
        for line in file:
            matrix.append(list(line[:-1]))
    return matrix

def calc_price(matrix):
    visited = set()
    n, m = len(matrix), len(matrix[0])
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    price = 0
    def calc_area_and_perimeter(region_type, i, j):
        visited.add((i, j))
        total_area, total_perimeter = 1, 0

        for m1, m2 in moves:
            new_row, new_col = i + m1, j + m2

            if (
                new_row < 0 or new_row >= n or
                new_col < 0 or new_col >= m or
                matrix[new_row][new_col] != region_type
            ):
                total_perimeter += 1
            elif (new_row, new_col) not in visited:
                area, perimeter = calc_area_and_perimeter(region_type, new_row, new_col)
                total_area += area
                total_perimeter += perimeter
        return total_area, total_perimeter
    
    for i in range(n):
        for j in range(m):
            if (i, j) not in visited:
                area, perimeter = calc_area_and_perimeter(matrix[i][j], i, j)
                price += area * perimeter
    return price

def main():
    tracemalloc.start()
    print("Processing input...")
    start = time.perf_counter()
    matrix = extract_matrix()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 1...")
    start = time.perf_counter()
    total_price = calc_price(matrix)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 1: {total_price}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 2...")
    start = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 2: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
