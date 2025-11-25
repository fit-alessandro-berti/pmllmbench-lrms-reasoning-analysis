import json
import os
import traceback
import pyperclip
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
import pm4py

# You need to install jsonschema if you haven't already:
# pip install jsonschema
from jsonschema import validate, ValidationError


def read_file_contents(input_path):
    try:
        f = open(input_path, "r", encoding="utf-8")
        content = f.read()
        f.close()
    except:
        f = open(input_path, "r")
        content = f.read()
        f.close()
    # Read input file content
    content = content.split("<think>")[-1].split("</think>")[0].split("<thought>")[-1].split("</thought>")[0]
    return content


def build_header_string():
    return """
Produce a JSON containing the ordered list of abstract reasoning steps followed in the provided text.
The list should include dictionaries having two keys:
- Name: the name of the activity.
- Text: the portion of text that is corresponding to the activity.

The name of the activity should start exclusively with one of these patterns:
- Pattern Recognition
- Deductive Reasoning
- Inductive Reasoning
- Abductive Reasoning
- Hypothesis Generation
- Validation
- Backtracking
- Ethical or Moral Reasoning
- Counterfactual Reasoning
- Heuristic Reasoning

And end exclusively with one of these patterns:
- PE: positive effect on the final answer and the overall correctness
- IND: neutral effect on the final answer and the overall correctness
- NE: negative effect on the final answer and the overall correctness

So, for example, "Backtracking - PE" or "Counterfactual Reasoning - IND".

At the end, introduce an artificial "Conclusion" activity, followed by one of these
suffixes: C (correct), PC (partially correct), W (substantially incorrect, wrong).
The conclusion should evaluate the correctness of the overall text,
so don't include any corresponding text.
The name of the activity can be:
- Conclusion - C
- Conclusion - PC
- Conclusion - W

AVOID reporting any strange characters inside the strings in the final JSON. Report only alphanumeric characters!

AVOID any escaping, so no quotation characters at all inside the strings of the final JSON! Try to make sure that every string is properly terminated!
            
Be careful to introduce the JSON in the tags ```json and ```

The JSON should look like:
```json
[
    {
        "Name": "Backtracking - PE",
        "Text": "..."
    },
    {
        "Name": "Counterfactual Reasoning - IND",
        "Text": "..."
    },
    {
        "Name": "Conclusion - C"
    }
]
```
"""


def process_file_task(filename, input_folder, prel_folder, questions_folder, schema, api_key):
    header_stri = build_header_string()
    prel_path = os.path.join(prel_folder, filename)
    input_path = os.path.join(input_folder, filename)
    question_path = os.path.join(questions_folder, "cat" + filename.split("_cat")[1])

    while True:
        try:
            question = read_file_contents(question_path)
            reasoning_trace = read_file_contents(input_path)

            clipboard_content = "\n".join([
                header_stri,
                "\n\nQuestion:",
                question,
                "\n\nReasoning trace:",
                reasoning_trace
            ])

            if False:
                # Copy to clipboard
                pyperclip.copy(clipboard_content)

                print(f"Copied content of '{filename}' to clipboard with a prepended request.")

                with open(prel_path, "w", encoding="utf-8") as f:
                    f.write("")  # create empty file

                # Open in Notepad (blocking call until user closes)
                print(f"Opening '{prel_path}' in Notepad. Please edit, save, and close.")
                subprocess.call(["notepad", prel_path])
            else:
                print("req")
                resp = pm4py.llm.openai_query(
                    clipboard_content,
                    api_key=api_key,
                    openai_model="grok-4-1-fast-reasoning",
                    api_url="https://api.x.ai/v1/"
                )
                with open(prel_path, "w", encoding="utf-8") as f:
                    f.write(resp)

            # Extract the JSON from the prel file (delimited by ```json ... ```).
            # Be careful to pick the correct segment if multiple code fences exist.
            raw_prel = read_file_contents(prel_path)
            if "```json" in raw_prel:
                # Split at the first occurrence after ```json
                json_segment = raw_prel.split("```json", 1)[1]
                # Then split at the first triple backticks after that
                contents_str = json_segment.split("```", 1)[0]
            else:
                raise ValueError(
                    "No ```json code fence found in the prel file. "
                    "Please include the JSON inside ```json ... ``` fences."
                )

            # Load the JSON
            contents = json.loads(contents_str)

            # Validate against the JSON schema
            try:
                validate(instance=contents, schema=schema)
            except ValidationError as e:
                # Raise a specific exception if validation fails
                raise Exception(f"JSON does not validate: {e.message}")

            # If validation succeeds, rename prel_path to .json extension
            new_prel_path = prel_path.replace(".txt", ".json")
            os.rename(prel_path, new_prel_path)

            # Write out the validated JSON in the new file
            with open(new_prel_path, "w", encoding="utf-8") as fp:
                json.dump(contents, fp, indent=2, ensure_ascii=False)

            print(f"Validation successful. Final JSON saved as '{new_prel_path}'.")
            print(f"Finished processing '{filename}'. Moving on...\n")
            return

        except Exception as ex:
            traceback.print_exc()
            print(f"Validation or file reading/writing failed for '{filename}'. Retrying...")
            time.sleep(2)


def main(input_folder, pattern, prel_folder, questions_folder):
    # JSON Schema to validate the final structure.
    # We expect an array of objects. Each object can be either:
    #    1) A normal reasoning step, where "Name" matches one of the
    #       known reasoning patterns, followed by " - PE", " - IND", or " - NE".
    #    2) The "Conclusion" step, with "Name" matching "Conclusion - C",
    #       "Conclusion - PC", or "Conclusion - W".
    #
    # The field "Corresponding text" must be a string for both types of items.
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "oneOf": [
                {
                    # Reasoning step pattern
                    "properties": {
                        "Name": {
                            "type": "string",
                            "pattern": (
                                r"^(Pattern Recognition|Deductive Reasoning|Inductive Reasoning|"
                                r"Abductive Reasoning|Hypothesis Generation|Validation|Backtracking|"
                                r"Ethical or Moral Reasoning|Counterfactual Reasoning|Heuristic Reasoning)"
                                r" - (PE|IND|NE)$"
                            )
                        },
                        "Text": {"type": "string"}
                    },
                    "required": ["Name", "Text"]
                },
                {
                    # Conclusion pattern
                    "properties": {
                        "Name": {
                            "type": "string",
                            "pattern": r"^Conclusion - (C|PC|W)$"
                        }
                    },
                    "required": ["Name"]
                }
            ]
        }
    }

    # List and filter matching files
    all_files = os.listdir(input_folder)
    txt_files = [
        f for f in all_files
        if f.startswith(pattern) and f.endswith(".txt")
    ]

    allowed = ["cat01", "cat02", "cat03", "cat04", "cat05", "cat06"]
    api_key = open("../api_grok.txt", "r").read()
    os.makedirs(prel_folder, exist_ok=True)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for filename in txt_files:
            if not any(p in filename.lower() for p in allowed):
                continue

            # Build path to corresponding prel file
            prel_path = os.path.join(prel_folder, filename)

            # If the prel file doesn't exist, create it
            if not os.path.exists(prel_path) and not os.path.exists(prel_path.replace(".txt", ".json")):
                futures.append(
                    executor.submit(
                        process_file_task,
                        filename,
                        input_folder,
                        prel_folder,
                        questions_folder,
                        schema,
                        api_key
                    )
                )

        for future in futures:
            future.result()

    print("All matching files have been processed.")


if __name__ == "__main__":
    # Usage (3 arguments, optionally):
    # python script.py <input_folder> <pattern> <prel_folder>
    # Defaults are set if no arguments are provided.

    questions_folder = r"C:\Users\berti\pm-llm-benchmark\questions"
    input_folder = r"C:\Users\berti\pm-llm-benchmark\answers"
    prel_folder = r"prel\final_abstract_steps"

    F = open("lrms_list.txt", "r")
    patterns = [x.strip() for x in F.readlines()]
    F.close()

    while True:
        for pattern in patterns:
            main(input_folder, pattern, prel_folder, questions_folder)
        #break
        time.sleep(60)
