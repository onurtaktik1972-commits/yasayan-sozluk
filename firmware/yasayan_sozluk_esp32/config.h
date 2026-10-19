// =====================================================================
//  Yaşayan Sözlük — ESP32 ayarları
//  Donanım geldiğinde SADECE bu dosyadaki WiFi bilgilerini doldurmanız yeterli.
// =====================================================================
#pragma once

// ---------- WiFi ----------
// Birden fazla ağ tanımlanabilir; ESP32 hangisi varsa ona bağlanır
// (örn. mekân WiFi'si + yedek olarak telefon hotspot'u).
#define WIFI_AGLARI { \
  { "MEKAN_WIFI_ADI",   "MEKAN_WIFI_SIFRESI" }, \
  { "TELEFON_HOTSPOT",  "HOTSPOT_SIFRESI"    }, \
}

// ---------- MQTT ----------
// Geliştirme: HiveMQ herkese açık broker (hesap gerekmez).
// Sergi: HiveMQ Cloud bilgileriyle değiştirin ve MQTT_TLS 1 yapın.
#define MQTT_HOST      "broker.hivemq.com"
#define MQTT_PORT      1883          // TLS ile: 8883
#define MQTT_TLS       0             // 1 = şifreli bağlantı (HiveMQ Cloud için zorunlu)
#define MQTT_KULLANICI ""            // HiveMQ Cloud: esp32_user
#define MQTT_SIFRE     ""

// Site tarafındaki config.js ile BİREBİR aynı olmalı
#define TOPIC_LED      "yasayansozluk/40c411/led"
#define TOPIC_DURUM    "yasayansozluk/40c411/durum"

// ---------- LED şeridi ----------
#define LED_PIN        16            // WS2812B DIN → GPIO16 (330 Ω seri direnç ile)
#define LED_SAYISI     50
#define LED_TIPI       WS2812B
#define RENK_SIRASI    GRB
#define PARLAKLIK      160           // 0–255
#define MAX_AKIM_MA    2000          // FastLED güç sınırı (5 V adaptör kapasitesinin altında tutun)
#define LED_SURE_MS    10000         // Yanık kalma süresi (site config.js → ledSuresiSn ile aynı)
#define SOLMA_MS       600           // Yumuşak yanma/sönme süresi
#define MIN_KOMUT_ARASI_MS 150       // Bundan sık gelen komutlar yok sayılır

// Kelimenin yanacağı renk (sıcak kandil ışığı)
#define YAKMA_RENGI    CRGB(255, 150, 50)

// Kart üzerindeki durum LED'i (çoğu DevKit'te GPIO2). WiFi/MQTT yokken yanıp söner.
#define DURUM_LED_PIN  2

// ---------- Fiziksel sıra eşlemesi ----------
// Sözlükteki sıra (0 = Adalet … 49 = Yolculuk) ile şeritteki fiziksel sıra AYNIYSA 0 bırakın.
// Panoda kelimeler farklı dizildiyse 1 yapıp LED_HARITASI'nı doldurun:
//   LED_HARITASI[sözlük_indeksi] = şeritteki_LED_numarası
#define HARITA_KULLAN  0
#if HARITA_KULLAN
static const uint8_t LED_HARITASI[LED_SAYISI] = {
   0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
  10,11,12,13,14,15,16,17,18,19,
  20,21,22,23,24,25,26,27,28,29,
  30,31,32,33,34,35,36,37,38,39,
  40,41,42,43,44,45,46,47,48,49
};
#endif
