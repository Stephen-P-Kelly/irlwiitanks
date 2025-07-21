#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include <Bounce2.h>

// ──────── Pin Assignments ────────────────────────────────────────────────────
const int JOYSTICK_VRX   = x;    // X-axis of joystick → analog 0
const int JOYSTICK_VRY   = x;    // Y-axis of joystick → analog 1
const int JOYSTICK_SW    = x;    // Joystick switch     → digital 2
const int BARREL_LEFT    = x;    // Barrel left servo   → digital 3
const int BARREL_RIGHT   = x;    // Barrel right servo  → digital 4
const int FIRE_BUTTON    = x;    // Fire button         → digital 5

// ──────── JSON Setup ─────────────────────────────────────────────────────────
const size_t JSON_DOCUMENT_SIZE = 256;
StaticJsonDocument<JSON_DOCUMENT_SIZE> control_data;

// ──────── Analog Resolution ──────────────────────────────────────────────────
const int ANALOG_RESOLUTION = 4096;  // 12-bit ADC resolution on ESP32

// ──────── Pin Debouncing ─────────────────────────────────────────────────────
Bounce jsSwitchDebounce = Bounce();
Bounce barrelLeftDebounce = Bounce();
Bounce barrelRightDebounce = Bounce();
Bounce fireDebounce = Bounce();
const uint16_t DEBOUNCE_INTERVAL = 25; // ms

// ──────── Wi-Fi Credentials & Network Config ─────────────────────────────────
char ssid[] = "TankGame";
char pass[] = "12345678";
// You’ll run your controller at 192.168.137.11 on a /24 subnet, gateway .1
IPAddress local_IP(192, 168, 137, 11);
IPAddress gateway(192, 168, 137, 1);
IPAddress subnet(255, 255, 255, 0);

// ──────── UDP Setup ───────────────────────────────────────────────────────────
WiFiUDP  udp;
IPAddress tank_IP(192, 168, 137, 10);
const uint16_t tank_rx_port = 4210;    // UDP port your tank listens on
char serial_buf[255];                  // Enough to hold serialized JSON
const uint16_t Hz = 50;                // The frequency of UDP transmission
const uint16_t LOOP_DELAY = 1000 / Hz; // Effective delay between UDP transmissions (ms)

// ──────── Setup ───────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  analogReadResolution(ANALOG_RESOLUTION);

  // configure pins
  pinMode(JOYSTICK_VRX, INPUT);
  pinMode(JOYSTICK_VRY, INPUT);
  pinMode(JOYSTICK_SW, INPUT_PULLUP);
  pinMode(BARREL_LEFT, INPUT_PULLUP);
  pinMode(BARREL_RIGHT, INPUT_PULLUP);
  pinMode(FIRE_BUTTON, INPUT_PULLUP);
  
  // set up debouncing
  jsSwitchDebounce.attach(JOYSTICK_SW);
  barrelLeftDebounce.attach(BARREL_LEFT);
  barrelRightDebounce.attach(BARREL_RIGHT);
  fireDebounce.attach(FIRE_BUTTON);
  // set debounce interval
  jsSwitchDebounce.interval(DEBOUNCE_INTERVAL);
  barrelLeftDebounce.interval(DEBOUNCE_INTERVAL);
  barrelRightDebounce.interval(DEBOUNCE_INTERVAL);
  fireDebounce.interval(DEBOUNCE_INTERVAL);

  // apply static IP configuration *before* connecting
  Serial.printf("Giving the controller a static IP of %s... ", local_IP.toString().c_str());
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("FAILED");
  } else {
    Serial.println("OK");
  }

  // connect to Wi-Fi
  Serial.printf("Connecting to %s", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println();
  Serial.println("Wi-Fi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // no need to call udp.begin(localPort) when only sending packets
  // send a handshake packet
  udp.beginPacket(tank_IP, tank_rx_port);
  udp.write("ground control to major tom");
  udp.endPacket();

  delay(2000);
}

// ──────── Main Loop ────────────────────────────────────────────────────────────
void loop() {
  // update debouncing
  jsSwitchDebounce.update();
  barrelLeftDebounce.update();
  barrelRightDebounce.update();
  fireDebounce.update();
  
  // read controls
  control_data["js_x"]   = analogRead(JOYSTICK_VRX);
  control_data["js_y"]   = analogRead(JOYSTICK_VRY);
  control_data["sw"]     = jsSwitchDebounce.read()     == LOW ? 1 : 0;
  control_data["left"]   = barrelLeftDebounce.read()   == LOW ? 1 : 0;
  control_data["right"]  = barrelRightDebounce.read()  == LOW ? 1 : 0;
  control_data["fire"]   = fireDebounce.read()   == LOW ? 1 : 0;

  // debug output
  Serial.println("=== CONTROL DATA ===");
  serializeJsonPretty(control_data, Serial);
  Serial.println();

  // serialize to buffer and send via UDP
  serializeJson(control_data, serial_buf, sizeof(serial_buf));
  udp.beginPacket(tank_IP, tank_rx_port);
  udp.write(serial_buf);
  udp.endPacket();

  delay(LOOP_DELAY);  // ~50Hz
}
