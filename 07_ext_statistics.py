import os
import json


def count_evaluations(directory):
    # Initialize counts for Y, P, and N.
    counts = {"Y": 0, "P": 0, "N": 0}
    total_steps = 0

    # Iterate over all JSON files in the given directory.
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    evaluation_list = json.load(f)
                    # Each file contains a JSON list of evaluations (each element is "Y", "P", or "N")
                    for evaluation in evaluation_list:
                        if evaluation in counts:
                            counts[evaluation] += 1
                            total_steps += 1
                        else:
                            print(f"Unexpected value '{evaluation}' in file {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return counts, total_steps


def print_percentages(counts, total_steps):
    if total_steps == 0:
        print("No evaluation steps found.")
        return

    percentage_Y = (counts["Y"] / total_steps) * 100
    percentage_P = (counts["P"] / total_steps) * 100
    percentage_N = (counts["N"] / total_steps) * 100

    print(f"Total evaluation steps processed: {total_steps}")
    print(f"Agreed steps (Y): {counts['Y']} ({percentage_Y:.2f}%)")
    print(f"Partially agreed steps (P): {counts['P']} ({percentage_P:.2f}%)")
    print(f"Non-agreed steps (N): {counts['N']} ({percentage_N:.2f}%)")


if __name__ == "__main__":
    # Set the target directory where evaluated JSON files are stored.
    target_directory = r"valid_ext"

    counts, total_steps = count_evaluations(target_directory)
    print_percentages(counts, total_steps)
