#define LED_PIN 13 // Define the pin for LED bulb

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(LED_PIN, OUTPUT); // Set LED pin as output
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read data from serial port
    if (data.startsWith("Speed:")) {
      data.remove(0, 6); // Remove "Speed:" from the received string
      float speed = data.toFloat(); // Convert string to float
      if (speed > 12000) {
        digitalWrite(LED_PIN, HIGH); // Turn on LED bulb
        delay(1000); // Keep LED on for 1 second
        digitalWrite(LED_PIN, LOW); // Turn off LED bulb
      }
    }
  }
}
