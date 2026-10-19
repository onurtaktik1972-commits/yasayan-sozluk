// =====================================================================
//  Yaşayan Sözlük — ESP32 LED denetleyicisi
//
//  Görevi: MQTT broker'daki TOPIC_LED konusunu dinler; "0".."49" gelince
//  o kelimenin LED'ini yumuşakça yakar, LED_SURE_MS sonra söndürür.
//  TOPIC_DURUM konusuna "online" yazar; elektrik/WiFi giderse broker
//  otomatik "offline" yayınlar (LWT) → sitede "Işık kapalı" görünür.
//
//  Kütüphaneler (Arduino IDE → Kütüphane Yöneticisi):
//    - FastLED      (Daniel Garcia)   ≥ 3.7
//    - PubSubClient (Nick O'Leary)    ≥ 2.8
//  Kart: "ESP32 Dev Module" (Arduino-ESP32 çekirdeği 2.x veya 3.x)
//  Ayarlar: config.h
// =====================================================================
#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include "config.h"

// ---------- Nesneler ----------
WiFiMulti wifiMulti;
#if MQTT_TLS
WiFiClientSecure netClient;
#else
WiFiClient netClient;
#endif
PubSubClient mqtt(netClient);
CRGB leds[LED_SAYISI];

struct Ag { const char* ssid; const char* sifre; };
static const Ag AGLAR[] = WIFI_AGLARI;

// ---------- LED durum makinesi ----------
enum LedDurum { BOS, YANIYOR, SONUYOR };
static LedDurum ledDurum = BOS;
static int      aktifLed = -1;        // fiziksel LED numarası
static uint32_t durumBaslangic = 0;
static uint8_t  seviye = 0;           // 0..255 parlaklık çarpanı
static uint32_t sonKomut = 0;

static String clientId;
static uint32_t sonMqttDeneme = 0;

static int fizikselIndeks(int sozlukIndeksi) {
#if HARITA_KULLAN
  return LED_HARITASI[sozlukIndeksi];
#else
  return sozlukIndeksi;
#endif
}

static void tumunuSondur() {
  FastLED.clear();
  FastLED.show();
  aktifLed = -1;
  ledDurum = BOS;
  seviye = 0;
}

static void ledYak(int sozlukIndeksi) {
  int fiz = fizikselIndeks(sozlukIndeksi);
  if (fiz != aktifLed) {
    FastLED.clear();               // önceki kelimenin ışığı söner
    seviye = 0;
  }
  aktifLed = fiz;
  ledDurum = YANIYOR;
  durumBaslangic = millis();
}

// Her döngüde çağrılır: yumuşak yanma → bekleme → yumuşak sönme
static void ledGuncelle() {
  static uint32_t sonCizim = 0;
  uint32_t simdi = millis();
  if (simdi - sonCizim < 10) return;        // ~100 Hz
  sonCizim = simdi;
  if (ledDurum == BOS || aktifLed < 0) return;

  uint32_t gecen = simdi - durumBaslangic;
  if (ledDurum == YANIYOR) {
    seviye = gecen >= SOLMA_MS ? 255 : (uint8_t)(255UL * gecen / SOLMA_MS);
    if (gecen >= LED_SURE_MS) { ledDurum = SONUYOR; durumBaslangic = simdi; }
  } else { // SONUYOR
    if (gecen >= SOLMA_MS) { tumunuSondur(); return; }
    seviye = 255 - (uint8_t)(255UL * gecen / SOLMA_MS);
  }
  CRGB c = YAKMA_RENGI;
  c.nscale8_video(seviye);
  leds[aktifLed] = c;
  FastLED.show();
}

// ---------- MQTT mesajı ----------
static void mesajGeldi(char* topic, byte* payload, unsigned int len) {
  if (len == 0 || len > 4) return;
  char buf[5];
  memcpy(buf, payload, len);
  buf[len] = '\0';

  if (strcmp(buf, "off") == 0 || strcmp(buf, "-1") == 0) {
    Serial.println("[LED] söndür komutu");
    tumunuSondur();
    return;
  }
  for (unsigned int i = 0; i < len; i++) if (!isdigit((unsigned char)buf[i])) {
    Serial.printf("[LED] geçersiz komut reddedildi: %s\n", buf);
    return;
  }
  int idx = atoi(buf);
  if (idx < 0 || idx >= LED_SAYISI) {
    Serial.printf("[LED] aralık dışı: %d\n", idx);
    return;
  }
  uint32_t simdi = millis();
  if (simdi - sonKomut < MIN_KOMUT_ARASI_MS) return;   // aşırı sık komut koruması
  sonKomut = simdi;

  Serial.printf("[LED] %d yakılıyor\n", idx);
  ledYak(idx);
}

// ---------- Bağlantılar ----------
static void wifiKontrol() {
  static bool oncekiBagli = false;
  bool bagli = (wifiMulti.run(2000) == WL_CONNECTED);
  if (bagli != oncekiBagli) {
    if (bagli) Serial.printf("[WiFi] bağlandı: %s  IP: %s  RSSI: %d dBm\n",
                             WiFi.SSID().c_str(), WiFi.localIP().toString().c_str(), WiFi.RSSI());
    else       Serial.println("[WiFi] bağlantı koptu");
    oncekiBagli = bagli;
  }
}

static void mqttKontrol() {
  if (WiFi.status() != WL_CONNECTED || mqtt.connected()) return;
  uint32_t simdi = millis();
  if (simdi - sonMqttDeneme < 3000) return;            // 3 sn'de bir dene, döngüyü kilitleme
  sonMqttDeneme = simdi;

  Serial.printf("[MQTT] %s:%d bağlanılıyor…\n", MQTT_HOST, MQTT_PORT);
  bool ok = mqtt.connect(clientId.c_str(),
                         strlen(MQTT_KULLANICI) ? MQTT_KULLANICI : nullptr,
                         strlen(MQTT_SIFRE) ? MQTT_SIFRE : nullptr,
                         TOPIC_DURUM, 1, true, "offline");   // LWT: retained "offline"
  if (ok) {
    Serial.println("[MQTT] bağlandı");
    mqtt.publish(TOPIC_DURUM, "online", true);
    mqtt.subscribe(TOPIC_LED, 0);
  } else {
    Serial.printf("[MQTT] başarısız, durum=%d\n", mqtt.state());
  }
}

// Kart üzerindeki LED: sabit yanık = her şey yolunda, yanıp sönme = bağlantı yok
static void durumLedi() {
  bool hazir = (WiFi.status() == WL_CONNECTED) && mqtt.connected();
  digitalWrite(DURUM_LED_PIN, hazir ? HIGH : ((millis() / 400) % 2));
}

static void acilisTesti() {
  for (int i = 0; i < LED_SAYISI; i++) {
    FastLED.clear();
    leds[i] = CRGB(40, 120, 255);
    FastLED.show();
    delay(25);
  }
  tumunuSondur();
}

// ---------- Arduino ----------
void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("\n=== Yaşayan Sözlük — ESP32 ===");

  pinMode(DURUM_LED_PIN, OUTPUT);

  FastLED.addLeds<LED_TIPI, LED_PIN, RENK_SIRASI>(leds, LED_SAYISI);
  FastLED.setBrightness(PARLAKLIK);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, MAX_AKIM_MA);
  acilisTesti();

  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);                 // daha düşük gecikme
  for (const Ag& a : AGLAR) wifiMulti.addAP(a.ssid, a.sifre);

  uint8_t mac[6];
  WiFi.macAddress(mac);
  char id[32];
  snprintf(id, sizeof(id), "esp32-sozluk-%02x%02x%02x", mac[3], mac[4], mac[5]);
  clientId = id;

#if MQTT_TLS
  netClient.setInsecure();              // Sertifika doğrulaması yok; şifreleme var. (İsterseniz setCACert ile kök sertifika ekleyin.)
#endif
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(mesajGeldi);
  mqtt.setKeepAlive(30);
  mqtt.setSocketTimeout(5);
}

void loop() {
  static uint32_t sonWifi = 0;
  if (millis() - sonWifi > 1000) { sonWifi = millis(); wifiKontrol(); }
  mqttKontrol();
  mqtt.loop();
  ledGuncelle();
  durumLedi();
}
