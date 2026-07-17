import argparse
import json
import os
import traceback
import time
import pm4py  # assumes pm4py.llm.google_query is available
from concurrent.futures import ThreadPoolExecutor
from file_utils import read_file_with_fallback


DEFAULT_API_KEY_PATH = "../api_grok.txt"
DEFAULT_API_KEY_ENV_VAR = "GROK_API_KEY"


def read_json_file(file_path):
    return json.loads(read_file_with_fallback(file_path))


def read_api_key(
    api_key_path=DEFAULT_API_KEY_PATH,
    api_key_env_var=DEFAULT_API_KEY_ENV_VAR,
):
    api_key = os.environ.get(api_key_env_var, "").strip()
    if api_key:
        return api_key

    return read_file_with_fallback(api_key_path).strip()


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
            response = pm4py.llm.openai_query(prompt,
                                              api_key=api_key,
                                              api_url="https://api.x.ai/v1",
                                              openai_model="grok-4.20-non-reasoning",
                                              extra_payload={})
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
    # Process each JSON file from the input folder using a thread pool.
    json_files = [
        file for file in os.listdir(input_folder)
        if file.endswith(".json")
    ]

    pending_files = []
    for file in json_files:
        output_path = os.path.join(output_folder, file)
        if os.path.exists(output_path):
            continue
        pending_files.append(file)

    if not pending_files:
        print("No pending JSON files found.")
        return 0

    # Read API key only when there is work to submit.
    api_key = read_api_key()

    with ThreadPoolExecutor(max_workers=150) as executor:
        futures = []
        for file in pending_files:
            file_path = os.path.join(input_folder, file)
            futures.append(executor.submit(evaluate_file, file_path, output_folder, api_key))

        for future in futures:
            future.result()
    print("All files have been processed.")
    return len(futures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate pending extracted reasoning-step JSON files.")
    parser.add_argument(
        "--exit-on-no-changes",
        action="store_true",
        default=False,
        help="Exit instead of waiting for the next scan when no pending files are found.",
    )
    args = parser.parse_args()

    # Set the input folder (with JSON files produced by the previous script) and the output folder.
    input_folder = os.path.join("prel", "final_abstract_steps")
    output_folder = r"valid_ext"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while True:
        processed_count = main(input_folder, output_folder)
        if processed_count == 0 and args.exit_on_no_changes:
            print("No pending JSON files found, exiting.")
            break
        time.sleep(60)
