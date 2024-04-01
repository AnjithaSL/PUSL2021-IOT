#include <NewPing.h>

#define TRIGGER_PIN  12 
#define ECHO_PIN     11 
#define MAX_DISTANCE 200 // Maximum distance in centimeters

#define sensorPin A0 // Assuming the sensor is connected to analog pin A0
#define LED_PIN 13 // LED connected to digital pin 13

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  Serial.begin(9600); // Set the baud rate to match your serial monitor
  pinMode(LED_PIN, OUTPUT); // Set the LED pin as an output
}

void loop() {
  // Read the analog value from the sensor
  int sensorValue = analogRead(sensorPin);

  // Convert the analog value to TDS using a calibration formula
  float tdsValue = map(sensorValue, 0, 150, 0, 1500); // Example calibration, adjust according to your sensor
  
  // Print the TDS value
  Serial.print("TDS Value: ");
  Serial.print(tdsValue);
  Serial.println(" ppm");

  // Read the distance from the ultrasonic sensor
  unsigned int distance_cm = sonar.ping_cm();
  
  if (tdsValue > 500|| distance_cm == 0) {
    digitalWrite(LED_PIN, HIGH); // Turn on the LED if TDS  greater than 200 ppm or distance is 0
  } else {
    digitalWrite(LED_PIN, LOW); // Turn off the LED if conditions are not met

    // Filter out erroneous distance readings
    if (distance_cm < 2 || distance_cm > MAX_DISTANCE) { // Adjust threshold according to your requirements
      Serial.println("Error: Invalid distance measurement.");
    } else {
      // Convert cm to mm
      unsigned int distance_mm = distance_cm * 10;
      Serial.print("Distance: ");
      Serial.print(distance_mm);
      Serial.println(" mm");
    }
  }

  delay(1000);
}
