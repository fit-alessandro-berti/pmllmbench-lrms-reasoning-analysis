from __future__ import annotations

import argparse
import json
import subprocess
import time
import traceback
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple, Union

import pm4py
import pyperclip
from jsonschema import ValidationError, validate


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_PM_BENCHMARK_ROOT = REPO_ROOT.parent / "pm-llm-benchmark"
DEFAULT_QUESTIONS_FOLDER = DEFAULT_PM_BENCHMARK_ROOT / "questions"
DEFAULT_INPUT_FOLDER = DEFAULT_PM_BENCHMARK_ROOT / "answers"
DEFAULT_PREL_FOLDER = Path("prel") / "final_abstract_steps"
DEFAULT_PATTERNS_FILE = Path("lrms_list.txt")
DEFAULT_API_KEY_PATH = Path("../api_openai.txt")

ALLOWED_CATEGORIES = ("cat01", "cat02", "cat03", "cat04", "cat05", "cat06")
REQUEST_MODEL = "gpt-5.4"
API_URL = "https://api.openai.com/v1/"
MAX_WORKERS = 150
SCAN_INTERVAL_SECONDS = 60
MANUAL_MODE = False


@dataclass(frozen=True)
class ProcessingConfig:
    input_folder: Path
    prel_folder: Path
    questions_folder: Path
    api_key_path: Path = DEFAULT_API_KEY_PATH
    allowed_categories: Sequence[str] = ALLOWED_CATEGORIES
    max_workers: int = MAX_WORKERS
    request_model: str = REQUEST_MODEL
    api_url: str = API_URL
    manual_mode: bool = MANUAL_MODE


@dataclass(frozen=True)
class TraceJob:
    filename: str
    model_pattern: str
    input_path: Path
    question_path: Path
    temp_output_path: Path
    final_output_path: Path


PatternInput = Union[str, Sequence[str]]


def read_file_contents(input_path: Union[str, Path]) -> str:
    path = Path(input_path)
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text()

    return extract_thought_content(content)


def extract_thought_content(content: str) -> str:
    for start_tag, end_tag in (("<think>", "</think>"), ("<thought>", "</thought>")):
        if start_tag in content:
            content = content.split(start_tag, 1)[1]
            if end_tag in content:
                content = content.split(end_tag, 1)[0]
    return content


def build_header_string() -> str:
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


def build_schema() -> dict:
    return {
        "type": "array",
        "items": {
            "type": "object",
            "oneOf": [
                {
                    "properties": {
                        "Name": {
                            "type": "string",
                            "pattern": (
                                r"^(Pattern Recognition|Deductive Reasoning|Inductive Reasoning|"
                                r"Abductive Reasoning|Hypothesis Generation|Validation|Backtracking|"
                                r"Ethical or Moral Reasoning|Counterfactual Reasoning|Heuristic Reasoning)"
                                r" - (PE|IND|NE)$"
                            ),
                        },
                        "Text": {"type": "string"},
                    },
                    "required": ["Name", "Text"],
                },
                {
                    "properties": {
                        "Name": {
                            "type": "string",
                            "pattern": r"^Conclusion - (C|PC|W)$",
                        }
                    },
                    "required": ["Name"],
                },
            ],
        },
    }


def load_patterns(patterns_file: Union[str, Path]) -> Tuple[str, ...]:
    with Path(patterns_file).open("r", encoding="utf-8") as f:
        return tuple(line.strip() for line in f if line.strip())


def normalize_patterns(patterns: PatternInput) -> Tuple[str, ...]:
    if isinstance(patterns, str):
        return (patterns,)
    return tuple(pattern for pattern in patterns if pattern)


def read_api_key(api_key_path: Union[str, Path]) -> str:
    return Path(api_key_path).read_text(encoding="utf-8").strip()


def build_prompt(question: str, reasoning_trace: str) -> str:
    return "\n".join(
        [
            build_header_string(),
            "\n\nQuestion:",
            question,
            "\n\nReasoning trace:",
            reasoning_trace,
        ]
    )


def question_filename_for(answer_filename: str) -> str:
    if "_cat" not in answer_filename:
        raise ValueError(f"Cannot derive question filename from '{answer_filename}'")
    return "cat" + answer_filename.split("_cat", 1)[1]


def matching_model_pattern(filename: str, patterns: Sequence[str]) -> Optional[str]:
    for pattern in patterns:
        if filename.startswith(pattern):
            return pattern
    return None


def is_allowed_category(filename: str, allowed_categories: Sequence[str]) -> bool:
    lower_filename = filename.lower()
    return any(category in lower_filename for category in allowed_categories)


def discover_pending_jobs(config: ProcessingConfig, patterns: Sequence[str]) -> Tuple[TraceJob, ...]:
    jobs = []
    for input_path in sorted(config.input_folder.iterdir(), key=lambda path: path.name):
        filename = input_path.name
        if not input_path.is_file() or input_path.suffix != ".txt":
            continue

        model_pattern = matching_model_pattern(filename, patterns)
        if model_pattern is None or not is_allowed_category(filename, config.allowed_categories):
            continue

        final_output_path = config.prel_folder / input_path.with_suffix(".json").name
        if final_output_path.exists():
            continue

        jobs.append(
            TraceJob(
                filename=filename,
                model_pattern=model_pattern,
                input_path=input_path,
                question_path=config.questions_folder / question_filename_for(filename),
                temp_output_path=config.prel_folder / filename,
                final_output_path=final_output_path,
            )
        )

    return tuple(jobs)


def interleave_jobs_by_model(jobs: Sequence[TraceJob]) -> Tuple[TraceJob, ...]:
    grouped_jobs = {}
    for job in jobs:
        grouped_jobs.setdefault(job.model_pattern, deque()).append(job)

    interleaved_jobs = []
    active_models = sorted(grouped_jobs)
    while active_models:
        next_active_models = []
        for model_pattern in active_models:
            model_jobs = grouped_jobs[model_pattern]
            interleaved_jobs.append(model_jobs.popleft())
            if model_jobs:
                next_active_models.append(model_pattern)
        active_models = next_active_models

    return tuple(interleaved_jobs)


def request_trace_identification(prompt: str, api_key: str, config: ProcessingConfig) -> str:
    return pm4py.llm.openai_query(
        prompt,
        api_key=api_key,
        openai_model=config.request_model,
        api_url=config.api_url,
        extra_payload={},
    )


def write_manual_request(prompt: str, job: TraceJob) -> None:
    pyperclip.copy(prompt)
    print(f"Copied content of '{job.filename}' to clipboard with a prepended request.")

    job.temp_output_path.write_text("", encoding="utf-8")
    print(f"Opening '{job.temp_output_path}' in Notepad. Please edit, save, and close.")
    subprocess.call(["notepad", str(job.temp_output_path)])


def extract_json_from_response(raw_response: str) -> str:
    if "```json" not in raw_response:
        raise ValueError(
            "No ```json code fence found in the prel file. "
            "Please include the JSON inside ```json ... ``` fences."
        )

    json_segment = raw_response.split("```json", 1)[1]
    return json_segment.split("```", 1)[0].strip()


def validate_trace_json(contents: object, schema: dict) -> None:
    try:
        validate(instance=contents, schema=schema)
    except ValidationError as e:
        raise ValueError(f"JSON does not validate: {e.message}") from e


def write_final_json(job: TraceJob, contents: object) -> None:
    with job.final_output_path.open("w", encoding="utf-8") as fp:
        json.dump(contents, fp, indent=2, ensure_ascii=False)

    try:
        job.temp_output_path.unlink()
    except FileNotFoundError:
        pass


def process_file_task(job: TraceJob, schema: dict, api_key: str, config: ProcessingConfig) -> None:
    while True:
        try:
            if job.final_output_path.exists():
                print(f"Skipping '{job.filename}' because '{job.final_output_path}' already exists.")
                return

            question = read_file_contents(job.question_path)
            reasoning_trace = read_file_contents(job.input_path)
            prompt = build_prompt(question, reasoning_trace)

            if config.manual_mode:
                write_manual_request(prompt, job)
            else:
                print(f"req {job.model_pattern} {job.filename}")
                response = request_trace_identification(prompt, api_key, config)
                job.temp_output_path.write_text(response, encoding="utf-8")

            raw_response = read_file_contents(job.temp_output_path)
            contents = json.loads(extract_json_from_response(raw_response))
            validate_trace_json(contents, schema)
            write_final_json(job, contents)

            print(f"Validation successful. Final JSON saved as '{job.final_output_path}'.")
            print(f"Finished processing '{job.filename}'. Moving on...\n")
            return

        except Exception:
            traceback.print_exc()
            print(f"Validation or file reading/writing failed for '{job.filename}'. Retrying...")
            time.sleep(2)


def summarize_models(jobs: Iterable[TraceJob]) -> str:
    counts = {}
    for job in jobs:
        counts[job.model_pattern] = counts.get(job.model_pattern, 0) + 1

    return ", ".join(f"{model}: {count}" for model, count in sorted(counts.items()))


def process_pending_files(config: ProcessingConfig, patterns: Sequence[str]) -> int:
    if not patterns:
        print("No model patterns configured.")
        return 0

    config.prel_folder.mkdir(parents=True, exist_ok=True)
    jobs = interleave_jobs_by_model(discover_pending_jobs(config, patterns))
    if not jobs:
        print("No pending matching files found.")
        return 0

    schema = build_schema()
    api_key = "" if config.manual_mode else read_api_key(config.api_key_path)

    print(f"Submitting {len(jobs)} files across {len(set(job.model_pattern for job in jobs))} model(s).")
    print(f"Pending by model: {summarize_models(jobs)}")

    with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        future_to_job = {
            executor.submit(process_file_task, job, schema, api_key, config): job
            for job in jobs
        }

        for future in as_completed(future_to_job):
            future.result()

    print("All matching files have been processed.")
    return len(jobs)


def main(
    input_folder: Union[str, Path],
    patterns: PatternInput,
    prel_folder: Union[str, Path],
    questions_folder: Union[str, Path],
) -> int:
    config = ProcessingConfig(
        input_folder=Path(input_folder),
        prel_folder=Path(prel_folder),
        questions_folder=Path(questions_folder),
    )
    return process_pending_files(config, normalize_patterns(patterns))


def run_loop(
    config: ProcessingConfig,
    patterns_file: Union[str, Path],
    *,
    exit_on_no_changes: bool = False,
) -> None:
    while True:
        patterns = load_patterns(patterns_file)
        processed_count = process_pending_files(config, patterns)
        if processed_count == 0 and exit_on_no_changes:
            print("No pending matching files found, exiting.")
            return
        time.sleep(SCAN_INTERVAL_SECONDS)


def run_forever(config: ProcessingConfig, patterns_file: Union[str, Path]) -> None:
    run_loop(config, patterns_file, exit_on_no_changes=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Identify reasoning trace steps for pending LRM files.")
    parser.add_argument(
        "--exit-on-no-changes",
        action="store_true",
        default=False,
        help="Exit instead of waiting for the next scan when no pending files are found.",
    )
    args = parser.parse_args()

    default_config = ProcessingConfig(
        input_folder=DEFAULT_INPUT_FOLDER,
        prel_folder=DEFAULT_PREL_FOLDER,
        questions_folder=DEFAULT_QUESTIONS_FOLDER,
    )
    run_loop(default_config, DEFAULT_PATTERNS_FILE, exit_on_no_changes=args.exit_on_no_changes)
