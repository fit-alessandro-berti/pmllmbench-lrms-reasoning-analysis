import os
import pyperclip
from file_utils import read_file_with_fallback


def merge_txt_files(folder_path, delimiter="\n\n---\n\n"):
    # Initialize the final content with the request
    final_content = "From the following list of raw, preliminary activities, can you identify a coherent set of activities for process mining? They should be limited in number and occur in different traces. Just the list of activities please.\n\n"

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Process only .txt files
        if filename.endswith(".txt"):
            input_path = os.path.join(folder_path, filename)
            content = read_file_with_fallback(input_path)

            # Append file content to the final content with the delimiter
            final_content += content + delimiter

    # Remove the last delimiter if added
    if final_content.endswith(delimiter):
        final_content = final_content[:-len(delimiter)]

    return final_content


# Example usage:
if __name__ == "__main__":
    folder_path = r"prel\raw_abstract_steps"
    delimiter = "\n\n---\n\n"
    merged_content = merge_txt_files(folder_path, delimiter)

    pyperclip.copy(merged_content)
