#include <Arduino.h>
#include "Wireless.h"
#include "WebSocket.h"


//SSID | PASSWORD
Wireless wireless("IGNIS", "SNCTproject2024");

WebSocket ws;
WebSocketsClient client;

void setup() {
  Serial.begin(115200);
  bool status = wireless.connect();

  if(!status) {
    Serial.println("Erro ao se conectar a rede wifi! Reinicie a ESP32");
    while(true);
  }

  client = ws.attempt();
}

void loop() {
  Serial.println("Passou de boa!");
}