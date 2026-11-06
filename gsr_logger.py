import serial
import time
import csv

# 🔥 Denek numarası al
subject_id = input("Denek numarası gir: ")

# 🔥 Dosya adı oluştur
filename = f"gsr_{subject_id}.csv"

ser = serial.Serial('COM9', 9600)  # COM portunu kontrol et
time.sleep(2)

file = open(filename, 'w', newline='')
writer = csv.writer(file)

writer.writerow(["time", "gsr"])

start_time = time.time()

print(f"Kayıt başladı → {filename}")

while True:
    line = ser.readline().decode().strip()

    if line.isdigit():
        current_time = round(time.time() - start_time, 2)
        writer.writerow([current_time, line])
        print(current_time, line)