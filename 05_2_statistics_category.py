import json
import os
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


FOLDER = Path("prel/final_abstract_steps")
OUTPUT_FILENAME = Path("category_reasoning_percentage.md")
CATEGORIES_TO_PROCESS = ("cat01", "cat02", "cat03", "cat04", "cat05", "cat06")
CATEGORY_PATTERN = re.compile(r"_(cat\d{2})_")
JSON_WORKERS = min(32, (os.cpu_count() or 1) * 4)

ACTIVITIES = (
    "Pattern Recognition",
    "Deductive Reasoning",
    "Inductive Reasoning",
    "Abductive Reasoning",
    "Hypothesis Generation",
    "Validation",
    "Backtracking",
    "Ethical or Moral Reasoning",
    "Counterfactual Reasoning",
    "Heuristic Reasoning",
)

ACTIVITY_ABBREVIATIONS = {
    "Pattern Recognition": "P.R.",
    "Deductive Reasoning": "D.R.",
    "Inductive Reasoning": "I.R.",
    "Abductive Reasoning": "A.R.",
    "Hypothesis Generation": "H.G.",
    "Validation": "V",
    "Backtracking": "B",
    "Ethical or Moral Reasoning": "E.R.",
    "Counterfactual Reasoning": "C.R.",
    "Heuristic Reasoning": "H.R.",
}

ACTIVITY_SET = set(ACTIVITIES)


def iter_json_paths(folder):
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".json"):
                yield Path(entry.path)


def parse_activity_name(name):
    activity, separator, _ = name.partition(" - ")
    if not separator:
        return None
    return activity.strip()


def extract_category(filename):
    match = CATEGORY_PATTERN.search(filename)
    if match is None:
        return None
    return match.group(1)


def collect_category_counts(folder):
    category_counts = {category: Counter() for category in CATEGORIES_TO_PROCESS}
    total_steps = Counter()
    processed_files_count = 0
    skipped_files_count = 0

    print(f"Processing files in folder: {folder}")
    try:
        paths = list(iter_json_paths(folder))
    except FileNotFoundError:
        print(f"Error: Folder not found: {folder}")
        raise SystemExit(1)

    print(f"Found {len(paths)} JSON files.")

    worker_count = min(JSON_WORKERS, len(paths)) or 1
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        for result in executor.map(read_category_file, paths):
            if result is None:
                skipped_files_count += 1
                continue

            category, file_activity_counts, file_step_count = result
            category_counts[category].update(file_activity_counts)
            total_steps[category] += file_step_count
            if file_step_count > 0:
                processed_files_count += 1

    print(f"\nProcessed {processed_files_count} files containing valid steps.")
    if skipped_files_count:
        print(f"Skipped {skipped_files_count} files.")

    return category_counts, total_steps


def read_category_file(path):
    category = extract_category(path.name)
    if category not in CATEGORIES_TO_PROCESS:
        return None

    try:
        with path.open("r", encoding="utf-8") as fp:
            steps = json.load(fp)
    except (json.JSONDecodeError, OSError):
        return None

    if not isinstance(steps, list) or not steps:
        return None

    activity_counts = Counter()
    for step in steps[:-1]:
        if not isinstance(step, dict):
            continue

        activity = parse_activity_name(step.get("Name", ""))
        if activity in ACTIVITY_SET:
            activity_counts[activity] += 1

    return category, activity_counts, sum(activity_counts.values())


def percentage(numerator, denominator):
    if denominator == 0:
        return "0.0"
    return f"{float(numerator) / float(denominator) * 100.0:.1f}"


def markdown_table(headers, rows, right_align=None):
    right_align = set(right_align or ())
    string_rows = [[str(cell) for cell in row] for row in rows]
    widths = []
    for index, header in enumerate(headers):
        widths.append(max([len(str(header))] + [len(row[index]) for row in string_rows]))

    def format_row(values):
        cells = []
        for index, value in enumerate(values):
            value = str(value)
            if headers[index] in right_align:
                cells.append(value.rjust(widths[index]))
            else:
                cells.append(value.ljust(widths[index]))
        return "| " + " | ".join(cells) + " |"

    alignment = [
        (
            "-" * max(width, 3) + ":"
            if headers[index] in right_align
            else ":" + "-" * max(width, 3)
        )
        for index, width in enumerate(widths)
    ]
    return "\n".join(
        [format_row(headers), "| " + " | ".join(alignment) + " |"]
        + [format_row(row) for row in string_rows]
    )


def build_results_table(category_counts, total_steps):
    headers = ("Category",) + tuple(ACTIVITY_ABBREVIATIONS[activity] for activity in ACTIVITIES)
    rows = []

    for category in CATEGORIES_TO_PROCESS:
        total = total_steps[category]
        row = [category]
        for activity in ACTIVITIES:
            row.append(percentage(category_counts[category][activity], total))
        rows.append(tuple(row))

    return markdown_table(headers, rows, right_align=set(headers[1:]))


def write_report(markdown_table_content):
    with OUTPUT_FILENAME.open("w", encoding="utf-8") as fp:
        fp.write("# Reasoning Steps Percentage by Category\n\n")
        fp.write(
            "This table shows the percentage distribution of different reasoning steps within each question category.\n"
        )
        fp.write(
            "Each cell represents the percentage of steps corresponding to the reasoning type "
            "(column) out of the total steps counted for that category (row).\n\n"
        )
        fp.write(markdown_table_content)
        fp.write("\n\n")
        fp.write("## Activity Legend\n\n")
        for activity, abbreviation in sorted(
            ACTIVITY_ABBREVIATIONS.items(), key=lambda item: item[1]
        ):
            fp.write(f"* **{abbreviation}**: {activity}\n")

    print(f"\nSuccessfully created Markdown report: '{OUTPUT_FILENAME}'")


def main():
    category_counts, total_steps = collect_category_counts(FOLDER)
    write_report(build_results_table(category_counts, total_steps))


if __name__ == "__main__":
    main()
