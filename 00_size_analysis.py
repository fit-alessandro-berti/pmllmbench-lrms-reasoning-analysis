import os

def sum_txt_sizes_by_pattern(directory, patterns):
    """
    For each pattern in `patterns`, sum the sizes of all '.txt' files in `directory`
    that start with the given pattern. Print the result for each pattern.
    """
    for pattern in patterns:
        total_size = 0
        for filename in os.listdir(directory):
            if filename.startswith(pattern) and filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                total_size += os.path.getsize(file_path)
        print(f"Pattern '{pattern}' => total size: {total_size} bytes")


if __name__ == "__main__":
    # Example usage:
    # 1. Replace 'your_directory_path' with the path to the directory containing your files
    # 2. Update the patterns list accordingly
    your_directory_path = r"C:\Users\berti\pm-llm-benchmark\answers"

    # Define the patterns you want to match
    patterns_to_check = [
        "DeepSeek-R1-Distill-Llama-70B",
        "DeepSeek-R1-Distill-Qwen-32B",
        "DeepSeek-R1-Distill-Qwen-14B",
        "QwenQwQ"
    ]

    sum_txt_sizes_by_pattern(your_directory_path, patterns_to_check)
