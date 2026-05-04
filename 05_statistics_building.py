import json
import os
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


FOLDER = Path("prel/final_abstract_steps")
OUTPUT_FILENAME = Path("reasoning_dashboards.md")
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

EFFECT_TO_TOTAL_KEY = {
    "PE": "step_positive_effect",
    "IND": "step_indifferent",
    "NE": "step_negative_effect",
}

CONCLUSION_TO_KEY = {
    "C": "conclusion_correct",
    "PC": "conclusion_partially_correct",
    "W": "conclusion_incorrect",
}


def iter_json_paths(folder):
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".json"):
                yield Path(entry.path)


def new_model_stats():
    return {
        "conclusion_correct": 0,
        "conclusion_partially_correct": 0,
        "conclusion_incorrect": 0,
        "step_positive_effect": 0,
        "step_indifferent": 0,
        "step_negative_effect": 0,
        "activities": {activity: Counter() for activity in ACTIVITIES},
    }


def parse_activity_and_effect(name):
    activity, separator, effect = name.partition(" - ")
    if not separator:
        return None, None
    return activity, effect


def load_models(folder):
    models = defaultdict(new_model_stats)
    paths = tuple(iter_json_paths(folder))

    worker_count = min(JSON_WORKERS, len(paths)) or 1
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        for model, file_stats in executor.map(load_file_stats, paths):
            merge_model_stats(models[model], file_stats)

    return dict(models)


def load_file_stats(path):
    file_stats = new_model_stats()
    model = path.name.split("_cat", 1)[0]

    with path.open("r", encoding="utf-8") as fp:
        steps = json.load(fp)

    if not steps:
        return model, file_stats

    conclusion_name = steps[-1].get("Name", "")
    conclusion = conclusion_name.rsplit(" - ", 1)[-1]
    conclusion_key = CONCLUSION_TO_KEY.get(conclusion)
    if conclusion_key is not None:
        file_stats[conclusion_key] += 1

    for step in steps[:-1]:
        activity, effect = parse_activity_and_effect(step.get("Name", ""))
        total_key = EFFECT_TO_TOTAL_KEY.get(effect)
        if total_key is None or activity not in file_stats["activities"]:
            continue

        file_stats[total_key] += 1
        file_stats["activities"][activity][total_key] += 1

    return model, file_stats


def merge_model_stats(target_stats, source_stats):
    for key in (
        "conclusion_correct",
        "conclusion_partially_correct",
        "conclusion_incorrect",
        "step_positive_effect",
        "step_indifferent",
        "step_negative_effect",
    ):
        target_stats[key] += source_stats[key]

    for activity in ACTIVITIES:
        target_stats["activities"][activity].update(source_stats["activities"][activity])


def add_derived_statistics(models):
    for stats in models.values():
        total_reasoning_steps = 0

        for activity_stats in stats["activities"].values():
            total = (
                activity_stats["step_positive_effect"]
                + activity_stats["step_negative_effect"]
                + activity_stats["step_indifferent"]
            )
            activity_stats["total"] = total
            total_reasoning_steps += total
            activity_stats["percentage_correct"] = percentage(
                activity_stats["step_positive_effect"], total
            )

        for activity_stats in stats["activities"].values():
            activity_stats["percentage_over_total"] = percentage(
                activity_stats["total"], total_reasoning_steps
            )

        stats["score"] = (
            2.5
            * (
                100 * stats["conclusion_correct"]
                - 100 * stats["conclusion_partially_correct"]
                - 200 * stats["conclusion_incorrect"]
            )
            + (
                10 * stats["step_positive_effect"]
                - stats["step_indifferent"]
                - 20 * stats["step_negative_effect"]
            )
        )


def percentage(numerator, denominator):
    if denominator == 0:
        return 0.0
    return round(float(numerator) / float(denominator) * 100.0, 1)


def format_percentage(value):
    return f"{value:.1f}".rstrip("0").rstrip(".")


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


def ordered_model_names(models):
    ordered_models = [(model, stats["score"]) for model, stats in models.items()]
    ordered_models.sort(key=lambda item: (item[1], item[0]), reverse=True)
    return [model for model, _ in ordered_models]


def build_score_table(models, ordered_models):
    headers = ("Model", "Score", "C", "PC", "W", "PE", "IND", "NE")
    rows = [
        (
            model,
            f"**{int(models[model]['score'])}**",
            models[model]["conclusion_correct"],
            models[model]["conclusion_partially_correct"],
            models[model]["conclusion_incorrect"],
            models[model]["step_positive_effect"],
            models[model]["step_indifferent"],
            models[model]["step_negative_effect"],
        )
        for model in ordered_models
    ]
    return markdown_table(headers, rows, right_align={"C", "PC", "W", "PE", "IND", "NE"})


def build_percentage_table(models, ordered_models, statistic_name):
    headers = ("Model",) + tuple(ACTIVITY_ABBREVIATIONS[activity] for activity in ACTIVITIES)
    rows = []

    for model in ordered_models:
        row = [model]
        activity_stats = models[model]["activities"]
        for activity in ACTIVITIES:
            row.append(format_percentage(activity_stats[activity][statistic_name]))
        rows.append(tuple(row))

    return markdown_table(headers, rows, right_align=set(headers[1:]))


def write_dashboard(models):
    add_derived_statistics(models)
    ordered_models = ordered_model_names(models)

    reasoning_score = build_score_table(models, ordered_models)
    percentage_per_reasoning_type_over_total = build_percentage_table(
        models, ordered_models, "percentage_over_total"
    )
    correctness_per_reasoning_type = build_percentage_table(
        models, ordered_models, "percentage_correct"
    )

    with OUTPUT_FILENAME.open("w", encoding="utf-8") as fp:
        fp.write("# Reasoning Dashboards\n\n")
        fp.write("## Model Scores\n\n")
        fp.write(reasoning_score)
        fp.write(
            "\n\nHere, **C**, **PC**, **W** refer to the number of correct, partially correct, "
            "and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning "
            "steps with positive, indifferent, and negative effect.\n\n"
        )
        fp.write("**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**\n\n")
        fp.write("## Percentage per Reasoning Type over Total\n\n")
        fp.write(percentage_per_reasoning_type_over_total)
        fp.write("\n\n")
        fp.write("Dictionary of activities:\n")
        for activity, abbreviation in ACTIVITY_ABBREVIATIONS.items():
            fp.write(f"* **{abbreviation}** -> {activity}\n")
        fp.write("\n\n")
        fp.write("## Percentage of Correctness per Reasoning Type\n\n")
        fp.write(correctness_per_reasoning_type)
        fp.write("\n")


def main():
    write_dashboard(load_models(FOLDER))


if __name__ == "__main__":
    main()
