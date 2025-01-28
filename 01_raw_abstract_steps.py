import os
import sys
import pyperclip
import subprocess

def main(input_folder, pattern, prel_folder):
    """
    For every .txt file in `input_folder` that starts with `pattern`,
    copy "Analyze this content" + file content into the clipboard.
    Then open the corresponding file in `prel_folder` (same filename)
    in Notepad, and wait for the user to edit/save/close before moving on.
    """
    # Ensure the prel_folder exists (create it if it doesn't)
    if not os.path.exists(prel_folder):
        os.makedirs(prel_folder)

    # List and filter matching files
    all_files = os.listdir(input_folder)
    txt_files = [
        f for f in all_files
        if f.startswith(pattern) and f.endswith(".txt")
    ]

    # Process each matching file
    for filename in txt_files:
        input_path = os.path.join(input_folder, filename)

        try:
            f = open(input_path, "r", encoding="utf-8")
            content = f.read()
            f.close()
        except:
            f = open(input_path, "r")
            content = f.read()
            f.close()
        # Read input file content

        content = content.split("<think>")[-1].split("</think>")[0]

        # Prepare clipboard content
        clipboard_content = "Produce a list of the abstract reasoning steps followed in the following trace. Something like deductive reasoning, inductive reasoning, Abductive Reasoning, backtracking, but you decide about that. This should abstract from any reference to the actually solved problem or steps specific to the problem. Suppose I have 100 reasoning traces and I need to analyze them with process mining. So there should be a limited number of labels in the end. Very abstract steps. Please provide a list with just the names, no explanation needed.\n\n" + content

        # Copy to clipboard
        pyperclip.copy(clipboard_content)
        print(f"Copied content of '{filename}' to clipboard with a prepended request.")

        # Build path to corresponding prel file
        prel_path = os.path.join(prel_folder, filename)

        # If the prel file doesn't exist, create it
        if not os.path.exists(prel_path):
            with open(prel_path, "w", encoding="utf-8") as f:
                f.write("")  # create empty file

            # Open in Notepad (blocking call until user closes)
            print(f"Opening '{prel_path}' in Notepad. Please edit, save, and close.")
            subprocess.call(["notepad", prel_path])

        print(f"Finished processing '{filename}'. Moving on...\n")

    print("All matching files have been processed.")

if __name__ == "__main__":
    # Usage (3 arguments, optionally):
    # python script.py <input_folder> <pattern> <prel_folder>
    # Defaults are set if no arguments are provided.

    input_folder = r"C:\Users\berti\pm-llm-benchmark\answers"
    pattern      = "DeepSeek-R1-Distill-Qwen-14B"
    prel_folder  = "prel\\raw_abstract_steps"

    main(input_folder, pattern, prel_folder)
