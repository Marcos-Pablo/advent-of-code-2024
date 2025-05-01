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

def calculate_checksum(disk_map):
    i = 0
    checksum = 0
    while i < len(disk_map) and disk_map[i] != ".":
        checksum += i * disk_map[i]
        i += 1
    return checksum

def fragment_disk(disk_map):
    i = get_next_empty_pos_left_to_right(disk_map, -1)
    j = get_next_non_empty_pos_right_to_left(disk_map, len(disk_map))
    while i < j:
        disk_map[i], disk_map[j] = disk_map[j], disk_map[i]
        i = get_next_empty_pos_left_to_right(disk_map, i)
        j = get_next_non_empty_pos_right_to_left(disk_map, j)

def main():
    start = time.perf_counter()
    tracemalloc.start()

    disk_map = extract_disk_map()
    fragment_disk(disk_map)
    checksum = calculate_checksum(disk_map)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()

    print(f"Part 1 response: {checksum}")
    print(f"Part 2 response: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
