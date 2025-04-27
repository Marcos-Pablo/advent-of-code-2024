from pathlib import Path
from collections import defaultdict
import time

def extract_rules_and_updates():
    rules = defaultdict(list)
    updates = []
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"

    with open(input_path.resolve(), "r") as file:
        for line in file:
            if len(line) == 6 and line[2] == "|":
                n1, n2 = line[0:2], line[3:5]
                rules[n2].append(n1)
            elif line == "\n":
                continue
            else:
                updates.append(line.replace("\n", "").split(","))
    return updates, rules

def is_update_valid(update, rules):
    pages = set(update)
    processed_pages = set()
    for page in update:
        for dependency in rules[page]:
            if dependency in pages and dependency not in processed_pages:
                return False
        processed_pages.add(page)
    return True

def process_updates(updates, rules):
    middle_page_sum = 0
    for update in updates:
        if is_update_valid(update, rules):
            middle_page_idx = len(update) // 2
            middle_page = update[middle_page_idx]
            middle_page_sum += int(middle_page)
    return middle_page_sum

def main():
    start = time.perf_counter()
    updates, rules = extract_rules_and_updates()
    middle_page_sum = process_updates(updates, rules)
    end = time.perf_counter()
    
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(f"Middle page sum -> {middle_page_sum}")

main()
