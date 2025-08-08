#include "DHT.h"
#include <MQ135.h>
#include <PMsensor.h>
#include <Wire.h>
#include "Adafruit_TCS34725.h"
#define PIN_MQ135 32
#define DHTPIN 14
#define DHTTYPE DHT11 

DHT dht(DHTPIN, DHTTYPE);
MQ135 mq135_sensor(PIN_MQ135);
PMsensor PM;

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_600MS, TCS34725_GAIN_1X);

void setup() {
  Serial.begin(115200);
  dht.begin();
  PM.init(13, 35);
  if (tcs.begin()) {
    Serial.println("TCS34725 found");
  } else {
    Serial.println("No TCS34725 found ... check wiring!");
    while (1);
  }
  

}

void loop() {
  //DHT data
  delay(1000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  float rzero = mq135_sensor.getRZero();
  float correctedRZero = mq135_sensor.getCorrectedRZero(t, h);
  float resistance = mq135_sensor.getResistance();
  float ppm = mq135_sensor.getPPM();
  float correctedPPM1 = mq135_sensor.getCorrectedPPM(t, h);
  float correctedPPM = (correctedPPM1/2500);

  //mq135

  //dht11
  //GP2YDATA
  float filter_Data = PM.read(0.1);
  float noFilter_Data = PM.read();
  float no_filter_actual_Data = noFilter_Data/10;
   uint16_t r, g, b, c;
  tcs.getRawData(&r, &g, &b, &c);

  // Detect dominant color
  String detectedColor = "Unknown";

  if (r > g && r > b) {
    detectedColor = "Bacteria R";
  } else if (g > r && g > b) {
    detectedColor = "Bacteria G";
  } else if (b > r && b > g) {
    detectedColor = "Bacteria B";
  } else{
    detectedColor ="Ambient light only";
  }


  Serial.println("Humidity (%), Temp (°C), Heat Index (°C), PM2.5, R, G, B, Bacteria Type, Corrected PPM");
  Serial.print(h); Serial.print(", ");
  Serial.print(t); Serial.print(", ");
  Serial.print(hic); Serial.print(", ");
  Serial.print(no_filter_actual_Data); Serial.print(", ");
  Serial.print(r); Serial.print(", ");
  Serial.print(g); Serial.print(", ");
  Serial.print(b); Serial.print(", ");
  Serial.print(detectedColor); Serial.print(", ");
  Serial.println(correctedPPM);

  delay(1000);

}

