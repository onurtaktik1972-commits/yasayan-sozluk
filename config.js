// =====================================================================
//  Yaşayan Sözlük — Yapılandırma (site + ESP32 taklitçisi ortak kullanır)
//
//  GELİŞTİRME: HiveMQ'nun herkese açık, ücretsiz broker'ı (hesap gerekmez).
//    Konu adlarındaki "40c411" bu projeye özel rastgele bir kimliktir;
//    başka kimse aynı konuyu kullanmasın diye var. ESP32 config.h ile AYNI olmalı.
//
//  SERGİ (üretim): HiveMQ Cloud'a geçince url/username/password doldurulur
//    (bkz. docs/FAZ3_MQTT.md). Kodda başka değişiklik gerekmez.
//
//  url "" yapılırsa uygulama TEST MODUNDA çalışır (sanal LED şeridi).
// =====================================================================
window.SOZLUK_CONFIG = {
  mqtt: {
    url: "wss://broker.hivemq.com:8884/mqtt",
    username: "",
    password: "",
    topicLed: "yasayansozluk/40c411/led",     // site → ESP32 : "0".."49"
    topicDurum: "yasayansozluk/40c411/durum"  // ESP32 → site : "online" / "offline" (retained)
  },
  // Kart görseli: sozluk.json içindeki "foto" adresinden (Unsplash) gelir; açılamazsa düz zemin + Arapça gösterilir.
  gorselModu: "otomatik",
  ledSayisi: 50,
  ledSuresiSn: 60,       // Güvenlik süresi: kart kapatılınca LED hemen söner; kapatılmazsa en fazla bu kadar yanar (ESP32 config.h → LED_SURE_MS ile aynı)
  // Sanal LED şeridi: "auto" = sadece test modunda, true = her zaman, false = asla. ?debug=1 her zaman gösterir.
  sanalSerit: "auto"
};
