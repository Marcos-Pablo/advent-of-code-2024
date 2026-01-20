from collections import defaultdict
from pathlib import Path
import time
import tracemalloc


def extract_graph():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    graph = defaultdict(set)
    with open(input_path.resolve(), "r") as file:
        for line in file:
            a, b = line.strip().split("-")
            graph[a].add(b)
            graph[b].add(a)
        return graph


def find_all_three_connected_pcs_starting_with_t(graph):
    groups = 0
    processed_pcs = set()
    for first_pc, first_connections in graph.items():
        seen_in_curr_round = set()
        if not first_pc.startswith("t"):
            continue

        for second_pc in first_connections:
            if second_pc in processed_pcs:
                continue
            seen_in_curr_round.add(second_pc)

            for third_pc in graph[second_pc]:
                if third_pc in processed_pcs or third_pc in seen_in_curr_round:
                    continue
                if first_pc in graph[third_pc]:
                    groups += 1
        processed_pcs.add(first_pc)
    return groups


def find_maximal_clique(graph):
    best_group = None
    best = 0
    vertices = sorted(graph.keys())
    store = []

    def is_clique():
        for i in range(len(store)):
            for j in range(i + 1, len(store)):
                if store[j] not in graph[store[i]]:
                    return False
        return True

    def backtrack(start):
        nonlocal best
        nonlocal best_group

        for i in range(start, len(vertices)):
            store.append(vertices[i])

            if is_clique():
                if len(store) > best:
                    best = len(store)
                    best_group = store.copy()
                backtrack(i + 1)
            store.pop()

    backtrack(0)

    if not best_group:
        return []

    return best_group


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    graph = extract_graph()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    groups = find_all_three_connected_pcs_starting_with_t(graph)

    print(f"Response part 1: {groups}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()
    biggest_group = find_maximal_clique(graph)
    password = ",".join(biggest_group)

    print(f"Response part 2: {password}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
