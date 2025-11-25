import json
import os
import traceback
import time
import pm4py  # assumes pm4py.llm.google_query is available
from concurrent.futures import ThreadPoolExecutor


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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
    output_path = os.path.join(output_folder, os.path.basename(file_path))

    while True:
        try:
            if os.path.exists(output_path):
                return

            # Read the validated source JSON of reasoning steps
            source_data = read_json_file(file_path)

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

            print(f"Evaluating file: {os.path.basename(file_path)}")
            response = pm4py.llm.openai_query(prompt, api_key=api_key, openai_model="gpt-5-nano")
            json_str = extract_json_from_response(response)
            evaluation_list = json.loads(json_str)
            evaluation_list = [x for x in evaluation_list if x in ["Y", "P", "N"]]

            # Save the validated evaluation JSON list to the output folder with the same filename.
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_list, f, indent=2, ensure_ascii=False)
            print(f"Processed file {os.path.basename(file_path)} and saved evaluation to {output_path}")
            return

        except Exception as ex:
            traceback.print_exc()
            print(f"Error processing file: {file_path}. Retrying...")
            time.sleep(2)


def main(input_folder, output_folder):
    # Read API key (adjust the path to your API key file as needed)
    api_key_path = "../api_openai.txt"
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()

    # Process each JSON file from the input folder using a thread pool.
    json_files = [
        file for file in os.listdir(input_folder)
        if file.endswith(".json")
    ]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for file in json_files:
            output_path = os.path.join(output_folder, file)
            if os.path.exists(output_path):
                continue
            file_path = os.path.join(input_folder, file)
            futures.append(executor.submit(evaluate_file, file_path, output_folder, api_key))

        for future in futures:
            future.result()
    print("All files have been processed.")


if __name__ == "__main__":
    # Set the input folder (with JSON files produced by the previous script) and the output folder.
    input_folder = r"prel\final_abstract_steps"
    output_folder = r"valid_ext"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while True:
        main(input_folder, output_folder)
        #break
        time.sleep(60)
