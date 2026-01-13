from pathlib import Path
import time
import tracemalloc


def extract_map():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    map = []
    start_pos, end_pos = None, None
    with open(input_path.resolve(), "r") as file:
        i = 0
        for line in file:
            j = 0
            new_line = []
            for k in range(len(line) - 1):
                ch = line[k]
                new_line.append(ch)
                if ch == "S":
                    start_pos = (i, j)
                if ch == "E":
                    end_pos = (i, j)
                j += 1
            i += 1
            map.append(new_line)
    return map, start_pos, end_pos


def print_map(map):
    col_widths = [max(len(str(row[i])) for row in map) for i in range(len(map[0]))]
    for line in map:
        print(" ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(line)))


def get_next_pos(map, i, j):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for m1, m2 in moves:
        new_row, new_col = i + m1, j + m2
        if (
            0 <= new_row < len(map)
            and 0 <= new_col < len(map[0])
            and (map[new_row][new_col] == "." or map[new_row][new_col] == "E")
        ):
            return (new_row, new_col)

    return None


def calc_original_path(map, start_pos):
    original_path = []
    picoseconds = 0
    next_pos = start_pos
    while next_pos:
        i, j = next_pos
        original_path.append((i, j))
        map[i][j] = str(picoseconds)
        picoseconds += 1
        next_pos = get_next_pos(map, i, j)
    return original_path


def calc_cheats(map, original_path, max_cheats=20, threshold=100):
    count = 0
    for init_row, init_col in original_path:
        init_pogress = int(map[init_row][init_col])
        for row_offset in range(-max_cheats, max_cheats + 1):
            max_horizontal_offset = max_cheats - abs(row_offset)
            end_row = init_row + row_offset

            if end_row < 0 or end_row >= len(map):
                continue

            for col_offset in range(-max_horizontal_offset, max_horizontal_offset + 1):
                end_col = init_col + col_offset
                if end_col < 0 or end_col >= len(map[0]):
                    continue

                cheats = abs(row_offset) + abs(col_offset)
                if cheats == 0:
                    continue

                end_pos = map[end_row][end_col]
                if end_pos == "#":
                    continue

                final_progress = int(map[end_row][end_col])

                saved = (final_progress - init_pogress) - cheats
                if saved >= threshold:
                    count += 1
    return count


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    map, start_pos, end_pos = extract_map()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    original_path = calc_original_path(map, start_pos)
    print(f"Response part 1: {calc_cheats(map, original_path, 2, 100)}")
    print(f"Response part 2: {calc_cheats(map, original_path, 20, 100)}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
