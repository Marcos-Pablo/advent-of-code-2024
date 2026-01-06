from pathlib import Path
import time
import tracemalloc

UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"
CONFIRM = "A"

possible_moves = {DOWN: (1, 0), UP: (-1, 0), RIGHT: (0, 1), LEFT: (0, -1)}


def extract_codes():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        codes = file.read().splitlines()
        return codes


def numeric_keyboard():
    keyboard = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", CONFIRM]]
    return keyboard


def directional_keyboard():
    keyboard = [[None, UP, CONFIRM], [LEFT, DOWN, RIGHT]]
    return keyboard


def find_min_moves_keyboard(code, keyboard, init_row, init_col):
    min = float("inf")
    new_code = []
    visited = set()

    def find_min_moves_keyboard_r(i, row, col, curr):
        nonlocal new_code
        nonlocal min
        if i >= len(code) and len(curr) < min:
            new_code = curr.copy()
            min = len(curr)
            return

        if i >= len(code) or keyboard[row][col] == None:
            return

        if keyboard[row][col] == code[i]:
            curr.append(CONFIRM)
            find_min_moves_keyboard_r(i + 1, row, col, curr)
            curr.pop()
            return

        for key, (m1, m2) in possible_moves.items():
            new_row, new_col = row + m1, col + m2
            if new_row < 0 or new_row >= len(keyboard):
                continue
            if new_col < 0 or new_col >= len(keyboard[0]):
                continue
            if (i, new_row, new_col) in visited:
                continue

            visited.add((i, new_row, new_col))
            curr.append(key)

            find_min_moves_keyboard_r(i, new_row, new_col, curr)

            visited.remove((i, new_row, new_col))
            curr.pop()

    find_min_moves_keyboard_r(0, init_row, init_col, [])

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
    num_keyboard = numeric_keyboard()
    dir_keyboard = directional_keyboard()
    res1 = 0

    for num_code in codes:
        print(f"Processing {num_code}")
        dir_code = find_min_moves_keyboard(num_code, num_keyboard, 3, 2)
        print(f"First combination of moves= {dir_code}")

        dir_code = find_min_moves_keyboard(dir_code, dir_keyboard, 0, 2)
        print(f"Second combination of moves= {dir_code}")

        # dir_code = find_min_moves_keyboard(dir_code, dir_keyboard, 0, 2)
        # print(f"Third combination of moves= {dir_code}")
        #
        # dir_code = find_min_moves_keyboard(dir_code, dir_keyboard, 0, 2)
        # print(f"Fourth combination of moves= {dir_code}")
        #
        # res1 += len(dir_code) * extract_number(num_code)
        break

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
