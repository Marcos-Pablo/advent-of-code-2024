from collections import Counter

def solve_part_one(left_list, right_list):
    total_diff = 0

    for left_id, right_id in zip(left_list, right_list):
        total_diff += abs(left_id - right_id)

    return total_diff

def solve_part_two(left_list, right_list):
    similarity_score = 0
    appearances_count = Counter(right_list)
    for left_id in left_list:
        similarity_score += left_id * appearances_count.get(left_id, 0)

    return similarity_score

def process_input():
    left_list, right_list = [], []
    with open("./input.txt", "r") as file:
        for line in file:
            left_id, right_id = line.split()
            left_list.append(int(left_id))
            right_list.append(int(right_id))

    left_list.sort()
    right_list.sort()

    return left_list, right_list

def main():
    left_list, right_list = process_input()
    response_part_one = solve_part_one(left_list, right_list)
    response_part_two = solve_part_two(left_list, right_list)

    print(f"response part one - > {response_part_one}")
    print(f"response part two - > {response_part_two}")
main()

