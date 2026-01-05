from pathlib import Path


def process_input():
    reports = []
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        for line in file:
            report = []
            for level in line.split():
                report.append(int(level))
            reports.append(report)
    return reports


def is_report_safe(report):
    is_increasing = True if report[0] < report[1] else False
    for i in range(1, len(report)):
        prev_level = report[i - 1]
        curr_level = report[i]
        level_diff = abs(curr_level - prev_level)
        if (
            prev_level == curr_level
            or level_diff > 3
            or (is_increasing and prev_level > curr_level)
            or (not is_increasing and prev_level < curr_level)
        ):
            return False
    return True


def is_report_safe_removing_one_level(report):
    if is_report_safe(report):
        return True

    for i in range(len(report)):
        if is_report_safe(report[:i] + report[i + 1 :]):
            return True
    return False


def count_safe_reports(reports):
    safe_reports = 0
    safe_reports_removing_at_most_one_level = 0
    for report in reports:
        if is_report_safe(report):
            safe_reports += 1
            safe_reports_removing_at_most_one_level += 1
        elif is_report_safe_removing_one_level(report):
            safe_reports_removing_at_most_one_level += 1

    return safe_reports, safe_reports_removing_at_most_one_level


def main():
    reports = process_input()
    safe_reports, safe_reports_removing_at_most_one_level = count_safe_reports(reports)
    print(f"Number of safe reports -> {safe_reports}")
    print(
        f"Number of safe reports removing at most one level-> {safe_reports_removing_at_most_one_level}"
    )


main()
