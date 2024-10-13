//TODO: melhorar qualidade da imagem

#include "Cam.h"

Cam::Cam(char *id) {
    this->id = id;
}

void Cam::setup() {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;

    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 7;
    config.fb_count = 1;

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Erro a iniciar câmera: 0x%x", err);
        return;
    }

    sensor_t *s = esp_camera_sensor_get();
    s->set_framesize(s, FRAMESIZE_QVGA); // Resolução
    s->set_quality(s, 7); // Qualidade JPEG (quanto menor o valor, maior a qualidade)
    s->set_brightness(s, 0.8); // Brilho (-2 a 2)
    s->set_contrast(s, 0.9); // Contraste (-2 a 2)
    s->set_saturation(s, 1); // Saturação (-2 a 2)
    s->set_sharpness(s, 1.5); // Nitidez (-2 a 2)
}

void Cam::live(WebSocket &ws) {

     if (!ws.isConnected()) {
        Serial.println("WebSocket não está conectado!");
        return;
    }

    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Não foi possível adquirir o buffer do frame!");
        return;
    }

    if (ws.sendTXT((String) "START:" + String("drone")) == false) {
        Serial.println("Falha ao enviar START via WebSocket");
        esp_camera_fb_return(fb);
        return;
    }

    if (ws.sendBIN(fb->buf, fb->len) == false) {
        Serial.println("Falha ao enviar frame via WebSocket");
        esp_camera_fb_return(fb);
        return;
    }

    if (ws.sendTXT("STOP") == false) {
        Serial.println("Falha ao enviar STOP via WebSocket");
        esp_camera_fb_return(fb);
        return;
    }

    esp_camera_fb_return(fb);
}