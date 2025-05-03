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
        visited.add((i, j))
        if map[i][j] == 9:
            return 1

        height = map[i][j]
        res = 0
        for m1, m2 in moves:
            new_row, new_col = i + m1, j + m2
            if (
                0 <= new_row < n and 
                0 <= new_col < m and
                map[new_row][new_col] == height + 1
                and (new_row, new_col) not in visited
            ):
                res += calc_score(new_row, new_col, visited)
        return res
    scores = 0
    for i, j in trailheads:
        scores += calc_score(i, j, set())
    return scores

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

    print("Solving part 1...")
    start = time.perf_counter()
    scores = calc_scores(map, trailheads)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Part 1 response: {scores}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 2...")
    start = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Part 2 response: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
