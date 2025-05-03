from pathlib import Path
import time
import tracemalloc

def extract_disk_map():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    disk_map = []
    pos = 0
    id = 0
    with open(input_path.resolve(), "r") as file:
        char = file.read(1)
        while char != "\n":
            num = int(char)
            if pos % 2 == 0:
                for _ in range(num):
                    disk_map.append(id)
                id += 1
            else:
                for _ in range(num):
                    disk_map.append(".")
            pos += 1
            char = file.read(1)
    return disk_map

def get_next_empty_pos_left_to_right(disk_map, i):
    i += 1
    while i < len(disk_map) and disk_map[i] != ".":
        i += 1
    return i

def get_next_non_empty_pos_right_to_left(disk_map, j):
    j -= 1
    while j < len(disk_map) and disk_map[j] == ".":
        j -= 1
    return j

def get_next_empty_size_window(disk_map, i, size = 1):
    start = i + 1
    end = start
    while start < len(disk_map):
        if disk_map[start] != ".":
            start += 1
            continue

        end = start
        while (
            end - start + 1 < size and
            end + 1 < len(disk_map) and 
            disk_map[end + 1] == "."
        ):
            end += 1

        if end - start + 1 == size:
            break
        else:
            start = end + 1

    return start, end

def calculate_checksum(disk_map):
    checksum = 0
    for i in range(len(disk_map)):
        if disk_map[i] != ".":
            checksum += disk_map[i] * i
    return checksum

def fragment_disk_strategy1(disk_map):
    i = get_next_empty_pos_left_to_right(disk_map, -1)
    j = get_next_non_empty_pos_right_to_left(disk_map, len(disk_map))
    while i < j:
        disk_map[i], disk_map[j] = disk_map[j], disk_map[i]
        i = get_next_empty_pos_left_to_right(disk_map, i)
        j = get_next_non_empty_pos_right_to_left(disk_map, j)

def fragment_disk_strategy2(disk_map):
    files = []
    start = 0
    while start < len(disk_map):
        end = start
        while end + 1 < len(disk_map) and disk_map[end] == disk_map[end + 1]:
            end += 1
        
        id = disk_map[start]
        if id != ".":
            size = end - start + 1
            files.append((id, start, size))
        start = end + 1

    while files:
        id, start, size = files.pop()
        end = start + size - 1
        empty_w_start, empty_w_end = get_next_empty_size_window(disk_map, -1, size)
        if empty_w_end < start:
            disk_map[empty_w_start:empty_w_end + 1], disk_map[start:end + 1] = (
                disk_map[start:end + 1], disk_map[empty_w_start:empty_w_end + 1]
            )

def main():
    start = time.perf_counter()
    tracemalloc.start()

    disk_map = extract_disk_map()
    disk_map_copy = disk_map.copy()

    fragment_disk_strategy1(disk_map)
    checksumstrategy1 = calculate_checksum(disk_map)

    fragment_disk_strategy2(disk_map_copy)
    checksumstrategy2 = calculate_checksum(disk_map_copy)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()

    print(f"Part 1 response: {checksumstrategy1}")
    print(f"Part 2 response: {checksumstrategy2}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
