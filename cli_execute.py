#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
PIPELINE_SCRIPTS = (
    ("03_trace_identification.py", "--exit-on-no-changes"),
    ("06_ext_validation.py", "--exit-on-no-changes"),
    ("05_statistics_building.py",),
    ("05_2_statistics_category.py",),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute pmllmbench-lrms-reasoning-analysis without model-specific arguments."
    )
    parser.add_argument(
        "--disable-git-clean",
        action="store_true",
        help="Skip git clean during repository preflight. Disabled by default.",
    )
    parser.add_argument("--python", default=sys.executable, help="Python executable for subprocess phases.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing them.")
    return parser


def run_subprocess(command: list[str], cwd: Path, dry_run: bool) -> None:
    print("+", " ".join(command))
    if dry_run:
        return
    subprocess.run(command, cwd=str(cwd), check=True)


def sync_repository(dry_run: bool, disable_git_clean: bool = False) -> None:
    if not (REPO_ROOT / ".git").exists():
        return

    git_commands = [["git", "reset", "--hard", "HEAD"]]
    if disable_git_clean:
        print("# git clean disabled")
    else:
        git_commands.append(["git", "clean", "-x", "-f"])
    git_commands.append(["git", "pull"])
    for command in git_commands:
        run_subprocess(command, cwd=REPO_ROOT, dry_run=dry_run)


def resolve_pm_benchmark_root() -> Path:
    for candidate in (REPO_ROOT.parent / "pm-llm-benchmark", REPO_ROOT / "pm-llm-benchmark"):
        if (candidate / "utils" / "list_lrms.py").is_file():
            return candidate
    raise FileNotFoundError("Could not find pm-llm-benchmark/utils/list_lrms.py next to this repository.")


def refresh_lrm_patterns(python_executable: str, dry_run: bool) -> None:
    pm_root = resolve_pm_benchmark_root()
    source_path = pm_root / "utils" / "lrms_list.txt"
    target_path = REPO_ROOT / "lrms_list.txt"

    run_subprocess([python_executable, "utils/list_lrms.py"], cwd=pm_root, dry_run=dry_run)
    print("+", "cp", str(source_path), str(target_path))
    if not dry_run:
        shutil.copy2(source_path, target_path)


def execute_pipeline(python_executable: str, dry_run: bool) -> None:
    for script_args in PIPELINE_SCRIPTS:
        command = [python_executable, *script_args]
        run_subprocess(command, cwd=REPO_ROOT, dry_run=dry_run)


def publish_results(dry_run: bool) -> None:
    if not (REPO_ROOT / ".git").exists():
        return

    commit_message = "Update pmllmbench-lrms-reasoning-analysis results"
    run_subprocess(["git", "add", "-A"], cwd=REPO_ROOT, dry_run=dry_run)
    if dry_run:
        run_subprocess(["git", "commit", "-m", commit_message], cwd=REPO_ROOT, dry_run=True)
        run_subprocess(["git", "push"], cwd=REPO_ROOT, dry_run=True)
        return

    diff_result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(REPO_ROOT), check=False)
    if diff_result.returncode == 0:
        print("No git changes to commit.")
        return
    if diff_result.returncode not in {0, 1}:
        diff_result.check_returncode()

    run_subprocess(["git", "commit", "-m", commit_message], cwd=REPO_ROOT, dry_run=False)
    run_subprocess(["git", "push"], cwd=REPO_ROOT, dry_run=False)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    sync_repository(args.dry_run, args.disable_git_clean)
    refresh_lrm_patterns(args.python, args.dry_run)
    execute_pipeline(args.python, args.dry_run)
    publish_results(args.dry_run)


if __name__ == "__main__":
    main()
