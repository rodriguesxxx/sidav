#include <WiFi.h>

#ifndef __WIRELESS__
    #define __WIRELESS__
    
    class Wireless {
        private:
           char *ssid, *passwd;

        public:
            Wireless(char *ssid, char *passwd);
            bool connect();
    };

#endif