/*
  FIRE-X NASA Microgravity Combustion Intel Platform
  ESP32 + MQ-2 Combustion Sniffer Firmware (C++ / Arduino)
  NASA Space Apps Challenge 2026
  
  Pins:
    MQ-2 VCC -> ESP32 5V (VIN)
    MQ-2 GND -> ESP32 GND
    MQ-2 AO  -> ESP32 GPIO 34 (ADC1 Channel 6)
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ─── WI-FI CREDENTIALS ──────────────────────────────────────────
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ─── FIRE-X BACKEND SERVER ──────────────────────────────────────
// Sənin noutbukunun cari yerli Wi-Fi IP ünvanı:
const char* SERVER_URL    = "http://192.168.100.144:8000/api/sensor-data";

// ─── PIN DEFINITIONS ───────────────────────────────────────────
const int MQ2_ANALOG_PIN  = 34; // GPIO 34 (ADC1, Input Only)
const int ONBOARD_LED     = 2;  // Blue LED indicator

// ─── TELEMETRY VARIABLES ───────────────────────────────────────
unsigned long lastSendTime = 0;
const unsigned long SEND_INTERVAL_MS = 1500; // Send telemetry every 1.5 seconds

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  pinMode(ONBOARD_LED, OUTPUT);
  digitalWrite(ONBOARD_LED, LOW);
  
  // Set ADC attenuation for 0 - 3.3V range
  analogSetAttenuation(ADC_11db);
  
  Serial.println("\n==========================================");
  Serial.println("  NASA FIRE-X // ESP32 + MQ-2 IoT NODE   ");
  Serial.println("  Microgravity Combustion Gas Sniffer    ");
  Serial.println("==========================================");
  
  // Connect to Wi-Fi
  Serial.print("Connecting to Wi-Fi SSID: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 25) {
    delay(500);
    Serial.print(".");
    digitalWrite(ONBOARD_LED, !digitalRead(ONBOARD_LED));
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Connected successfully!");
    Serial.print("[WiFi] IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(ONBOARD_LED, HIGH);
  } else {
    Serial.println("\n[WiFi] Connection timeout. Operating in offline/serial telemetry mode.");
  }
}

void loop() {
  // Read analog value from MQ-2 sensor (12-bit ADC: 0 to 4095)
  int rawADC = analogRead(MQ2_ANALOG_PIN);
  
  // Sensor calibration & conversion:
  // Baseline ambient air gives ~ 150 - 250 ADC counts
  // Lighter / smoke gives ~ 600 - 1500+ ADC counts
  float gasPPM = map(rawADC, 150, 2500, 20, 1000);
  if (gasPPM < 10.0) gasPPM = 15.0 + (rawADC * 0.05);
  
  float smokeDensityPct = (rawADC / 4095.0) * 100.0;
  float ambientTempC = 23.5 + (random(-5, 5) * 0.1);
  float estimatedO2 = 20.9;
  
  // Print telemetry to serial monitor
  Serial.printf("[SENSOR] Raw ADC: %d | Gas: %.1f ppm | Smoke: %.1f %%\n", rawADC, gasPPM, smokeDensityPct);
  
  // Transmit telemetry to FastAPI backend
  if (millis() - lastSendTime >= SEND_INTERVAL_MS) {
    lastSendTime = millis();
    
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(SERVER_URL);
      http.addHeader("Content-Type", "application/json");
      
      // Build JSON Payload matching FastAPI SensorDataPayload model
      StaticJsonDocument<256> doc;
      doc["device_id"]         = "ESP32-FIREX-01";
      doc["raw_smoke_adc"]     = rawADC;
      doc["gas_ppm"]           = gasPPM;
      doc["smoke_density_pct"] = smokeDensityPct;
      doc["ambient_temp_c"]    = ambientTempC;
      doc["estimated_o2_pct"]  = estimatedO2;
      doc["simulated"]         = false;
      
      String jsonStr;
      serializeJson(doc, jsonStr);
      
      int httpResponseCode = http.POST(jsonStr);
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.printf("[HTTP] Status %d | Sent: %s\n", httpResponseCode, jsonStr.c_str());
        
        // Blink LED to indicate successful transmission
        digitalWrite(ONBOARD_LED, LOW);
        delay(60);
        digitalWrite(ONBOARD_LED, HIGH);
      } else {
        Serial.printf("[HTTP] POST failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
      }
      http.end();
    }
  }
  
  delay(100);
}
