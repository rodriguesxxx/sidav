#ifndef WEBSOCKET_H
#define WEBSOCKET_H
#include <WebSocketsClient.h>
class WebSocket : public WebSocketsClient {
        private:
            char *ip, *route;
            int port;
            WebSocketsClient wsClient;
            static void event(WStype_t type, uint8_t * payload, size_t length);

        public:
            WebSocket();
            WebSocket(char *ip, int port, char *route);
            void attempt();
    };

#endif