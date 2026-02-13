import serial
import pandas as pd
import time

ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)

label = input("Enter posture label (good/bad): ")

data = []

print("Collecting data... Sit in posture. Press Ctrl+C to stop.")
try:
    while True:
        line = ser.readline().decode().strip()
        if line:
            vals = line.split(',')
            if len(vals) == 6:
                ax, ay, az, gx, gy, gz = map(float, vals)
                data.append([ax, ay, az, gx, gy, gz, label])
except KeyboardInterrupt:
    df = pd.DataFrame(data, columns=['ax','ay','az','gx','gy','gz','label'])
    filename = f"posture_data_new_{label}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")
