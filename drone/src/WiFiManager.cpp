#include "WiFiManager.h"

WiFiManager::WiFiManager(const char *ssid, const char *password)
    : ssid(ssid), password(password) {}

bool WiFiManager::connect() {
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.printf("Connecting to %s\n", ssid);
    }

    return WiFi.status() == WL_CONNECTED;
}