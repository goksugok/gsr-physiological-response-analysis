"""Run the archived CSV pipeline on fabricated example data."""
from pathlib import Path
import csv
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
source = root / "examples" / "synthetic"
with tempfile.TemporaryDirectory(prefix="gsr-demo-") as temp:
    work = Path(temp)
    shutil.copytree(source / "opensesame_files", work / "opensesame_files")
    shutil.copytree(source / "gsr_files", work / "gsr_files")
    shutil.copy2(source / "first_photo_times.csv", work / "first_photo_times.csv")
    for script in ("analysis.py", "merge_final.py"):
        subprocess.run([sys.executable, str(root / "python" / script)], cwd=work, check=True)
    out = work / "FINAL_DATASET_FOR_SPSS.csv"
    with out.open(newline="", encoding="utf-8-sig") as f:
        records = list(csv.DictReader(f))
    assert len(records) == 4, f"Expected four synthetic trials, got {len(records)}"
    assert all(row["scr"] != "" for row in records)
    print(f"Demo passed: {len(records)} synthetic trials processed. No participant data used.")
