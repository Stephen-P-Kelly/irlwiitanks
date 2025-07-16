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
int JSON_DOCUMENT_SIZE = 256; // Bytes
StaticJsonDocument<JSON_DOCUMENT_SIZE> control_data; // "js_x", "js_y", "left", "right", "fire"
int analog_resolution = 4096;
// WiFi
char ssid[] = "TankGame";
char pass[] = "12345678";
char hostname[] = "greentank";
int ip[] = {192, 168, 137, 20};
IPAddress local_IP(ip[0], ip[1], ip[2], ip[3]);
IPAddress gateway(192, 168, 137, 1);
IPAddress subnet(255, 255, 255, 0);
// UDP
WiFiUDP udp;
int tank_ip[] = {192, 168, 137, 10};
IPAddress tank_IP(tank_ip[0], tank_ip[1], tank_ip[2], tank_ip[3]);
int tank_rx_port = x;
char serial[255];

void setup() {
  // Setup pins
  pinMode(JOYSTICK_VRX, INPUT);
  pinMode(JOYSTICK_VRY, INPUT);
  pinMode(JOYSTICK_SW, INPUT);
  pinMode(BARREL_LEFT, INPUT);
  pinMode(BARREL_RIGHT, INPUT);
  pinMode(FIRE_BUTTON, INPUT);
  
  analogReadResolution(x);

  // Connect to WiFi
  Serial.print("Attempting to connect to SSID: ");
  Serial.print(ssid);
  while (WiFi.begin(ssid) != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected! :)");
  // Configuring device
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure! :(");
  }
  WiFi.setHostname(hostname);
}

void loop() {
  // Collect pin info
  control_data["js_x"] = analogRead(JOYSTICK_VRX);
  control_data["js_y"] = analogRead(JOYSTICK_VRY);
  control_data["left"] = analogRead(BARREL_LEFT);
  control_data["right"] = analogRead(BARREL_RIGHT);
  control_data["fire"] = analogRead(FIRE_BUTTON);
  serializeJson(control_data, serial);
  // Make + send UDP packet to tank
  udp.beginPacket(tank_IP, tank_port);
  udp.write(serial);
  udp.endPacket();
  // Delay for 20 ms (results in 50 Hz)
  delay(20);
}
