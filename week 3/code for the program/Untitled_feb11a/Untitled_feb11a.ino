#include "arduino_secrets.h"
#include "thingProperties.h"
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  initProperties(); 


  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  // Initialize the LSM6DS3 sensor
  if (!IMU.begin()) {
    Serial.println("Failed to initialize LSM6DS3!");
    while (1);
  }
}

void loop() {
  ArduinoCloud.update();  

  // Read accelerometer data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accx, accy, accz); 

    // Print values for debugging
    Serial.print("X: ");
    Serial.print(accx);
    Serial.print(", Y: ");
    Serial.print(accy);
    Serial.print(", Z: ");
    Serial.println(accz);
  }
  
  delay(1000);  // Collect data every second
}

// Callback functions when Cloud variables change
void onAccxChange() {}
void onAccyChange() {}
void onAcczChange() {}