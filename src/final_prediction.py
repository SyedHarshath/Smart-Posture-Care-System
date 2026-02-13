import serial
import numpy as np
import joblib  
import time


scaler = joblib.load("scaler_new_posture.pkl")
model = joblib.load("rf_new_posture.pkl")

ser = serial.Serial('COM6', 9600, timeout=1)  

while True:
    try:
        line = ser.readline().decode().strip()
        
        if not line or not any(c.isdigit() or c=='-' or c=='.' for c in line):
            continue

        data = line.split(',')
        if len(data) != 6: 
            continue

        X = np.array([float(x) for x in data]).reshape(1, -1)

        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)

        print("Prediction:", prediction[0])
        time.sleep(0.1)

        if prediction[0] == "bad":
            ser.write(b'1')
        else:
            ser.write(b'0')  

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Error:", e)
