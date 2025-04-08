import os
import json
import pandas as pd
import re # Import regex for more robust category extraction

# --- Configuration ---
folder = "prel/final_abstract_steps"  # Folder containing the JSON files
output_filename = "category_reasoning_percentage.md" # Output Markdown file name
categories_to_process = ["cat01", "cat02", "cat03", "cat04", "cat05", "cat06"]

# Define the types of reasoning activities
activities = [
    "Pattern Recognition",
    "Deductive Reasoning",
    "Inductive Reasoning",
    "Abductive Reasoning",
    "Hypothesis Generation",
    "Validation",
    "Backtracking",
    "Ethical or Moral Reasoning",
    "Counterfactual Reasoning",
    "Heuristic Reasoning"
]

# Dictionary for abbreviations used in the table header
act_dictio = {
    "Pattern Recognition": "P.R.",
    "Deductive Reasoning": "D.R.",
    "Inductive Reasoning": "I.R.",
    "Abductive Reasoning": "A.R.",
    "Hypothesis Generation": "H.G.",
    "Validation": "V",
    "Backtracking": "B",
    "Ethical or Moral Reasoning": "E.R.",
    "Counterfactual Reasoning": "C.R.",
    "Heuristic Reasoning": "H.R."
}

# --- Data Initialization ---
category_data = {}
# Initialize data structure for each category
for cat in categories_to_process:
    category_data[cat] = {
        "total_steps": 0,
        "activity_counts": {act: 0 for act in activities}
    }

# --- File Processing ---
print(f"Processing files in folder: {folder}")
try:
    all_files = [f for f in os.listdir(folder) if f.endswith(".json")]
    print(f"Found {len(all_files)} JSON files.")
except FileNotFoundError:
    print(f"Error: Folder not found: {folder}")
    exit()

processed_files_count = 0
skipped_files = []

for filename in all_files:
    # Extract category from filename (e.g., "model_cat01_xyz.json")
    match = re.search(r'_(cat\d{2})_', filename)
    if match:
        category = match.group(1)
        if category not in categories_to_process:
            # print(f"Skipping file: Category '{category}' not in categories_to_process list ({filename})")
            skipped_files.append(f"{filename} (Category not targeted)")
            continue
    else:
        # print(f"Skipping file: Could not extract category from filename ({filename})")
        skipped_files.append(f"{filename} (Category pattern not found)")
        continue

    file_path = os.path.join(folder, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list) or not data:
            # print(f"Skipping file: Invalid or empty JSON content ({filename})")
            skipped_files.append(f"{filename} (Invalid/empty JSON)")
            continue

        # Process steps (exclude the final conclusion step)
        step_count_in_file = 0
        for i in range(len(data) - 1):
            step = data[i]
            if not isinstance(step, dict) or "Name" not in step:
                 # print(f"Warning: Skipping invalid step format in {filename}, step index {i}")
                 continue

            # Extract activity name (part before " - ")
            try:
                activity_name = step["Name"].split(" - ")[0].strip()
            except IndexError:
                # print(f"Warning: Could not parse activity name from step '{step['Name']}' in {filename}. Skipping step.")
                continue

            if activity_name in activities:
                category_data[category]["total_steps"] += 1
                category_data[category]["activity_counts"][activity_name] += 1
                step_count_in_file += 1
            # else:
            #     print(f"Warning: Unknown activity '{activity_name}' found in {filename}. Skipping step.")

        if step_count_in_file > 0:
             processed_files_count += 1
        # else:
        #      print(f"Note: No valid steps found or processed in file {filename}")


    except json.JSONDecodeError:
        # print(f"Skipping file: Invalid JSON format ({filename})")
        skipped_files.append(f"{filename} (JSON Decode Error)")
    except Exception as e:
        # print(f"Skipping file: An unexpected error occurred ({filename}): {e}")
        skipped_files.append(f"{filename} (Error: {e})")

print(f"\nProcessed {processed_files_count} files containing valid steps.")
if skipped_files:
    print(f"Skipped {len(skipped_files)} files:")
    # for skipped in skipped_files:
    #     print(f"  - {skipped}") # Optionally print details

# --- Calculate Percentages ---
results_table_data = []
for cat in categories_to_process: # Iterate in the defined order
    data = category_data[cat]
    total_steps = data["total_steps"]
    row = {"Category": cat} # Start row dictionary with category name

    if total_steps > 0:
        for act in activities:
            count = data["activity_counts"][act]
            percentage = (count / total_steps) * 100.0
            # Store percentage formatted to one decimal place
            row[act_dictio[act]] = f"{percentage:.1f}"
    else:
        # Handle categories with zero steps
        for act in activities:
            row[act_dictio[act]] = "0.0" # Represent as 0.0 if no steps

    results_table_data.append(row)

# --- Create Pandas DataFrame ---
df = pd.DataFrame(results_table_data)

# Ensure columns are in the desired order: Category first, then activities
column_order = ["Category"] + [act_dictio[act] for act in activities]
df = df[column_order]

# --- Generate Markdown Output ---
markdown_table = df.to_markdown(index=False, floatfmt=".1f") # Use floatfmt for consistency

# --- Write Output File ---
try:
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("# Reasoning Steps Percentage by Category\n\n")
        f.write("This table shows the percentage distribution of different reasoning steps within each question category.\n")
        f.write("Each cell represents the percentage of steps corresponding to the reasoning type (column) out of the total steps counted for that category (row).\n\n")
        f.write(markdown_table)
        f.write("\n\n")
        f.write("## Activity Legend\n\n")
        # Sort abbreviations alphabetically for readability
        sorted_abbr = sorted(act_dictio.items(), key=lambda item: item[1])
        for act, abbr in sorted_abbr:
            f.write(f"* **{abbr}**: {act}\n")

    print(f"\nSuccessfully created Markdown report: '{output_filename}'")

except IOError as e:
    print(f"Error writing output file '{output_filename}': {e}")
except Exception as e:
    print(f"An unexpected error occurred during file writing: {e}")
