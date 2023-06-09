#include <Arduino.h>
#include <SimpleDHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "HX711.h"

#define pumpPin 5
#define dirtPin 34
int pinDHT11 = 4;

const int LOADCELL_DOUT_PIN = 32;
const int LOADCELL_SCK_PIN = 33;
const double factor = (-195000.0)/500.0;
const int dry = 2500;

HX711 scale;
HTTPClient http;
SimpleDHT11 dht11(pinDHT11);

//const char* ssid = "CHT WI-FI Auto";
const char* ssid = "MSI 9243";
const char* password = "0963920068";
const char* serverName = "https://aiot-server-shsjao25ha-de.a.run.app/data";
const char* serverName_2 = "https://aiot-server-shsjao25ha-de.a.run.app/lstm";

const char* root_ca = "-----BEGIN CERTIFICATE-----\n" \
    "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\n" \
    "bP6MvPJwNQzcmRk13NfIRmPVNnGuV/u3gm3c\n" \
    "-----END CERTIFICATE-----\n";

void setup() {
  pinMode(pumpPin, OUTPUT);
  pinMode(dirtPin, OUTPUT);
  digitalWrite(pumpPin, LOW);
  Serial.begin(115200);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  Serial.println("Sample WH-080...");
  int DirtSensorValue = analogRead(dirtPin);
  Serial.print("Dirt humidity sensor value: ");
  Serial.println((int)DirtSensorValue);

  double leak = 0.0;

  if(DirtSensorValue >= dry) {
    if (scale.is_ready()) {
      scale.set_scale(factor);
      Serial.println("Tare... remove any other weights from the scale.");
      delay(500);
      scale.tare();
      Serial.println("Tare done...");

      // Your Domain name with URL path or IP address with path
      if(WiFi.status() == WL_CONNECTED){
        http.begin(serverName_2, root_ca);
        http.addHeader("Content-Type", "application/json");
        int code = http.POST("{\"Security\": 1104}");
        Serial.print("Get watering value. HTTP Response code: ");
        Serial.println(code);
        // http.end();
      } else {
        Serial.println("WiFi Disconnected");

        WiFi.begin(ssid, password);
        Serial.println("Connecting");
        while(WiFi.status() != WL_CONNECTED) {
          delay(500);
          Serial.print(".");
        }
        Serial.println("");
        Serial.print("Connected to WiFi network with IP Address: ");
        Serial.println(WiFi.localIP());
      }
      
      String res = http.getString();
      const char* response = res.c_str();
      http.end();

      Serial.print("Watering - Pump for ");
      Serial.print(atoi(response));
      Serial.println(" ms...");

      digitalWrite(pumpPin, HIGH);
      delay(atoi(response));
      digitalWrite(pumpPin, LOW);
      Serial.println("Stop pump...");

      Serial.println("Counting water leakage...");
      delay(1000*60*5);
      leak = scale.get_units(50);
      Serial.print("Leak out water: ");
      Serial.print(leak);
      Serial.println(" g");
    } else {
      Serial.println("HX711 not found.");
    }
  } else {
      Serial.println("No need to watering.");
  }

  Serial.println("Sample DHT11...");
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err=");
    Serial.print(SimpleDHTErrCode(err));
    Serial.println(SimpleDHTErrDuration(err));
    delay(1000);
    return;
  }
  
  Serial.print("Temperature: ");
  Serial.print((int)temperature);
  Serial.print(" *C, humidity: "); 
  Serial.print((int)humidity);
  Serial.println("%");

  if(WiFi.status() == WL_CONNECTED){
    char str[9];
    char total_str[100] = "{\"temperature\":";
    
    itoa(temperature, str, 10);
    strcat(total_str, str);
    strcat(total_str, ",\"moisture\":");

    itoa(humidity, str, 10);
    strcat(total_str, str);
    strcat(total_str, ",\"soil_moisture\":");

    itoa(DirtSensorValue, str, 10);
    strcat(total_str, str);
    strcat(total_str, ",\"gravity\":");

    itoa(leak, str, 10);
    strcat(total_str, str);
    strcat(total_str, "}");

    //Serial.println(total_str);
    http.begin(serverName, root_ca);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(total_str);
    Serial.print("Upload data. HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    // Free resources
    http.end();
  } else {
    Serial.println("WiFi Disconnected");

    WiFi.begin(ssid, password);
    Serial.println("Connecting");
    while(WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());
  }

  delay(1000*60*30);
}

