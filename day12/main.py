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


def verify_corners(matrix, region_type, i, j):
    n, m = len(matrix), len(matrix[0])
    total_perimeter2 = 0
    top_left_corner = (
        (j - 1 < 0 or matrix[i][j - 1] != region_type)
        and (i - 1 < 0 or matrix[i - 1][j] != region_type)
    ) or (
        (j - 1 >= 0 and matrix[i][j - 1] == region_type)
        and (i - 1 >= 0 and matrix[i - 1][j] == region_type)
        and matrix[i - 1][j - 1] != region_type
    )
    top_right_corner = (
        (j + 1 >= m or matrix[i][j + 1] != region_type)
        and (i - 1 < 0 or matrix[i - 1][j] != region_type)
    ) or (
        (j + 1 < m and matrix[i][j + 1] == region_type)
        and (i - 1 >= 0 and matrix[i - 1][j] == region_type)
        and matrix[i - 1][j + 1] != region_type
    )
    bottom_left_corner = (
        (j - 1 < 0 or matrix[i][j - 1] != region_type)
        and (i + 1 >= n or matrix[i + 1][j] != region_type)
    ) or (
        (j - 1 >= 0 and matrix[i][j - 1] == region_type)
        and (i + 1 < n and matrix[i + 1][j] == region_type)
        and matrix[i + 1][j - 1] != region_type
    )
    bottom_right_corner = (
        (j + 1 >= m or matrix[i][j + 1] != region_type)
        and (i + 1 >= n or matrix[i + 1][j] != region_type)
    ) or (
        (j + 1 < m and matrix[i][j + 1] == region_type)
        and (i + 1 < n and matrix[i + 1][j] == region_type)
        and matrix[i + 1][j + 1] != region_type
    )

    if top_left_corner:
        total_perimeter2 += 1
    if top_right_corner:
        total_perimeter2 += 1
    if bottom_left_corner:
        total_perimeter2 += 1
    if bottom_right_corner:
        total_perimeter2 += 1

    return total_perimeter2


def calc_price(matrix):
    visited = set()
    n, m = len(matrix), len(matrix[0])
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    price1 = 0
    price2 = 0

    def calc_area_and_perimeter(region_type, i, j):
        visited.add((i, j))
        total_area = 1
        total_perimeter1, total_perimeter2 = 0, 0
        total_perimeter2 += verify_corners(matrix, region_type, i, j)

        for m1, m2 in moves:
            new_row, new_col = i + m1, j + m2

            if (
                new_row < 0
                or new_row >= n
                or new_col < 0
                or new_col >= m
                or matrix[new_row][new_col] != region_type
            ):
                total_perimeter1 += 1
            elif (new_row, new_col) not in visited:
                area, perimeter1, perimeter2 = calc_area_and_perimeter(
                    region_type, new_row, new_col
                )
                total_area += area
                total_perimeter1 += perimeter1
                total_perimeter2 += perimeter2
        return total_area, total_perimeter1, total_perimeter2

    for i in range(n):
        for j in range(m):
            if (i, j) not in visited:
                area, perimeter1, perimeter2 = calc_area_and_perimeter(
                    matrix[i][j], i, j
                )
                price1 += area * perimeter1
                price2 += area * perimeter2
    return price1, price2


def main():
    tracemalloc.start()
    print("Processing input...")
    start = time.perf_counter()
    matrix = extract_matrix()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    print("Solving part 1 and 2...")
    start = time.perf_counter()
    price1, price2 = calc_price(matrix)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Response part 1: {price1}")
    print(f"Response part 2: {price2}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )


main()
