// =====================================================================
//  Yaşayan Sözlük — Uygulama
//  Akış: kelimeye tıkla → detay kartı aç + MQTT ile "sozluk/led" = indeks
//  MQTT ayarı yoksa TEST MODU: komut sanal LED şeridinde gösterilir.
// =====================================================================
(() => {
  const CFG = Object.assign({ ledSayisi: 50, ledSuresiSn: 60, sanalSerit: "auto", gorselModu: "otomatik" }, window.SOZLUK_CONFIG || {});
  const $ = (id) => document.getElementById(id);
  const debug = new URLSearchParams(location.search).has("debug");
  const ISIK = CFG.isikSistemi !== false;   // false → LED/MQTT tamamen devre dışı

  let sozluk = [];
  let secili = null;
  let gorselSayac = 0;
  let mqttClient = null;
  let testModu = !(CFG.mqtt && CFG.mqtt.url);
  const ses = new Audio();
  ses.preload = "none";

  // ---------- Yardımcılar ----------
  const trKucuk = (s) => s.replace(/I/g, "ı").replace(/İ/g, "i").toLocaleLowerCase("tr");
  const sade = (s) => trKucuk(s).replace(/[çğıöşüâîû]/g, (c) => ({ç:"c",ğ:"g",ı:"i",ö:"o",ş:"s",ü:"u",â:"a",î:"i",û:"u"}[c]));
  let bildirimZaman;
  function bildir(metin) {
    const b = $("bildirim");
    b.textContent = metin;
    b.classList.add("goster");
    clearTimeout(bildirimZaman);
    bildirimZaman = setTimeout(() => b.classList.remove("goster"), 2600);
  }
  function durumAyarla(sinif, yazi) {
    $("durum").className = "durum " + sinif;
    $("durumYazi").textContent = yazi;
  }

  // ---------- Liste ----------
  function listeyiCiz(filtre = "") {
    const f = sade(filtre.trim());
    const ol = $("liste");
    ol.innerHTML = "";
    let adet = 0;
    for (const k of sozluk) {
      if (f && !sade(k.tr).includes(f) && !k.ar.includes(filtre.trim())) continue;
      adet++;
      const li = document.createElement("li");
      li.innerHTML = `<button class="kelime" data-id="${k.id}">
          <span class="k-no">${String(k.id).padStart(2, "0")}</span>
          <span class="k-tr">${k.tr}${k.ses_var ? ' <i class="k-ses" title="Sesli">🔊</i>' : ""}</span>
          <span class="k-ar" lang="ar">${k.ar_harakeli.split(" / ")[0]}</span>
        </button>`;
      ol.appendChild(li);
    }
    $("bos").hidden = adet > 0;
    aktifIsaretle();
  }
  function aktifIsaretle() {
    document.querySelectorAll(".kelime").forEach((b) =>
      b.classList.toggle("aktif", secili && +b.dataset.id === secili.id));
  }

  // ---------- Detay ----------
  function detayAc(k, ledGonderilsin = true) {
    secili = k;
    sesiDurdur();
    $("dNo").textContent = `${String(k.id).padStart(2, "0")} / ${sozluk.length}`;
    $("dBaslik").textContent = k.tr;
    $("dArapca").textContent = k.ar_harakeli;
    $("dGorselYazi").textContent = k.ar_harakeli.split(" / ")[0];
    $("dSoz").textContent = k.soz || "";
    $("sozKutu").hidden = !k.soz;

    // Görsel sırası (gorselModu "otomatik"): img/foto/<slug>.jpg → yoksa hat levhası → yoksa düz zemin.
    // Foto gösterilirken Arapça kartuş ve Mevlânâ çerçevesi üstüne eklenir; hat levhasında zaten içindedir.
    const img = $("dGorsel"), yedek = $("dGorselYedek"), kap = $("gorselKap");
    const sira = { otomatik: [k.foto, k.hat], hat: [k.hat] }[CFG.gorselModu] || [k.foto, k.hat];
    const adaylar = sira.filter(Boolean);
    let i = 0;
    img.hidden = false; yedek.hidden = true; img.alt = k.tr;
    const dene = () => {
      if (i >= adaylar.length) { img.hidden = true; yedek.hidden = false; kap.classList.remove("hat-modu"); return; }
      const src = adaylar[i++];
      kap.classList.toggle("hat-modu", src === k.hat);
      img.src = src;
    };
    const benim = ++gorselSayac;            // hızlı geçişte eski kartın hatası yenisini etkilemesin
    img.onerror = () => { if (benim === gorselSayac) dene(); };
    dene();

    // Ses: dosya yoksa buton soluk görünür
    const btn = $("sesBtn");
    if (k.ses_var === false) {            // tools/medya_hazirla.py işaretler; yoksa boşuna istek atma
      btn.classList.add("yok");
      ses.removeAttribute("src");
    } else {
      btn.classList.remove("yok");
      ses.src = k.ses;
      ses.preload = "auto";
      ses.load();
    }

    $("perde").hidden = false;
    $("detay").hidden = false;
    document.body.style.overflow = "hidden";
    if (location.hash !== "#" + k.slug) history.replaceState(null, "", "#" + k.slug);
    aktifIsaretle();
    if (ledGonderilsin) ledYak(k.led);
  }
  function detayKapat() {
    sesiDurdur();
    ledSondur();
    $("perde").hidden = true;
    $("detay").hidden = true;
    document.body.style.overflow = "";
    history.replaceState(null, "", location.pathname + location.search);
  }

  // ---------- Ses ----------
  function sesiDurdur() {
    ses.pause();
    try { ses.currentTime = 0; } catch (_) {}
    $("sesBtn").classList.remove("caliyor");
    $("sesIlerleme").style.width = "0";
  }
  $("sesBtn").addEventListener("click", () => {
    if ($("sesBtn").classList.contains("yok")) { bildir("Bu kelimenin sesi henüz eklenmedi."); return; }
    if (!ses.paused) { sesiDurdur(); return; }
    ses.play().then(() => $("sesBtn").classList.add("caliyor"))
      .catch(() => { $("sesBtn").classList.add("yok"); bildir("Bu kelimenin sesi henüz eklenmedi."); });
  });
  ses.addEventListener("error", () => { if (ses.src) $("sesBtn").classList.add("yok"); $("sesBtn").classList.remove("caliyor"); });
  ses.addEventListener("ended", () => { $("sesBtn").classList.remove("caliyor"); $("sesIlerleme").style.width = "100%"; });
  ses.addEventListener("timeupdate", () => {
    if (ses.duration) $("sesIlerleme").style.width = (100 * ses.currentTime / ses.duration) + "%";
  });

  // ---------- LED komutu ----------
  let bizimLed = null;   // bu telefonun yaktığı LED (kart açıkken)
  function ledSondur() {
    if (!ISIK || bizimLed === null) return;
    // "off:N" → ESP32 sadece N hâlâ yanıyorsa söndürür; başka ziyaretçinin ışığına dokunmaz
    if (mqttClient && mqttClient.connected) mqttClient.publish(CFG.mqtt.topicLed, "off:" + bizimLed, { qos: 0, retain: false });
    const l = document.querySelectorAll(".led")[bizimLed];
    if (l) l.classList.remove("yanik");
    bizimLed = null;
  }
  // Telefon kilitlenir / sekme kapanırsa ışığı söndür
  window.addEventListener("pagehide", ledSondur);
  document.addEventListener("visibilitychange", () => { if (document.hidden) ledSondur(); });

  function ledYak(indeks) {
    if (!ISIK) return;
    bizimLed = indeks;
    if (mqttClient && mqttClient.connected) {
      mqttClient.publish(CFG.mqtt.topicLed, String(indeks), { qos: 0, retain: false });
    } else if (!testModu) {
      bildir("Işık sistemine şu an ulaşılamıyor.");
    }
    sanalLed(indeks);
  }

  // ---------- Sanal LED şeridi ----------
  let sanalZaman;
  function seritKur() {
    const goster = debug || CFG.sanalSerit === true || (CFG.sanalSerit === "auto" && testModu);
    $("serit").hidden = !goster;
    if (!goster) return;
    const kap = $("ledler");
    for (let i = 0; i < CFG.ledSayisi; i++) {
      const d = document.createElement("div");
      d.className = "led"; d.title = `LED ${i}`;
      kap.appendChild(d);
    }
    $("seritBilgi").textContent = testModu ? "(test modu — ESP32 yerine)" : "(ESP32 ile eş zamanlı)";
    document.querySelector("main").style.paddingBottom = "150px";
  }
  function sanalLed(indeks) {
    const ledler = document.querySelectorAll(".led");
    if (!ledler.length) return;
    ledler.forEach((l, i) => l.classList.toggle("yanik", i === indeks));
    clearTimeout(sanalZaman);
    sanalZaman = setTimeout(() => ledler.forEach((l) => l.classList.remove("yanik")), CFG.ledSuresiSn * 1000);
  }

  // ---------- MQTT ----------
  function mqttBaglan() {
    if (testModu) { durumAyarla("test", "Test modu"); return; }
    if (!window.mqtt) { durumAyarla("offline", "Kütüphane yok"); return; }
    durumAyarla("", "Bağlanıyor…");
    mqttClient = mqtt.connect(CFG.mqtt.url, {
      username: CFG.mqtt.username,
      password: CFG.mqtt.password,
      clientId: "web-" + Math.random().toString(16).slice(2, 10),
      reconnectPeriod: 3000,
      connectTimeout: 8000,
      clean: true
    });
    mqttClient.on("connect", () => {
      durumAyarla("", "Işık aranıyor…");
      mqttClient.subscribe(CFG.mqtt.topicDurum);
    });
    mqttClient.on("message", (topic, msg) => {
      if (topic !== CFG.mqtt.topicDurum) return;
      const online = msg.toString() === "online";
      durumAyarla(online ? "online" : "offline", online ? "Işık bağlı" : "Işık kapalı");
    });
    mqttClient.on("reconnect", () => durumAyarla("", "Yeniden bağlanıyor…"));
    mqttClient.on("offline", () => durumAyarla("offline", "Bağlantı yok"));
    mqttClient.on("error", (e) => { console.warn("MQTT:", e.message); durumAyarla("offline", "Bağlantı hatası"); });
  }

  // ---------- Olaylar ----------
  $("liste").addEventListener("click", (e) => {
    const b = e.target.closest(".kelime");
    if (b) detayAc(sozluk.find((k) => k.id === +b.dataset.id));
  });
  $("ara").addEventListener("input", (e) => listeyiCiz(e.target.value));
  $("kapat").addEventListener("click", detayKapat);
  $("perde").addEventListener("click", detayKapat);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") detayKapat(); });

  // ---------- Başlat ----------
  fetch("sozluk.json", { cache: "no-cache" })
    .then((r) => r.json())
    .then((veri) => {
      sozluk = veri;
      listeyiCiz();
      if (ISIK) { $("durum").hidden = false; seritKur(); mqttBaglan(); }
      // Doğrudan kelime bağlantısı: ...#adalet  (LED yakmaz, sadece kartı açar)
      const h = decodeURIComponent(location.hash.slice(1));
      const k = h && sozluk.find((x) => x.slug === h);
      if (k) detayAc(k, false);
    })
    .catch(() => bildir("Sözlük yüklenemedi."));
})();
