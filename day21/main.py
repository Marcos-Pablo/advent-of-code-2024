from pathlib import Path
import time
import tracemalloc

UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"
CONFIRM = "A"

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


def extract_codes():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        codes = file.read().splitlines()
        return codes


def find_min_moves_keyboard(code, keyboard, inv_keyboard, init_row, init_col):
    new_code = []
    row, col = init_row, init_col
    for key in code:
        target_row, target_col = keyboard[key]
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


def extract_number(code: str):
    digits = []
    for c in code:
        if not c.isdigit():
            continue

        if c == "0" and not digits:
            continue

        digits.append(c)
    return int("".join(digits))


def main():
    tracemalloc.start()
    start = time.perf_counter()
    print("Processing input...")
    codes = extract_codes()
    res1 = 0

    for num_code in codes:
        print()
        print(f"Processing {num_code}")
        first_dir_code = find_min_moves_keyboard(
            num_code, num_keyboard, inv_num_keyboard, 3, 2
        )
        print(f"First combination of moves= {first_dir_code}")

        second_dir_code = find_min_moves_keyboard(
            first_dir_code, dir_keyboard, inv_dir_keyboard, 0, 2
        )
        print(f"Second combination of moves= {second_dir_code}")

        third_dir_code = find_min_moves_keyboard(
            second_dir_code, dir_keyboard, inv_dir_keyboard, 0, 2
        )
        print(f"Third combination of moves= {third_dir_code}")

        num = extract_number(num_code)
        res = len(third_dir_code) * num
        print(f"{len(third_dir_code)} * {num} = {res}")

        res1 += res

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Response part 1: {res1}")
    print(f"Response part 2: ")

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
