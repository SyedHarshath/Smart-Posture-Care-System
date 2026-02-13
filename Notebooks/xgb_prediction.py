import time
import joblib
import serial
import numpy as np
from collections import deque

COM_PORT = "COM6"
BAUD = 9600

CALIB_SAMPLES = 30        
SMOOTH_WINDOW = 6         
CLIP_LIMIT = 20.0         
APPLY_OFFSET = True       
THRESHOLD = 0.15         
GOOD_RATIO = 0.70   

model = joblib.load("xgb_new_posture.pkl")
scaler = joblib.load("scaler_xgb_posture.pkl")

ser = serial.Serial(COM_PORT, BAUD, timeout=1)
time.sleep(2) 
label_map = {0: "bad", 1: "good"}
buffer = deque(maxlen=SMOOTH_WINDOW)

print("Starting. Please keep GOOD posture for calibration phase...")

collected = []
while len(collected) < CALIB_SAMPLES:
    try:
        raw = ser.readline().decode(errors='ignore').strip()
        if not raw:
            continue

        parts = [p.strip().replace(' ', '') for p in raw.split(',')]
        if len(parts) != 6:
            continue

        try:
            vals = [float(x) for x in parts]
        except ValueError:
            continue

        collected.append(vals)
        print(f"Calib Samples: {len(collected)}/{CALIB_SAMPLES}")

    except KeyboardInterrupt:
        print("Calibration aborted by user.")
        ser.close()
        raise SystemExit

collected = np.array(collected)
live_mean = collected.mean(axis=0)
train_mean = scaler.mean_
offset = live_mean - train_mean

print("\nCalibration complete.")
print("Live mean:", np.round(live_mean, 3).tolist())
print("Train mean:", np.round(train_mean, 3).tolist())
print("Offset (live - train):", np.round(offset, 3).tolist())
print("-> Offset correction:", "Enabled" if APPLY_OFFSET else "Disabled")
print("Starting real-time monitoring. Press Ctrl+C to stop.\n")

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            time.sleep(0.01)
            continue

        parts = [p.strip().replace(' ', '') for p in line.split(',')]
        if len(parts) != 6:
            continue

        try:
            X = np.array([float(x) for x in parts]).reshape(1, -1)
        except ValueError:
            continue

        X[0, 0] *= -1   
        X[0, 3] *= -1   

        X_corrected = X - offset.reshape(1, -1) if APPLY_OFFSET else X

        X_scaled = scaler.transform(X_corrected)
        X_scaled = np.clip(X_scaled, -CLIP_LIMIT, CLIP_LIMIT)

        proba = model.predict_proba(X_scaled)[0][1]
        pred = int(proba > THRESHOLD)   # 1 = good, 0 = bad

        buffer.append(pred)
        if len(buffer) > 0:
          
            final_pred = 1 if buffer.count(1) >= GOOD_RATIO * len(buffer) else 0
        else:
            final_pred = pred

        posture = label_map[final_pred]

        print("Posture Detected:", posture)

        ser.write(b'1' if posture == "bad" else b'0')

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting gracefully...")

except Exception as e:
    print("Error:", e)

finally:
    ser.close()
    print("Serial connection closed.")
