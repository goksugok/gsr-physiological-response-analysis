import csv
import os

INPUT_FOLDER = "final_files"
OUTPUT_FILE = "FINAL_DATASET_FOR_SPSS.csv"

all_rows = []
header_saved = False

for file in sorted(os.listdir(INPUT_FOLDER)):
    if file.endswith(".csv"):
        path = os.path.join(INPUT_FOLDER, file)

        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            print(f"Boş dosya atlandı: {file}")
            continue

        header = rows[0]
        data = rows[1:]

        if not header_saved:
            all_rows.append(header)
            header_saved = True

        all_rows.extend(data)

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(all_rows)

print(f"Bitti: {OUTPUT_FILE} oluşturuldu.")
print(f"Toplam veri satırı: {len(all_rows) - 1}")
