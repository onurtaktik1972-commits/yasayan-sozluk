// =====================================================================
//  Yaşayan Sözlük — Uygulama
//  Akış: kelimeye tıkla → detay kartı aç + MQTT ile "sozluk/led" = indeks
//  MQTT ayarı yoksa TEST MODU: komut sanal LED şeridinde gösterilir.
// =====================================================================
(() => {
  const CFG = Object.assign({ ledSayisi: 50, ledSuresiSn: 10, sanalSerit: "auto" }, window.SOZLUK_CONFIG || {});
  const $ = (id) => document.getElementById(id);
  const debug = new URLSearchParams(location.search).has("debug");

  let sozluk = [];
  let secili = null;
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
          <span class="k-tr">${k.tr}</span>
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
    $("dKoken").textContent = k.koken || "";
    $("dTdk").innerHTML = (k.tdk || []).map((a) => {
      const m = a.match(/^\(([^)]+)\)\s*(.*)$/);   // "(özlem) ..." → bkz. yönlendirmesi
      return m ? `<li><span class="bk">${m[1]}:</span> ${m[2]}</li>` : `<li>${a}</li>`;
    }).join("");

    // Görsel: dosya yoksa düz lacivert zemin
    const img = $("dGorsel"), yedek = $("dGorselYedek");
    img.hidden = false; yedek.hidden = true;
    img.alt = k.tr;
    img.onerror = () => { img.hidden = true; yedek.hidden = false; };
    img.src = k.gorsel;

    // Ses: dosya yoksa buton soluk görünür
    const btn = $("sesBtn");
    btn.classList.remove("yok");
    ses.src = k.ses;
    ses.load();

    $("perde").hidden = false;
    $("detay").hidden = false;
    document.body.style.overflow = "hidden";
    if (location.hash !== "#" + k.slug) history.replaceState(null, "", "#" + k.slug);
    aktifIsaretle();
    if (ledGonderilsin) ledYak(k.led);
  }
  function detayKapat() {
    sesiDurdur();
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
  function ledYak(indeks) {
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
      seritKur();
      mqttBaglan();
      // Doğrudan kelime bağlantısı: ...#adalet  (LED yakmaz, sadece kartı açar)
      const h = decodeURIComponent(location.hash.slice(1));
      const k = h && sozluk.find((x) => x.slug === h);
      if (k) detayAc(k, false);
    })
    .catch(() => bildir("Sözlük yüklenemedi."));
})();
