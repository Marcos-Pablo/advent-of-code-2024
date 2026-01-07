from pathlib import Path
import time
import tracemalloc

UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"
CONFIRM = "A"

STARTING_LEVEL_FIRST_PART = 3
STARTING_LEVEL_SECOND_PART = 26

num_keyboard = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    CONFIRM: (3, 2),
}

inv_num_keyboard = {v: k for k, v in num_keyboard.items()}


dir_keyboard = {
    UP: (0, 1),
    CONFIRM: (0, 2),
    LEFT: (1, 0),
    DOWN: (1, 1),
    RIGHT: (1, 2),
}

inv_dir_keyboard = {v: k for k, v in dir_keyboard.items()}
cache = {}


def extract_codes():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        codes = file.read().splitlines()
        return codes


def get_length(sequence, level, starting_level):
    if level == 0:
        return len(sequence)

    if (sequence, level) in cache:
        return cache[(sequence, level)]

    keyboard, inv_keyboard = dir_keyboard, inv_dir_keyboard
    if level == starting_level:
        keyboard, inv_keyboard = num_keyboard, inv_num_keyboard

    chunks = extract_chunks(sequence)
    total_length = 0
    for chunk in chunks:
        current = CONFIRM
        for ch in chunk:
            subsequence = find_min_moves_to_target(current, ch, keyboard, inv_keyboard)
            total_length += get_length(subsequence, level - 1, starting_level)
            current = ch
    cache[(sequence, level)] = total_length
    return total_length


def extract_number(code: str):
    digits = []
    for c in code:
        if not c.isdigit():
            continue

        if c == "0" and not digits:
            continue

        digits.append(c)
    return int("".join(digits))


def extract_chunks(code: str):
    chunks = []
    chunk = []
    for i, c in enumerate(code):
        chunk.append(c)

        if c != CONFIRM:
            continue

        if i + 1 < len(code) and code[i + 1] == CONFIRM:
            continue

        chunks.append("".join(chunk))
        chunk = []

    return chunks


def find_min_moves_to_target(current, target, keyboard, inv_keyboard):
    new_code = []
    row, col = keyboard[current]
    target_row, target_col = keyboard[target]

    count_up = count_down = count_left = count_right = 0

    if row > target_row:
        count_up = row - target_row
    elif row < target_row:
        count_down = target_row - row

    if col > target_col:
        count_left = col - target_col
    elif col < target_col:
        count_right = target_col - col

    if count_left:
        if count_up:
            if (row, target_col) in inv_keyboard:
                new_code.append(LEFT * count_left)
                new_code.append(UP * count_up)
            else:
                new_code.append(UP * count_up)
                new_code.append(LEFT * count_left)
        elif count_down:
            if (row, target_col) in inv_keyboard:
                new_code.append(LEFT * count_left)
                new_code.append(DOWN * count_down)
            else:
                new_code.append(DOWN * count_down)
                new_code.append(LEFT * count_left)
        else:
            new_code.append(LEFT * count_left)

    elif count_right:
        if count_up:
            if (target_row, col) in inv_keyboard:
                new_code.append(UP * count_up)
                new_code.append(RIGHT * count_right)
            else:
                new_code.append(RIGHT * count_right)
                new_code.append(UP * count_up)
        elif count_down:
            if (target_row, col) in inv_keyboard:
                new_code.append(DOWN * count_down)
                new_code.append(RIGHT * count_right)
            else:
                new_code.append(RIGHT * count_right)
                new_code.append(DOWN * count_down)
        else:
            new_code.append(RIGHT * count_right)

    elif count_up:
        new_code.append(UP * count_up)
    elif count_down:
        new_code.append(DOWN * count_down)

    new_code.append(CONFIRM)
    row, col = target_row, target_col
    return "".join(new_code)


def main():
    tracemalloc.start()
    start = time.perf_counter()
    print("Processing input...")
    codes = extract_codes()
    res1 = 0
    res2 = 0

    for num_code in codes:
        length_part_1 = get_length(
            num_code, STARTING_LEVEL_FIRST_PART, STARTING_LEVEL_FIRST_PART
        )
        length_part_2 = get_length(
            num_code, STARTING_LEVEL_SECOND_PART, STARTING_LEVEL_SECOND_PART
        )
        num = extract_number(num_code)
        res1 += length_part_1 * num
        res2 += length_part_2 * num

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Response part 1: {res1}")
    print(f"Response part 2: {res2}")

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
