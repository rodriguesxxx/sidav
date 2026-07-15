#include <Arduino.h>
#include "WiFiManager.h"
#include "WebSocketClient.h"
#include "Camera.h"

WiFiManager wifi("IGNIS", "SNCTproject2024");
WebSocketClient cameraStream;
Camera camera("drone");

void setup() {
    Serial.begin(115200);

    if (!wifi.connect()) {
        Serial.println("WiFi connection failed. Restart the ESP32.");
        while (true) { delay(1000); }
    }

    Serial.println("WiFi connected");

    cameraStream.route = "/api/ws/cam";
    cameraStream.connect();
    camera.setup();
}

void loop() {
    cameraStream.loop();

    if (cameraStream.isConnected()) {
        camera.streamTo(cameraStream);
        delay(10);
    }
}