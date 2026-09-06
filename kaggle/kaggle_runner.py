"""
QUANT RESEARCH AUTOMATION - KAGGLE EXECUTION RUNNER

This file is intentionally kept small.

The actual research code lives in GitHub.
This runner exists only to tell the Kaggle execution
environment which GitHub Python program to execute.

GitHub = source of truth
Kaggle = remote computation environment
"""

from pathlib import Path
import json
import os
import runpy
import shutil
import sys
import traceback
from datetime import datetime, timezone


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# The main GitHub program that Kaggle will execute.
MAIN_PROGRAM = PROJECT_ROOT / "hello.py"

# Kaggle's working/output directory.
KAGGLE_WORKING = Path("/kaggle/working")

# Directory where we will place persistent result files.
RESULTS_DIR = KAGGLE_WORKING / "quant_results"


# ============================================================
# START
# ============================================================

print("=" * 80)
print("QUANT RESEARCH AUTOMATION")
print("KAGGLE EXECUTION ENGINE")
print("=" * 80)

print()
print("Execution time:")
print(datetime.now(timezone.utc).isoformat())

print()
print("Python:")
print(sys.version)

print()
print("Python executable:")
print(sys.executable)

print()
print("Project root:")
print(PROJECT_ROOT)

print()
print("Kaggle working directory:")
print(KAGGLE_WORKING)

print()
print("-" * 80)
print("FILES AVAILABLE TO KAGGLE")
print("-" * 80)

for path in sorted(PROJECT_ROOT.rglob("*")):

    if path.is_file():

        relative = path.relative_to(PROJECT_ROOT)

        # Avoid displaying excessively large/unnecessary files.
        if ".git" not in relative.parts:

            print(relative)


# ============================================================
# CHECK MAIN PROGRAM
# ============================================================

print()
print("-" * 80)
print("CHECKING MAIN GITHUB PROGRAM")
print("-" * 80)

if not MAIN_PROGRAM.exists():

    raise FileNotFoundError(
        f"Main GitHub program was not found: {MAIN_PROGRAM}"
    )

print(f"Found: {MAIN_PROGRAM}")


# ============================================================
# PREPARE RESULT DIRECTORY
# ============================================================

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print()
print(f"Results directory: {RESULTS_DIR}")


# ============================================================
# COPY IMPORTANT SOURCE FILES INTO KAGGLE OUTPUT
# ============================================================

print()
print("-" * 80)
print("COPYING SOURCE/CONFIGURATION FILES")
print("-" * 80)

files_to_copy = [
    PROJECT_ROOT / "hello.py",
    PROJECT_ROOT / "parameters.json",
    PROJECT_ROOT / "leaderboard.csv",
]

for source in files_to_copy:

    if source.exists():

        destination = RESULTS_DIR / source.name

        shutil.copy2(
            source,
            destination
        )

        print(f"Copied: {source.name}")


# ============================================================
# RUN THE REAL GITHUB PROGRAM
# ============================================================

print()
print("=" * 80)
print("EXECUTING GITHUB CODE ON KAGGLE")
print("=" * 80)

execution_successful = False

try:

    # runpy executes hello.py as if it were run directly.
    #
    # Therefore:
    #
    # GitHub hello.py
    #        ↓
    # Kaggle
    #        ↓
    # runpy
    #        ↓
    # actual program
    #
    runpy.run_path(
        str(MAIN_PROGRAM),
        run_name="__main__"
    )

    execution_successful = True

    print()
    print("=" * 80)
    print("GITHUB PROGRAM COMPLETED SUCCESSFULLY")
    print("=" * 80)

except Exception as error:

    print()
    print("=" * 80)
    print("GITHUB PROGRAM FAILED")
    print("=" * 80)

    print()
    print("ERROR:")
    print(error)

    print()
    print("TRACEBACK:")
    traceback.print_exc()


# ============================================================
# CREATE EXECUTION SUMMARY
# ============================================================

summary = {
    "execution_successful": execution_successful,
    "execution_time_utc": datetime.now(timezone.utc).isoformat(),
    "python_version": sys.version,
    "python_executable": sys.executable,
    "main_program": str(MAIN_PROGRAM),
    "kaggle_working_directory": str(KAGGLE_WORKING),
}


summary_file = RESULTS_DIR / "kaggle_execution_summary.json"

with open(
    summary_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        summary,
        file,
        indent=4
    )


# ============================================================
# DISPLAY RESULT FILES
# ============================================================

print()
print("=" * 80)
print("KAGGLE RESULT FILES")
print("=" * 80)

for path in sorted(RESULTS_DIR.rglob("*")):

    if path.is_file():

        print(
            f"{path.relative_to(RESULTS_DIR)}"
        )


# ============================================================
# FINAL STATUS
# ============================================================

print()
print("=" * 80)

if execution_successful:

    print("KAGGLE EXECUTION: SUCCESS")
    print()
    print("GitHub code was successfully executed on Kaggle.")

else:

    print("KAGGLE EXECUTION: FAILED")
    print()
    print("GitHub code could not be completed.")

print("=" * 80)


# Make GitHub Actions/Kaggle aware of failure.
if not execution_successful:

    raise RuntimeError(
        "The GitHub research program failed during Kaggle execution."
    )
