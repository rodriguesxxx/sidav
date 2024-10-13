//TODO: Corrigir bug do reboot

#include <Arduino.h>
#include "Wireless.h"
#include "WebSocket.h"
#include "Cam.h"


//SSID | PASSWORD
// Wireless wireless("IGNIS", "SNCTproject2024");
Wireless wireless("motog", "elllllly");
WebSocket wsSerial;
WebSocket wsCam;
Cam cam("drone");

void setup() {
    Serial.begin(115200);
    bool status = wireless.connect();

    if(!status) {
      Serial.println("Erro ao se conectar a rede wifi! Reinicie a ESP32");
      while(true);
    }
      
    Serial.println("Sucesso ao se conectar a rede WiFi!");

    // wsSerial.route = "/api/ws/serial";
    // wsSerial.attempt();

    wsCam.route = "/api/ws/cam";
    wsCam.attempt();
    cam.setup();
}

void loop() {
    //BUG#1: ERROR DO REBOOTING
      //BUG#1: [REPORT] RESOLVIDO PARCIALMENTE, CASO PERSISTIR, REINICIE O ROTEADOR/ESP32
    wsCam.loop();
    if(wsCam.isConnected()) {
      cam.live(wsCam);
      delay(100);
    }
}