# Yaşayan Sözlük

QR kod ile açılan mobil sözlük. Bir kelimeye dokunulduğunda telefonda kelimenin kartı açılır, kelimenin sesi çalınabilir ve sergideki ilgili adreslenebilir LED yanar.

```
Telefon (GitHub Pages sitesi) ──WSS──► HiveMQ Cloud ──TLS──► ESP32 ──► WS2812B × 50
        sozluk/led = "0..49"                           sozluk/durum = online/offline
```

## Klasör yapısı

| Yol | İçerik |
|---|---|
| `index.html`, `style.css`, `app.js` | Mobil web uygulaması (QR'ın açtığı sayfa) |
| `config.js` | MQTT broker ve konu adları. `url` boş bırakılırsa **test modu** çalışır. |
| `sozluk.json` | 50 kelime (alfabetik): Arapça, TDK anlamları, köken, LED no, görsel/ses yolu |
| `esp32-taklit.html` | Donanım gelene kadar ESP32'nin yerine geçen sanal LED panosu |
| `qr.html` | Baskıya hazır A5 QR afişi; SVG ve PNG indirme |
| `img/` | Kelime görselleri (`<slug>.svg`; isterseniz kendi `.webp` / `.jpg` dosyalarınızla değiştirin) |
| `audio/` | Kelime sesleri: `<slug>.mp3` (bekleniyor) |
| `firmware/` | ESP32 kodu, kablolama ve yükleme rehberi |
| `docs/YAYIN_VE_TEST.md` | Telefonda test, GitHub Pages yayını, özel broker'a geçiş |
| `docs/medya_listesi.csv` | 50 kelimenin ses ve görsel dosya adları, hazırlık takip listesi |

## Fazlar

| Faz | İş | Donanım? | Durum |
|---|---|---|---|
| 1 | Veri: sıralı sözlük, LED eşlemesi, dosya adları | Hayır | ✅ |
| 2 | Mobil arayüz, Mevlânâ çerçeveli görseller, ses ikonu | Hayır | ✅ |
| 3 | MQTT bağlantısı, ESP32 taklitçisi, QR afişi | Hayır | ✅ (uçtan uca test edildi) |
| 4 | ESP32 firmware (WiFi, MQTT, FastLED, LWT, yumuşak geçiş) | Derleme için hayır | ✅ (bilgisayarda derlendi ve test edildi) |
| 5 | GitHub Pages yayını + QR baskısı | Hayır | ⏳ Sizde — `docs/YAYIN_VE_TEST.md` (B) |
| 6 | 50 ses dosyasının `audio/` klasörüne eklenmesi | Hayır | ⏳ Dosyalar bekleniyor |
| 7 | Sergi öncesi özel broker (HiveMQ Cloud) | Hayır | ⏳ `docs/YAYIN_VE_TEST.md` (C) |
| 8 | Kod yükleme, LED kablolama, saha testi | **Evet** | ⏳ `firmware/README.md` |

## Medya kuralları

Dosya adı, `sozluk.json` içindeki `slug` değeriyle **birebir aynı** olmalıdır: Türkçe karakter yok, küçük harf. Örnekler: `alcakgonulluluk.mp3`, `sukur.webp`. Tam liste `docs/medya_listesi.csv` dosyasında.

**Ses (`audio/<slug>.mp3`)**
- MP3, mono, 44.1 kHz, 96 kbps
- Süre 3–15 sn; başta ve sonda en fazla 0.3 sn sessizlik
- Ses seviyesi tüm dosyalarda eşit olmalı (yaklaşık −16 LUFS)
- Dosya boyutu tercihen 200 KB'tan küçük

**Görsel (`img/<slug>.svg`)**
- Her kelime için minyatür üslubunda, Mevlânâ imgelerinden (semâ, ney, pervane ile mum, gül, Yedi Öğüt) yola çıkan özel bir illüstrasyon var. Arapça kartuş ve Mevlânâ çerçevesi uygulama tarafından üzerine eklenir. Kaynak kod: `tools/sahneler.py`.
- Kendi görselinizi kullanmak isterseniz 1200×900 (4:3) WebP veya JPG hazırlayın ve `sozluk.json` içindeki `gorsel` alanını o dosyayı gösterecek şekilde değiştirin.

Bir kelimenin dosyası henüz yoksa uygulama bozulmaz. Ses butonu soluklaşır ve "ses henüz eklenmedi" uyarısı çıkar. Yeni dosyalar klasöre atılıp yayınlandığında kod değişikliği gerekmeden görünür.

> Ses, kullanıcı ses ikonuna dokunduğunda çalar. iOS ve Android tarayıcıları, dokunma olmadan otomatik ses çalmaya izin vermez.

## Yerelde deneme

```bash
cd yasayan-sozluk
python -m http.server 8000
# tarayıcıda: http://localhost:8000      (adrese ?debug=1 eklenirse LED şeridi her zaman görünür)
```

Aynı WiFi'deki bir telefondan `http://<bilgisayar-IP>:8000` adresiyle de açılabilir.
Bir kelimeye doğrudan bağlantı vermek için adresin sonuna `#adalet` gibi slug eklenebilir.

## Kaynaklar ve lisanslar

- **Anlamlar:** TDK Güncel Türkçe Sözlük (12. baskı, sozluk.gov.tr). Kelimeler için ilgili anlamlar seçilmiştir; "►" yönlendirmeleri açılmıştır.
- **Görseller:** Projeye özel çizildi (SVG, kod ile üretildi).
- **Yazı tipleri:** Amiri, Cormorant Garamond, Inter (Google Fonts, OFL).
