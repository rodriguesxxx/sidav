#include <WebSocketsClient.h>

#ifndef __WEBSOCKET__
    #define __WEBSOCKET__

    class WebSocket {
        private:
            char *ip, *route;
            int port;
            WebSocketsClient wsClient;
            static void event(WStype_t type, uint8_t * payload, size_t length);

        public:
            WebSocket();
            WebSocket(char *ip, int port, char *route);
            WebSocketsClient attempt();

    };

#endif