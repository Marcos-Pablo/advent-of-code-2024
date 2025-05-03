from pathlib import Path
import time
import tracemalloc

def extract_map_and_trailheads():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    map = []
    trailheads = []
    with open(input_path.resolve(), "r") as file:
        for line in file:
            map.append([])
            for i in range(len(line) - 1):
                height = int(line[i])
                if height == 0:
                    trailheads.append((len(map) - 1, i))
                map[-1].append(height)
    return map, trailheads

def calc_scores(map, trailheads):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    n, m = len(map), len(map[0])
    def calc_score(i, j, visited):
        if map[i][j] == 9:
            score = 1 if (i, j) not in visited else 0
            visited.add((i, j))
            return score, 1

        height = map[i][j]
        total_score = 0
        total_rating = 0
        for m1, m2 in moves:
            new_row, new_col = i + m1, j + m2
            if (
                0 <= new_row < n and 
                0 <= new_col < m and
                map[new_row][new_col] == height + 1
            ):
                score, rating = calc_score(new_row, new_col, visited)
                total_score += score
                total_rating += rating
        return total_score, total_rating
    total_score = 0
    total_rating = 0
    for i, j in trailheads:
        score, rating = calc_score(i, j, set())
        total_score += score
        total_rating += rating
    return total_score, total_rating

def main():
    tracemalloc.start()
    start = time.perf_counter()
    print("Processing input...")
    map, trailheads = extract_map_and_trailheads()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 1 and 2...")
    start = time.perf_counter()
    total_score, total_rating = calc_scores(map, trailheads)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Part 1 response: {total_score}")
    print(f"Part 2 response: {total_rating}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
