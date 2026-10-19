# Yaşayan Sözlük

Mevlânâ ve Mesnevî'den ilham alan 50 kelimelik sözlük. Ziyaretçi QR kodu okutur ve bir kelimeye dokunur. Telefonunda kelimenin görseli, Arapçası, sesi ve özlü sözü açılır; sergi panosunda da o kelimenin LED'i yanar.

- **Adres:** https://onurtaktik1972-commits.github.io/yasayan-sozluk/
- **QR kod:** `docs/qr/` (A5 afiş PDF, PNG, SVG). Adres değişmediği sürece QR hep aynıdır.
- **Nasıl çalışıyor:** `docs/CALISMA_MANTIGI.md` dosyasına bakın.
- **ESP32 kodu:** Ayrı paket olarak duruyor: `esp32-yasayan-sozluk`.

## Klasör

| Dosya | İçerik |
|---|---|
| `index.html`, `app.js`, `style.css` | Sözlük sayfası (QR'ın açtığı sayfa) |
| `config.js` | Işık sistemi (MQTT broker) ayarları ve görsel modu |
| `sozluk.json` | 50 kelime: Türkçe, Arapça, özlü söz, LED numarası, dosya yolları |
| Fotoğraflar | Unsplash'ten doğrudan gösterilir (adresleri `sozluk.json` → `foto`). Değiştirmek için adresi değiştirin. |
| `audio/` | Kelime sesleri (`<slug>.mp3`) |
| `esp32-taklit.html` | Donanım gelene kadar ESP32'nin yerine geçen sanal LED panosu |
| `qr.html` | QR afişi üretme ve yazdırma sayfası |
| `docs/medya_listesi.csv` | 50 kelimenin dosya adları ve sözleri |

## Bir sözü değiştirmek
`sozluk.json` içinde ilgili kelimenin `"soz"` satırını değiştirip dosyayı GitHub'a yeniden yükleyin.

## GitHub'a yükleme
1. Depo sayfasında **Add file → Upload files** deyin.
2. Bu klasörün **içindekileri** sürükleyip bırakın.
3. **Commit changes**'a basın.

Site 1–2 dakikada güncellenir.
