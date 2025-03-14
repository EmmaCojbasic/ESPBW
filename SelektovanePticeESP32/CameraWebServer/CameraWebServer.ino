#include "esp_camera.h"
#include <WiFi.h>
#include <EloquentTinyML.h>
#include <eloquent_tinyml/tensorflow.h>  // TensorFlow Lite za ESP32

#include "camera_pins.h"
#include "bird_model.h"  // Tvoj model u .h fajlu

#define NUMBER_OF_INPUTS  128 * 128 * 1   // Rezolucija grayscale slike (prilagodi ako je drugačije)
#define NUMBER_OF_OUTPUTS 20              // Broj klasa
#define TENSOR_ARENA_SIZE 30 * 1024       // Memorija za TFLite model

// TinyML model
Eloquent::TinyML::TensorFlow::TensorFlow<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> ml;

// WiFi podaci
const char *ssid = "**********";
const char *password = "**********";

void startCameraServer();
void setupLedFlash(int pin);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println("\nPokretanje sistema...");

  // Inicijalizacija TinyML modela
  Serial.println("Učitavanje TinyML modela...");
  ml.begin(bird_model);
  Serial.println("Model učitan!");

  // Konfiguracija kamere
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
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_GRAYSCALE;  // Koristimo grayscale sliku
  config.frame_size = FRAMESIZE_128X128;      // Prilagoditi rezoluciju modelu
  config.fb_count = 1;

  // Inicijalizacija kamere
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Greška pri pokretanju kamere: 0x%x\n", err);
    return;
  }

  // Povezivanje na WiFi
  WiFi.begin(ssid, password);
  Serial.print("Povezivanje na WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi povezan!");

  startCameraServer();

  Serial.print("Kamera spremna! Otvori: http://");
  Serial.print(WiFi.localIP());
  Serial.println(" za pregled.");
}

void loop() {
  // Uzimanje slike sa kamere
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Neuspelo hvatanje slike!");
    return;
  }

  // Proveri veličinu slike
  if (fb->width != 128 || fb->height != 128) {
    Serial.println("Neodgovarajuća veličina slike!");
    esp_camera_fb_return(fb);
    return;
  }

  // Priprema slike za model (konverzija u float niz)
  float input[NUMBER_OF_INPUTS];
  for (int i = 0; i < NUMBER_OF_INPUTS; i++) {
    input[i] = fb->buf[i] / 255.0f;  // Normalizacija piksela [0, 1]
  }

  // Oslobađanje memorije slike
  esp_camera_fb_return(fb);

  // Pokretanje predikcije
  float output[NUMBER_OF_OUTPUTS] = {0};
  ml.predict(input, output);

  // Pronalazak klase sa najvećom verovatnoćom
  int best_class = 0;
  float best_score = output[0];
  for (int i = 1; i < NUMBER_OF_OUTPUTS; i++) {
    if (output[i] > best_score) {
      best_score = output[i];
      best_class = i;
    }
  }

  // Prikaz rezultata
  Serial.print("Predikcija: Klasa ");
  Serial.print(best_class);
  Serial.print(" (");
  Serial.print(best_score * 100, 2);
  Serial.println("%)");
  
  delay(5000);  // Pauza pre sledeće slike
}