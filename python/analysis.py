import csv
import os
import re
from typing import List, Dict


OPENSESAME_FOLDER = "opensesame_files"
GSR_FOLDER = "gsr_files"
FIRST_PHOTO_FILE = "first_photo_times.csv"
OUTPUT_FOLDER = "final_files"

WINDOW_SECONDS = 4.0


def read_csv_file(filename: str) -> List[Dict[str, str]]:
    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def to_float(value: str) -> float:
    return float(str(value).strip().replace(",", "."))


def load_gsr_data(gsr_file: str) -> List[Dict[str, float]]:
    rows = read_csv_file(gsr_file)
    data = []

    for row in rows:
        data.append({
            "time": to_float(row["time"]),
            "gsr": to_float(row["gsr"])
        })

    data.sort(key=lambda x: x["time"])
    return data


def get_first_photo_time_for_participant(first_photo_rows, participant_id: int) -> float:
    for row in first_photo_rows:
        if str(row.get("participant", "")).strip() == str(participant_id):
            return to_float(row["gsr_first_photo_time"])

    raise ValueError(f"{participant_id} için first_photo_times.csv içinde zaman bulunamadı.")


def get_first_photo_offset(opensesame_rows, gsr_first_photo_time: float) -> float:
    first_trial_start = to_float(opensesame_rows[0]["time_image_screen"]) / 1000
    offset = gsr_first_photo_time - first_trial_start
    return offset


def get_window_data(gsr_data, start_time: float, end_time: float):
    return [row for row in gsr_data if start_time <= row["time"] <= end_time]


def compute_scr(gsr_data, trial_start_time: float):
    trial_end_time = trial_start_time + WINDOW_SECONDS
    window = get_window_data(gsr_data, trial_start_time, trial_end_time)

    if not window:
        return {
            "baseline_gsr": "",
            "peak_gsr": "",
            "scr": ""
        }

    baseline = window[0]["gsr"]
    peak = max(row["gsr"] for row in window)
    scr = peak - baseline

    return {
        "baseline_gsr": baseline,
        "peak_gsr": peak,
        "scr": scr
    }


def guess_type(image_name: str) -> str:
    name = image_name.lower()
    if "ai" in name:
        return "ai"
    if "real" in name:
        return "real"
    return "unknown"


def get_participant_id_from_subject_file(filename: str) -> int:
    # subject-5.csv → 5
    match = re.search(r"subject-(\d+)", filename)
    if not match:
        raise ValueError(f"Katılımcı numarası okunamadı: {filename}")
    return int(match.group(1))


def process_participant(participant_id: int, opensesame_file: str, gsr_file: str, first_photo_rows):
    opensesame_rows = read_csv_file(opensesame_file)
    gsr_rows = load_gsr_data(gsr_file)

    if not opensesame_rows:
        raise ValueError(f"{opensesame_file} boş")
    if not gsr_rows:
        raise ValueError(f"{gsr_file} boş")

    gsr_first_photo_time = get_first_photo_time_for_participant(first_photo_rows, participant_id)
    offset = get_first_photo_offset(opensesame_rows, gsr_first_photo_time)

    final_rows = []

    for row in opensesame_rows:
        opensesame_start = to_float(row["time_image_screen"]) / 1000
        gsr_trial_start = opensesame_start + offset

        result = compute_scr(gsr_rows, gsr_trial_start)

        final_rows.append({
            "participant": participant_id,
            "trial": row.get("trial_id", ""),
            "image_name": row.get("stimulus", ""),
            "type": guess_type(row.get("stimulus", "")),
            "familiarity": row.get("familiarity", ""),
            "opensesame_start_time": row.get("time_image_screen", ""),
            "gsr_trial_start_time": gsr_trial_start,
            "response": row.get("response", ""),
            "correct": row.get("correct", ""),
            "rt": row.get("response_time", ""),
            "baseline_gsr": result["baseline_gsr"],
            "peak_gsr": result["peak_gsr"],
            "scr": result["scr"]
        })

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(OUTPUT_FOLDER, f"final_{participant_id:03d}.csv")

    fieldnames = [
        "participant",
        "trial",
        "image_name",
        "type",
        "familiarity",
        "opensesame_start_time",
        "gsr_trial_start_time",
        "response",
        "correct",
        "rt",
        "baseline_gsr",
        "peak_gsr",
        "scr"
    ]

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    print(f"Tamam: {output_file} oluşturuldu.")


def main():
    first_photo_rows = read_csv_file(FIRST_PHOTO_FILE)

    for file in sorted(os.listdir(OPENSESAME_FOLDER)):
        if file.endswith(".csv") and file.startswith("subject-"):
            participant_id = get_participant_id_from_subject_file(file)

            opensesame_file = os.path.join(OPENSESAME_FOLDER, file)
            gsr_file = os.path.join(GSR_FOLDER, f"gsr_{participant_id:03d}.csv")

            if not os.path.exists(gsr_file):
                print(f"UYARI: {participant_id} için GSR dosyası bulunamadı: {gsr_file}")
                continue

            process_participant(participant_id, opensesame_file, gsr_file, first_photo_rows)


if __name__ == "__main__":
    main()
