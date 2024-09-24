#include "WebSocket.h"

WebSocket::WebSocket() {
    this->ip = "192.168.0.101";   
    this->port = 8080;   
    this->route = "/api/ws";   
}

WebSocket::WebSocket(char *ip, int port, char *route) {
    this->ip = ip;
    this->port = port;
    this->route = route;
}

void WebSocket::event(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.printf("[WS] Desconectado\n");
            break;
        case WStype_CONNECTED: {
            Serial.printf("[WS] Conectado: %s\n", payload);
        }
        
        break;
        
        case WStype_TEXT:
            Serial.printf("Resposta: %s\n", payload);
            break;

        // case WStype_BIN:
        //     case WStype_PING:
        //         case WStype_PONG:
        //             case WStype_ERROR:
        //                 case WStype_FRAGMENT_TEXT_START:
        //                     case WStype_FRAGMENT_BIN_START:
        //                         case WStype_FRAGMENT:
        //                             case WStype_FRAGMENT_FIN:
        //                                 break;
        default:
            break;
    }
}

void WebSocket::attempt() {
    begin(ip, port, route);
    onEvent(WebSocket::event);
}       
