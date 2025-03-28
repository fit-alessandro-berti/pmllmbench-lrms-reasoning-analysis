import os
import json
import math
from collections import Counter


def parse_step(step):
    """
    Given a reasoning step dictionary (with key "Name"),
    extract the reasoning type (before the " - ") and the suffix tag (after the " - ").
    For conclusions (which start with "Conclusion"), the type is set as "Conclusion".

    Returns:
        reasoning_type (str): e.g. "Deductive Reasoning" or "Conclusion"
        tag (str): e.g. "PE", "IND", "NE", "C", "PC", "W"
        is_correct (bool): True if tag indicates correctness (PE, C)
        is_incorrect (bool): True if tag indicates incorrectness (NE, W, IND, PC)
    """
    name = step.get("Name", "")
    if name.startswith("Conclusion"):
        parts = name.split(" - ")
        if len(parts) == 2:
            reasoning_type = "Conclusion"
            tag = parts[1].strip()
        else:
            reasoning_type = name
            tag = ""
    else:
        parts = name.split(" - ")
        if len(parts) == 2:
            reasoning_type = parts[0].strip()
            tag = parts[1].strip()
        else:
            reasoning_type = name
            tag = ""
    # Define tags for correctness and incorrectness.
    correct_tags = {"PE", "C"}
    incorrect_tags = {"NE", "W", "IND", "PC"}
    is_correct = tag in correct_tags
    is_incorrect = tag in incorrect_tags
    return reasoning_type, tag, is_correct, is_incorrect


def analyze_transitions(directory, model):
    """
    Iterates over all JSON files in the provided directory whose names start with `model`.
    For each JSON list of reasoning steps, it counts:
      1. The total number of occurrences of each target reasoning type that are incorrect.
      2. The number of times a transition occurs where a correct step is immediately
         followed by an incorrect step.

    Returns:
        A sorted list of tuples:
          (prev_reasoning_type, target_reasoning_type, transition_count, total_target_count, percentage)
        where:
          - transition_count: count of correct -> incorrect transitions.
          - total_target_count: total occurrences of the target reasoning type in an incorrect state.
          - percentage = (transition_count / total_target_count) * 100.

    The sorting uses a composite key: percentage * log(1 + transition_count).
    """
    total_incorrect = Counter()  # Count of each target reasoning type (incorrect occurrences)
    transition_counts = Counter()  # Count of transitions: (prev_type, target_type) for correct->incorrect pairs

    # Iterate over JSON files in the directory.
    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename.startswith(model):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            # Count total incorrect occurrences for each target reasoning type.
            for step in data:
                reasoning_type, tag, is_correct, is_incorrect = parse_step(step)
                if is_incorrect:
                    total_incorrect[reasoning_type] += 1

            # Examine consecutive pairs.
            for i in range(len(data) - 1):
                prev = data[i]
                curr = data[i + 1]
                prev_type, prev_tag, prev_correct, _ = parse_step(prev)
                curr_type, curr_tag, _, curr_incorrect = parse_step(curr)
                if prev_correct and curr_incorrect:
                    transition_counts[(prev_type, curr_type)] += 1

    # Compute percentages for each transition pair.
    transition_data = []
    for (prev_type, target_type), count in transition_counts.items():
        total = total_incorrect.get(target_type, 0)
        if total > 0:
            percentage = (count / total) * 100
            transition_data.append((prev_type, target_type, count, total, percentage))

    # Sort by the product: percentage * ln(1 + frequency), descending.
    transition_data.sort(key=lambda x: x[4] * math.log(1 + x[2]), reverse=True)
    return transition_data


def main():
    # Directory containing the validated JSON logs.
    directory = r"prel\final_abstract_steps"  # Adjust this path as needed.
    model = "QwenQwQ-32B"  # Filter files starting with this model identifier.
    results = analyze_transitions(directory, model)

    if not results:
        print("No valid transitions found.")
    else:
        print("Transition (Prev Type -> Target Type) | Count / Total | Frequency (%)")
        for prev_type, target_type, count, total, perc in results:
            composite_score = perc * math.log(1 + count)
            print(f"{prev_type} -> {target_type}: {count}/{total} ({perc:.2f}%) | Composite Score: {composite_score:.2f}")


if __name__ == "__main__":
    main()
