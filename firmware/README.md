# ESP32 — Kurulum ve Kablolama

Donanım geldiğinde yapılacak işler sadece bunlar:
1. Kabloları bağlamak
2. `config.h` içine WiFi adını ve şifresini yazmak
3. Kodu yüklemek

## 1. Malzeme

| Parça | Not |
|---|---|
| ESP32 DevKit (ESP32-WROOM-32) | ESP32-S3 de olur; sadece `LED_PIN` değişebilir |
| WS2812B adreslenebilir LED × 50 | Şerit veya tekli piksel (8 mm / 12 mm "string" tipi pano için çok uygundur) |
| 5 V / 4 A adaptör | Tek LED yandığı için pratikte çok daha az akım çeker; açılış testi ve pay için 4 A |
| 74AHCT125 (veya 74HCT245) seviye dönüştürücü | 3.3 V data → 5 V. Kısa kabloda olmadan da çalışabilir ama önerilir |
| 330 Ω direnç | Data hattına seri |
| 1000 µF / 10 V elektrolitik kondansatör | LED şeridi besleme girişine, + ve − arasına |

## 2. Bağlantı

```
 5V Adaptör (+) ───────────────┬──────────────► LED şeridi 5V
                               ├──► ESP32 5V (VIN) pini
                               └──► 74AHCT125 VCC
 5V Adaptör (−) ───────────────┬──────────────► LED şeridi GND
                               ├──► ESP32 GND          (ORTAK GND ŞART)
                               └──► 74AHCT125 GND, 1OE

 ESP32 GPIO16 ──► 74AHCT125 1A │ 1Y ──[330 Ω]──► LED şeridi DIN (ilk LED = Adalet)

 1000 µF kondansatör: LED şeridinin 5V ile GND'si arasına, şeridin girişine yakın
```

- **Ok yönü:** WS2812B şeritlerde veri yönü oklarla gösterilir. ESP32, oku başlatan uca bağlanır.
- **LED sırası:** İlk LED (0) = **Adalet**, son LED (49) = **Yolculuk**. Sıra `sozluk.json` ile aynıdır.
- **Farklı sıra:** Panoda kelimeleri farklı dizerseniz `config.h` içinde `HARITA_KULLAN 1` yapıp `LED_HARITASI` tablosunu doldurun. Kablolamayı değiştirmeniz gerekmez.
- **Uzun şerit:** 50 LED ve uzun kablo varsa 5 V beslemeyi şeridin her iki ucundan da verin (power injection).
- **USB ile çalışırken:** Kod yüklerken ESP32 USB'ye takılıyken adaptör de bağlı olabilir. Ancak LED'leri asla sadece USB'den beslemeyin.

## 3. Arduino IDE ile yükleme

1. **ESP32 kart desteğini ekleyin.**
   - Arduino IDE → Ayarlar → "Ek Kart Yöneticisi URL'leri" alanına şunu ekleyin: `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
   - Kart Yöneticisi'nden **esp32 (Espressif Systems)** paketini kurun.
2. **Kütüphaneleri kurun.** Kütüphane Yöneticisi'nden şu ikisini kurun:
   - **FastLED** (Daniel Garcia)
   - **PubSubClient** (Nick O'Leary)
3. **Projeyi açın.** `yasayan_sozluk_esp32` klasörünü açın. `.ino` ve `config.h` aynı klasörde olmalı.
4. **`config.h` dosyasını düzenleyin.** `WIFI_AGLARI` içine mekânın WiFi adını ve şifresini yazın. Yedek olarak bir telefon hotspot'u da ekleyebilirsiniz.
5. **Kartı seçin ve yükleyin.**
   - Kart: **ESP32 Dev Module**, port: ESP32'nin bağlı olduğu COM portu.
   - Ardından **Yükle** düğmesine basın.
6. **Seri Monitörü açın (115200 baud).** Şunları görmelisiniz:
   ```
   === Yaşayan Sözlük — ESP32 ===
   [WiFi] bağlandı: ...  IP: ...  RSSI: ... dBm
   [MQTT] bağlandı
   ```
   Siteden bir kelimeye tıklayınca `[LED] 0 yakılıyor` satırı çıkar ve LED yanar.

## 4. Davranış

| Durum | Ne olur |
|---|---|
| Açılış | Tüm LED'ler sırayla mavi yanıp söner (kablolama ve sıra testi) |
| Kelimeye tıklama | O LED 0,6 sn'de yumuşakça yanar, 10 sn yanık kalır, yumuşakça söner |
| Başka kelimeye tıklama | Önceki LED hemen söner, yenisi yanar (son tıklayan kazanır) |
| Kart üzerindeki mavi LED | Sabit yanıyorsa WiFi ve MQTT tamam; yanıp sönüyorsa bağlantı yok |
| Elektrik veya WiFi gider | Broker otomatik "offline" yayınlar, sitede "Işık kapalı" görünür. Bağlantı gelince ESP32 kendiliğinden yeniden bağlanır |
| Hatalı veya kötü niyetli komut | 0–49 dışındaki, sayı olmayan ya da saniyede 6'dan sık gelen komutlar yok sayılır |

Renk, parlaklık ve süre ayarları `config.h` içindedir (`YAKMA_RENGI`, `PARLAKLIK`, `LED_SURE_MS`).
Sitedeki `config.js` → `ledSuresiSn` değerini de `LED_SURE_MS` ile aynı tutun.

## 5. Test durumu

Bu firmware, gerçek PubSubClient kütüphanesiyle ve donanım yerine taklit WiFi/FastLED katmanıyla bilgisayarda derlenip çalıştırıldı. Test edilenler:
- Site → broker → firmware zinciri uçtan uca
- Yumuşak yanma ve sönme süreleri
- Hatalı komutların reddedilmesi
- "online" ve LWT ile "offline" bildirimleri

Gerçek ESP32 araç zinciriyle derleme, donanım geldiğinde Arduino IDE'de yapılacak.
