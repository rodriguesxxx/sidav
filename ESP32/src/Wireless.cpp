#include "Wireless.h"

Wireless::Wireless(char *ssid, char *passwd) {
    this->ssid = ssid;
    this->passwd = passwd;
}

bool Wireless::connect() {
    WiFi.begin(ssid, passwd);
    
    while(WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.printf("Tentando se conectar a rede: %s\n", ssid);
    }

    return (WiFi.status() == WL_CONNECTED ) ? true : false; 
}
