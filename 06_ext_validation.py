import json
import os
import traceback
import time
import pm4py  # assumes pm4py.llm.google_query is available


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_evaluation_list(evaluation_list, expected_length):
    """
    Validate that evaluation_list is a JSON list with the same number of items as expected_length,
    and each item is one of "Y", "P", or "N".
    """
    if not isinstance(evaluation_list, list):
        return False
    if len(evaluation_list) != expected_length:
        return False
    for elem in evaluation_list:
        if elem not in ["Y", "P", "N"]:
            return False
    return True


def extract_json_from_response(response_str):
    """
    Extract JSON content from a response string delimited by ```json ... ```.
    If no code fence is found, return the full string.
    """
    if "```json" in response_str:
        json_segment = response_str.split("```json", 1)[1]
        contents_str = json_segment.split("```", 1)[0]
    else:
        contents_str = response_str
    return contents_str.strip()


def evaluate_file(file_path, output_folder, api_key):
    try:
        # Read the validated source JSON of reasoning steps
        source_data = read_json_file(file_path)
        num_steps = len(source_data)

        # Build the evaluation prompt with the instructions and the source JSON.
        reasoning_types = (
            "Pattern Recognition, Deductive Reasoning, Inductive Reasoning, Abductive Reasoning, "
            "Hypothesis Generation, Validation, Backtracking, Ethical or Moral Reasoning, "
            "Counterfactual Reasoning, Heuristic Reasoning, and Conclusion (with suffixes: "
            "' - PE', ' - IND', ' - NE' for reasoning steps; and 'Conclusion - C', 'Conclusion - PC', "
            "'Conclusion - W' for conclusion)."
        )

        prompt = (
                "You are provided with a JSON list of reasoning steps. Each element is an object with keys 'Name' "
                "and optionally 'Text'. The 'Name' indicates the intended reasoning type (one of the following: "
                f"{reasoning_types}) and ends with a suffix that indicates its effect on the final answer "
                "(for reasoning steps: ' - PE' for positive effect, ' - IND' for neutral, or ' - NE' for negative; "
                "for the conclusion step: 'Conclusion - C', 'Conclusion - PC', or 'Conclusion - W').\n\n"
                "For each step, examine whether the provided 'Text' (if present) properly exhibits the reasoning "
                "corresponding to the 'Name'. If the step's text clearly corresponds to the intended reasoning type, "
                "output 'Y'. If it partially corresponds, output 'P'. If it does not, output 'N'.\n\n"
                "Your answer must be a JSON list with exactly the same number of elements as the input list, in order. "
                "Each element should be one of the following single-character strings: 'Y', 'P', or 'N'.\n\n"
                "Do not include any extra text or formatting; output only the JSON list.\n\n"
                "Source JSON:\n"
                + json.dumps(source_data, indent=2)
        )

        evaluation_list = None

        # Continue querying until a valid evaluation JSON is produced.
        while True:
            print(f"Evaluating file: {os.path.basename(file_path)}")
            response = pm4py.llm.openai_query(prompt, api_key=api_key, model="chatgpt-4o-latest")
            json_str = extract_json_from_response(response)
            try:
                evaluation_list = json.loads(json_str)
            except Exception as e:
                print("Failed to parse JSON from response, retrying...", e)
                continue

            if validate_evaluation_list(evaluation_list, num_steps):
                break
            else:
                print("Validation failed: output JSON list length mismatch or contains invalid values. Retrying...")
                time.sleep(1)

        # Save the validated evaluation JSON list to the output folder with the same filename.
        output_path = os.path.join(output_folder, os.path.basename(file_path))
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(evaluation_list, f, indent=2, ensure_ascii=False)
        print(f"Processed file {os.path.basename(file_path)} and saved evaluation to {output_path}")

    except Exception as ex:
        traceback.print_exc()
        print(f"Error processing file: {file_path}")


def main(input_folder, output_folder):
    # Read API key (adjust the path to your API key file as needed)
    api_key_path = "../openai_api.txt"
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()

    # Process each JSON file from the input folder.
    for file in os.listdir(input_folder):
        if file.endswith(".json"):
            file_path = os.path.join(input_folder, file)
            evaluate_file(file_path, output_folder, api_key)
    print("All files have been processed.")


if __name__ == "__main__":
    # Set the input folder (with JSON files produced by the previous script) and the output folder.
    input_folder = r"prel\final_abstract_steps"
    output_folder = r"valid_ext"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    main(input_folder, output_folder)
