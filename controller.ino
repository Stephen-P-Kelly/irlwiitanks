#include <WiFi.h>
#include <WiFiUDP.h>
#include <ArduinoJson.h>

// Pin Assignments
int JOYSTICK_VRX = x;
int JOYSTICK_VRY = x;
int JOYSTICK_SW = x;
int BARREL_LEFT = x;
int BARREL_RIGHT = x;
int FIRE_BUTTON = x;
// Analog Values
JsonDocument control_data; // "js_x", "js_y", "left", "right", "fire"
int analog_resolution = x;
// WiFi
char* ssid = "TankGame"
char* pass = "12345678"
char* hostname = "greentank"
int ip[] = [192, 168, 137, 21]

IPAddress local_IP(ip[0], ip[1], ip[2], ip[3]);
IPAddress gateway(192, 168, 137, 1);
IPAddress subnet(255, 255, 255, 0);

void setup() {
  // Setup pins
  pinMode(JOYSTICK_VRX, INPUT);
  pinMode(JOYSTICK_VRY, INPUT);
  pinMode(JOYSTICK_SW, INPUT);
  pinMode(BARREL_LEFT, INPUT);
  pinMode(BARREL_RIGHT, INPUT);
  pinMode(FIRE_BUTTON, INPUT);
  
  analogReadResolution(x);
  
  WiFi.begin(ssid, pass);
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }
  WiFi.setHostname(hostname); //define hostname
}

void loop() {
  control_data["js_x"] = analogRead(JOYSTICK_VRX);
  control_data["js_y"] = analogRead(JOYSTICK_VRY);
  control_data["left"] = analogRead(BARREL_LEFT);
  control_data["right"] = analogRead(BARREL_RIGHT);
  control_data["fire"] = analogRead(FIRE_BUTTON);
}
