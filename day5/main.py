from pathlib import Path
from collections import defaultdict, deque
import time


def extract_updates_and_rules():
    rules = defaultdict(list)
    updates = []
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"

    with open(input_path.resolve(), "r") as file:
        for line in file:
            if len(line) == 6 and line[2] == "|":
                n1, n2 = line[0:2], line[3:5]
                rules[n1].append(n2)
            elif line == "\n":
                continue
            else:
                updates.append(line.replace("\n", "").split(","))
    return updates, rules


def is_update_valid(update, rules):
    pages = set(update)
    processed_pages = set()
    for page in update:
        for dependent in rules[page]:
            if dependent in pages and dependent in processed_pages:
                return False
        processed_pages.add(page)
    return True


def find_topological_sort(update, rules):
    pages = set()
    degrees = {}
    queue = deque()
    sorted_update = []

    for page in update:
        pages.add(page)
        degrees[page] = 0

    for page in update:
        for dependent in rules[page]:
            if dependent in pages:
                degrees[dependent] += 1

    for page, degree in degrees.items():
        if degree == 0:
            queue.append(page)

    while queue:
        page = queue.popleft()
        sorted_update.append(page)
        for dependent in rules[page]:
            if dependent in pages:
                degrees[dependent] -= 1
                if degrees[dependent] == 0:
                    queue.append(dependent)

    return sorted_update


def process_updates(updates, rules):
    middle_page_sum = 0
    middle_page_sum_for_fixed = 0
    for update in updates:
        if is_update_valid(update, rules):
            middle_page_idx = len(update) // 2
            middle_page = update[middle_page_idx]
            middle_page_sum += int(middle_page)
        else:
            fixed_update = find_topological_sort(update, rules)
            middle_page_idx = len(fixed_update) // 2
            middle_page = fixed_update[middle_page_idx]
            middle_page_sum_for_fixed += int(middle_page)

    return middle_page_sum, middle_page_sum_for_fixed


def main():
    start = time.perf_counter()
    updates, rules = extract_updates_and_rules()
    middle_page_sum, middle_page_sum_for_fixed = process_updates(updates, rules)
    end = time.perf_counter()

    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Middle page sum -> {middle_page_sum}")
    print(f"Middle page sum for fixed -> {middle_page_sum_for_fixed}")


main()
