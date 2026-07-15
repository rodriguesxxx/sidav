#ifndef WEBSOCKET_CLIENT_H
#define WEBSOCKET_CLIENT_H

#include <WebSocketsClient.h>

class WebSocketClient : public WebSocketsClient {
public:
    WebSocketClient();
    WebSocketClient(const char *ip, int port, const char *route);
    void connect();

    char *route;

private:
    const char *ip;
    int port;
    static void handleEvent(WStype_t type, uint8_t *payload, size_t length);
};

#endif