from pathlib import Path
import time
import tracemalloc
from list_node import ListNode

def extract_disk_map():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    disk_map = []
    files = []
    empty_spaces = ListNode(0, 0)
    curr_node = empty_spaces
    pos = 0
    id = 0
    with open(input_path.resolve(), "r") as file:
        char = file.read(1)
        while char != "\n":
            num = int(char)
            if pos % 2 == 0:
                start = len(disk_map)
                files.append((start, num))
                for _ in range(num):
                    disk_map.append(id)
                id += 1
            else:
                if num > 0:
                    node = ListNode(len(disk_map), num)
                    curr_node.next = node
                    curr_node = node
                for _ in range(num):
                    disk_map.append(".")
            pos += 1
            char = file.read(1)
    return disk_map, files, empty_spaces

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

def get_next_empty_space_by_size(empty_spaces, size):
    node = empty_spaces
    while node.next:
        if node.next.size == size:
            empty_space_start = node.next.start
            node.next = node.next.next
            return empty_space_start
        elif node.next.size > size:
            empty_space_start = node.next.start
            node.next.start += size
            node.next.size -= size
            return empty_space_start
        node = node.next
    return None

def fragment_disk_strategy1(disk_map):
    i = get_next_empty_pos_left_to_right(disk_map, -1)
    j = get_next_non_empty_pos_right_to_left(disk_map, len(disk_map))
    while i < j:
        disk_map[i], disk_map[j] = disk_map[j], disk_map[i]
        i = get_next_empty_pos_left_to_right(disk_map, i)
        j = get_next_non_empty_pos_right_to_left(disk_map, j)

def fragment_disk_strategy2(disk_map, files, empty_spaces):
    while files:
        start, size = files.pop()
        end = start + size - 1
        empty_space_start = get_next_empty_space_by_size(empty_spaces, size)

        if empty_space_start == None:
            continue

        empty_w_start = empty_space_start
        empty_w_end = empty_w_start + size - 1
        if empty_w_end < start:
            disk_map[empty_w_start:empty_w_end + 1], disk_map[start:end + 1] = (
                disk_map[start:end + 1], disk_map[empty_w_start:empty_w_end + 1]
            )

def main():
    tracemalloc.start()
    start = time.perf_counter()
    print("Processing input...")
    disk_map, files, empty_spaces = extract_disk_map()
    disk_map_copy = disk_map.copy()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 1...")
    start = time.perf_counter()
    fragment_disk_strategy1(disk_map)
    checksumstrategy1 = calculate_checksum(disk_map)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Part 1 response: {checksumstrategy1}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")
    print("==================================")

    print("Solving part 2...")
    start = time.perf_counter()
    fragment_disk_strategy2(disk_map_copy, files, empty_spaces)
    checksumstrategy2 = calculate_checksum(disk_map_copy)
    current, peak = tracemalloc.get_traced_memory()
    end = time.perf_counter()
    print(f"Part 2 response: {checksumstrategy2}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB")

main()
