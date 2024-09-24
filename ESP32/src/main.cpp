#include <Arduino.h>
#include "Wireless.h"
#include "WebSocket.h"


//SSID | PASSWORD
Wireless wireless("IGNIS", "SNCTproject2024");

WebSocket wsSerial;
WebSocket wsCam;

void setup() {
  Serial.begin(115200);
  bool status = wireless.connect();

  if(!status) {
    Serial.println("Erro ao se conectar a rede wifi! Reinicie a ESP32");
    while(true);
  }

  wsSerial.route = "/api/ws/serial";
  wsSerial.attempt();

  wsCam.route = "/api/ws/cam";
  wsCam.attempt();
}

void loop() {
  wsSerial.loop();
  wsCam.loop();
  wsSerial.sendTXT("TESTE");
}