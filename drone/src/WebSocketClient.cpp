#include "WebSocketClient.h"

WebSocketClient::WebSocketClient()
    : ip("192.168.0.101"), port(8080), route("/api/ws") {}

WebSocketClient::WebSocketClient(const char *ip, int port, const char *route)
    : ip(ip), port(port), route(route) {}

void WebSocketClient::handleEvent(WStype_t type, uint8_t *payload, size_t length) {
    switch (type) {
    case WStype_DISCONNECTED:
        Serial.printf("[WS] Disconnected: %s\n", payload);
        break;
    case WStype_CONNECTED:
        Serial.printf("[WS] Connected: %s\n", payload);
        break;
    case WStype_TEXT:
        Serial.printf("[WS] Message: %s\n", payload);
        break;
    default:
        break;
    }
}

void WebSocketClient::connect() {
    begin(ip, port, route);
    onEvent(handleEvent);
}