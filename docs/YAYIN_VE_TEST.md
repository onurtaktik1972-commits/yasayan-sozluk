# Yayın, Telefonda Test ve Sergiye Geçiş

## A. Hemen telefonda deneme (yayın yapmadan, 2 dakika)

1. **Sunucuyu başlatın.** Zip'i açın; klasörde bir terminal açıp şunu çalıştırın: `python -m http.server 8000`
2. **IP adresini öğrenin.** Windows'ta `ipconfig` komutundaki IPv4 adresi kullanılır, örneğin `192.168.1.34`.
3. **ESP32 taklitçisini açın.** Bilgisayarın tarayıcısında `http://localhost:8000/esp32-taklit.html` adresini açın. Durum rozeti "Broker'a bağlı" olmalı.
4. **QR'ı oluşturun.** `http://localhost:8000/qr.html?url=http://192.168.1.34:8000/` adresini açın. Ekranda bilgisayarınızın IP'sini içeren bir QR çıkar.
5. **Telefonla okutun.** Telefon bilgisayarla aynı WiFi'de olmalı. QR'ı okutun, sözlük açılır ve sağ üstte "Işık bağlı" görünür.
6. **Deneyin.** Telefonda bir kelimeye dokunun; bilgisayardaki taklitçide o kelimenin LED'i yanar.

> Windows Güvenlik Duvarı Python için izin sorarsa "Özel ağlar" seçeneğine izin verin.

## B. Kalıcı yayın: GitHub Pages (ücretsiz, HTTPS)

1. **Hesap açın.** github.com'da bir hesap açın (varsa geçin).
2. **Depo oluşturun.** Sağ üstteki **+** → **New repository** yolunu izleyin.
   - Ad: `yasayan-sozluk`
   - Görünürlük: **Public**
   - **Create** düğmesine basın.
3. **Dosyaları yükleyin.**
   - Depo sayfasında **"uploading an existing file"** bağlantısına tıklayın.
   - Zip'ten çıkan klasörün **içindekileri** sürükleyip bırakın. `index.html` en üst seviyede olmalı.
   - **Commit changes** düğmesine basın.
4. **Pages'i açın.** **Settings** → **Pages** → Source: **Deploy from a branch**, Branch: **main**, klasör **/(root)** seçip **Save**'e basın.
5. **Adresi bekleyin.** 1–2 dakika sonra site `https://KULLANICI_ADINIZ.github.io/yasayan-sozluk/` adresinde yayında olur.
6. **QR'ı basın.** `https://KULLANICI_ADINIZ.github.io/yasayan-sozluk/qr.html` adresini açın. Adres otomatik dolar; **Yazdır (A5)** ya da **PNG indir** ile QR'ı alın.

Ses veya görsel eklemek için `audio/` ve `img/` klasörlerine dosyaları aynı yöntemle yükleyin. Site 1–2 dakika içinde güncellenir. QR kod değişmez.

## C. Sergiye geçiş: kendi özel broker'ınız (HiveMQ Cloud, ücretsiz)

Şu an sistem HiveMQ'nun **herkese açık** broker'ını kullanıyor. Test için idealdir, hesap gerekmez. Ancak bu broker'ın erişilebilirlik garantisi yoktur ve konu adını bilen herkes LED yakabilir. Sergiden önce özel broker'a geçin:

1. **Hesap ve cluster.** console.hivemq.cloud adresinde hesap açın ve **Serverless (Free)** bir cluster oluşturun.
2. **Adresi not edin.** Cluster sayfasında şu bilgiler yazar:
   - **Cluster URL**: `xxxxxxxx.s1.eu.hivemq.cloud`
   - TLS port **8883**, WebSocket port **8884**
3. **Kullanıcıları oluşturun.** **Access Management** → **Credentials** bölümünde iki kullanıcı açın:
   - `web_publisher`: şifresi sitede görünür olacak, bu yüzden yetkisi kısıtlı olmalı
   - `esp32_user`: güçlü bir şifre verin
4. **Yetkileri kısıtlayın.** Free planda izin (permission) seçenekleri sınırlıysa en azından kullanıcıları ayırın ve konu adını tahmin edilemez tutun. Planınız izin veriyorsa:
   - `web_publisher`: `yasayansozluk/40c411/led` → **Publish**, `yasayansozluk/40c411/durum` → **Subscribe**
   - `esp32_user`: `.../led` → **Subscribe**, `.../durum` → **Publish**
5. **Site tarafını güncelleyin.** `config.js` dosyasında şunları değiştirin:
   ```js
   url: "wss://xxxxxxxx.s1.eu.hivemq.cloud:8884/mqtt",
   username: "web_publisher",
   password: "…",
   ```
6. **ESP32 tarafını güncelleyin.** `config.h` dosyasında şunları değiştirin:
   ```cpp
   #define MQTT_HOST      "xxxxxxxx.s1.eu.hivemq.cloud"
   #define MQTT_PORT      8883
   #define MQTT_TLS       1
   #define MQTT_KULLANICI "esp32_user"
   #define MQTT_SIFRE     "…"
   ```

Başka kod değişikliği gerekmez. Değişiklikten sonra `esp32-taklit.html` ile tekrar test edin.

> Ek güvenlik için ESP32 her durumda 0–49 dışındaki komutları ve saniyede 6'dan sık gelenleri yok sayar. Biri şifreyi ele geçirse bile en fazla bir LED yakabilir.
