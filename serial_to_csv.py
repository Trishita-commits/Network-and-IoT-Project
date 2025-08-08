import serial
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# -------------------- Serial Port Setup --------------------
ser = serial.Serial('COM3', 115200)  # Change COM port if needed
ser.flush()

# -------------------- CSV Setup --------------------
csv_filename = "sensor_log.csv"
header = ["Time", "Humidity", "Temp", "HeatIndex", "PM2.5", "R", "G", "B", "BacteriaType", "CorrectedPPM"]

with open(csv_filename, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# -------------------- Data Structure --------------------
data = {
    "Humidity": 0.0,
    "Temp": 0.0,
    "HeatIndex": 0.0,
    "PM2.5": 0.0,
    "R": 0,
    "G": 0,
    "B": 0,
    "BacteriaType": "Unknown",
    "CorrectedPPM": 0.0
}

numeric_keys = ["Humidity", "Temp", "HeatIndex", "PM2.5", "R", "G", "B", "CorrectedPPM"]

# -------------------- Plot Setup --------------------
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(numeric_keys, [data[k] for k in numeric_keys], color='skyblue')
value_texts = [ax.text(0, i, '', va='center', fontsize=9) for i in range(len(numeric_keys))]

air_quality_text = ax.text(0.95, 1.05, '', transform=ax.transAxes,
                           ha='right', va='bottom', fontsize=14, weight='bold')
bacteria_text = ax.text(0.5, 1.05, '', transform=ax.transAxes,
                        ha='center', va='bottom', fontsize=14, weight='bold')

ax.set_xlim(0, 1000)  # Adjust depending on your expected range
ax.set_title("Live Sensor Data")

# -------------------- Update Function --------------------
def update(frame):
    global data
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            values = line.split(',')

            if len(values) == 9:
                h, t, hic, pm, r, g, b, bact, ppm = values

                data.update({
                    "Humidity": float(h),
                    "Temp": float(t),
                    "HeatIndex": float(hic),
                    "PM2.5": float(pm),
                    "R": int(r),
                    "G": int(g),
                    "B": int(b),
                    "BacteriaType": bact.strip(),
                    "CorrectedPPM": float(ppm)
                })

                # Append to CSV
                with open(csv_filename, "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        data["Humidity"],
                        data["Temp"],
                        data["HeatIndex"],
                        data["PM2.5"],
                        data["R"],
                        data["G"],
                        data["B"],
                        data["BacteriaType"],
                        data["CorrectedPPM"]
                    ])

                # Update bar widths and text labels
                for i, key in enumerate(numeric_keys):
                    val = data[key]
                    bars[i].set_width(val)
                    value_texts[i].set_position((val + 5, i))
                    value_texts[i].set_text(f"{val:.1f}")

                # Update Air Quality Text
                if data["PM2.5"] > 100 or data["CorrectedPPM"] > 200:
                    air_quality_text.set_text("Air Quality: POOR")
                    air_quality_text.set_color('red')
                else:
                    air_quality_text.set_text("Air Quality: GOOD")
                    air_quality_text.set_color('green')

                # Update Bacteria Type
                bacteria_text.set_text(f"Bacteria: {data['BacteriaType']}")

    except Exception as e:
        print(f"Error: {e}")

# -------------------- Animation --------------------
ani = FuncAnimation(fig, update, interval=1000)
plt.tight_layout()
plt.show()

