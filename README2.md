# PathoSense – IoT-based Fluorescence Biosensing System for Airborne Pathogen Detection

**PathoSense** is a low-cost, IoT-enabled environmental health monitoring system designed for detecting airborne pollutants and pathogens. It integrates multiple sensors with ESP32 and uses optical fluorescence sensing to assess the presence of harmful gases, fine dust particles (PM2.5), and biological contaminants like airborne bacteria.

---

## 🧪 Project Features

- **Gas Detection**: Detects NH3, CO2, smoke, and VOCs using the MQ-135 sensor.
- **Particulate Detection**: Measures PM2.5 using the GP2Y1010AU0F optical dust sensor.
- **Pathogen Detection**: Utilizes fluorescence biosensing with a UV-LED, photodiodes, and the TCS34725 color sensor to detect airborne bacterial signatures.
- **Data Acquisition**: Microcontroller-based data collection via ESP32 using Arduino IDE.
- **Data Processing**: Uses Python libraries to clean, analyze, and visualize sensor readings.

---

## 🧰 Tech Stack

- **Hardware**: ESP32, MQ-135, GP2Y1010AU0F, UV-LEDs, TCS34725, Photodiodes
- **Firmware**: Arduino IDE (ESP32 C/C++ code)
- **Data Analysis**: Python (`pyserial`, `numpy`, `pandas`, `matplotlib`)

---

## 📈 Data Visualization

Sensor readings are captured over serial communication and processed in Python. The pollutants and pathogen levels are then visualized using Matplotlib with real-time and cumulative analysis features.

---

## 📍 Demonstration

This project was presented at **ICCPDM 2025** as a proof-of-concept for a **cost-effective airborne pathogen detection system**, highlighting its potential in:
- Preventing diseases like **tuberculosis** and **asthma**
- Monitoring **indoor and urban air quality**
- Enabling **early detection** of airborne bacterial threats

---

## 🚀 Getting Started

1. Upload the Arduino code to ESP32 via Arduino IDE
2. Connect sensors to respective GPIOs (schematics included)
3. Run the Python script to collect and visualize data:

```bash
pip install pyserial numpy pandas matplotlib
python pathosense_data_logger.py
