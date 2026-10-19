import json, sys
sys.path.insert(0, "tools")
from sahne import *

def basak_egik(x, yb, h, i):
    o = f'<path d="M{x} {yb} Q{x+10} {yb-h*.7} {x+70} {yb-h}" stroke="#c9a24a" stroke-width="5" fill="none"/>'
    tx, ty = x + 70, yb - h
    for k in range(7):
        px, py = tx + 10 + k*7, ty + 14 + k*18
        for sg in (-1, 1):
            o += f'<ellipse cx="{px+sg*8}" cy="{py}" rx="7" ry="15" fill="#e8c06a" stroke="#b08a3c" stroke-width="1" transform="rotate({sg*30-15} {px+sg*8} {py})"/>'
    return o

def S(*parcalar): return "".join(parcalar)
GB = "#0f2245"   # hilal için gök rengi (gece)

SAHNE = {
"adalet": lambda: S(gok("gece"), yildizlar(60, 1), kemer(), terazi(600, 690, 470)),
"affetmek": lambda: S(gok("gece"), yildizlar(110, 2, 600), hilal(860, 190, 70, gokrenk="#0e1f40"),
    '<path d="M0 520 Q300 440 600 500 T1200 470 V900 H0Z" fill="#1b2f58" opacity=".7"/>', sehir(800, "#0a1630"),
    turbe(600, 760, .9, "#0a1630")),
"akil": lambda: S(gok("gece"), yildizlar(50, 3), kandil(600, 0, 330, 80), kitap(600, 700, 460, 230, isik=False)),
"alcakgonulluluk": lambda: S(gok("col"), gunes(600, 560, 60, False), tepeler(620, "#6b4a3a", "#4a2f22"),
    f'<rect x="0" y="760" width="{W}" height="140" fill="url(#gToprak)"/>',
    S(*[basak_egik(x, 800, 380 + (i % 3) * 40, i) for i, x in enumerate(range(140, 1100, 120))])),
"anlayis": lambda: S(gok("safak"), gunes(600, 470, 60), kitap(600, 690, 520, 250), ses_dalgalari(600, 300, 0)),
"arayis": lambda: S(gok("gece"), yildizlar(90, 6, 500), tepeler(700), yol_sahnesi(600, 520),
    fener(760, 440, .85)),
"ask": lambda: S(gok("gece"), yildizlar(40, 7, 400), mum(600, 760, 260, 70),
    spiral(600, 330, 230, 1.6, P['gold'], .35, 3),
    pervane(400, 300, .9, -20), pervane(820, 230, .7, 25), pervane(760, 420, .55, 40)),
"ates": lambda: S(gok("gece"), '<rect width="1200" height="900" fill="#3a1208" opacity=".35"/>',
    alev(480, 760, 380), alev(700, 760, 300), alev(600, 780, 460), ney(240, 640, 720, -24, 30)),
"ayrilik": lambda: S(gok("safak"), '<rect x="0" y="640" width="1200" height="260" fill="url(#gSu)"/>',
    dalgalar(670, 5, "#9fd0ea", 8, 120, 3, .6), sazlik(40, 620, 700, 26), ney(720, 380, 420, -12, 20),
    kus_suru(900, 180, 3, 1.1)),
"baris": lambda: S(gok("gun"), sehir(820, "#2b4b6e"), turbe(600, 800, .8, "#2b4b6e"), kus(600, 300, 1.6, dal=True)),
"bilgelik": lambda: S(gok("gece"), yildizlar(50, 9), kemer(), kitap(600, 470, 380, 200),
    f'<rect x="380" y="500" width="440" height="40" fill="#5a2e22"/><rect x="400" y="540" width="400" height="40" fill="#1f4a6e"/><rect x="370" y="580" width="460" height="40" fill="#6e3a2a"/>',
    kandil(890, 0, 260, 50)),
"birlik": lambda: S(gok("gece"), yildizlar(80, 10), '<circle cx="600" cy="470" r="330" fill="url(#gIsik)" opacity=".5"/>',
    spiral(600, 640, 420, 2, P['gold'], .3, 3),
    S(*[semazen(600 + 330*math.cos(a), 640 + 90*math.sin(a), 210 + 40*math.sin(a), ters=bool(i%2))
        for i, a in sorted(enumerate([2*math.pi*k/7 - math.pi/2 for k in range(7)]), key=lambda t: math.sin(t[1]))])),
"comertlik": lambda: S(gok("gun"), dag(250, 520, 520, 300, "#3f6a8a"), dag(900, 520, 600, 340, "#355d80"),
    '<rect x="0" y="500" width="1200" height="400" fill="#4f8a4a"/>', nehir(),
    agac(220, 760, 330, 140, 5, seed=3), agac(1000, 760, 300, 130, 4, seed=4)),
"dinlemek": lambda: S(gok("gece"), yildizlar(60, 11), ney(200, 560, 760, -20, 30), ses_dalgalari(930, 300, 5, aci=-20)),
"dogruluk": lambda: S(gok("safak"), tepeler(720, "#2a3b62", "#1a2a4a"), servi(600, 780, 600, 110),
    servi(380, 780, 380, 70, "#183f2e"), servi(820, 780, 380, 70, "#183f2e"), gunes(600, 140, 45, False)),
"dostluk": lambda: S(gok("gece"), yildizlar(60, 12), '<circle cx="600" cy="470" r="300" fill="url(#gIsik)" opacity=".45"/>',
    golge_elips(440, 760, 150), golge_elips(760, 760, 150), semazen(440, 760, 400), semazen(760, 760, 400, ters=True)),
"donusum": lambda: S(gok("gece"), yildizlar(70, 13), spiral(600, 520, 460, 3.2, P['gold'], .45, 4),
    spiral(600, 520, 300, 2.4, P['tur2'], .4, 3), semazen(600, 760, 480, donme=-6)),
"golge": lambda: S(gok("col"), gunes(1020, 470, 60), f'<rect x="0" y="620" width="{W}" height="280" fill="#b07a45"/>',
    '<g transform="translate(590 770) skewX(58) scale(1.1 .5)" opacity=".6">' + semazen(0, 0, 400, ters=True, renk_etek="#2a1a10").replace('fill="#f7f1e4"','fill="#2a1a10"').replace('fill="#e8c7a0"','fill="#2a1a10"').replace('fill="#a9825a"','fill="#2a1a10"').replace('stroke="#f7f1e4"','stroke="#2a1a10"') + '</g>',
    semazen(600, 770, 400, ters=True)),
"gonul": lambda: S(gok("gece"), yildizlar(50, 14), kalp_suslu(600, 420, 1.15),
    gul(330, 560, 40), gul(870, 560, 40), gul(600, 600, 34, sap=False, yaprak=False)),
"guzellik": lambda: S(gok("gece"), yildizlar(40, 15), '<circle cx="600" cy="380" r="300" fill="url(#gIsik)" opacity=".6"/>',
    gul(600, 340, 120), gul(360, 520, 50), gul(850, 500, 56)),
"hakikat": lambda: S(gok("safak"), gunes(600, 460, 120), sehir(820, "#0f1e3c"), turbe(600, 800, .95, "#0f1e3c")),
"hasret": lambda: S(gok("gece"), yildizlar(100, 16), hilal(820, 240, 90, gokrenk="#0f2245"),
    tepeler(700), turbe(950, 700, .35, "#0a1630"), insan(330, 720, 190, "#2a3b5a", "#1a2440"), kus_suru(620, 300, 3, .9)),
"hikmet": lambda: S(gok("gece"), yildizlar(50, 17), tomar(560, 420, 560, 340), hokka_kalem(880, 760, .9),
    kandil(220, 0, 230, 46)),
"hosgoru": lambda: S(gok("safak"), gunes(600, 520, 70, False), deniz(560), kus_suru(420, 260, 6, 1.1), kus_suru(860, 330, 4, .8, seed=9)),
"isik": lambda: S(gok("gece"), yildizlar(40, 18), isik_huzmesi(600, 380, 900, 60, 900, .25),
    kandil(600, 0, 360, 110)),
"idrak": lambda: S(gok("safak"), gunes(600, 560, 90), dag(250, 680, 600, 330, "#2b3f6a"), dag(950, 680, 640, 360, "#22355c"),
    dag(600, 700, 700, 230, "#1a2a4a", False), f'<rect x="0" y="680" width="{W}" height="220" fill="#14223f"/>'),
"insanlik": lambda: S(gok("safak"), gunes(600, 420, 80, False), '<path d="M0 760 Q600 620 1200 760 V900 H0Z" fill="#1e3256"/>',
    insan_halkasi(600, 760, 7, 1000)),
"irfan": lambda: S(gok("gece"), yildizlar(80, 19), isik_huzmesi(600, 0, 600, 600, 200, .18), kitap(600, 700, 500, 260),
    S(*[yildiz8(600 + dx, 300 + dy, 14, P['gold'], .9) for dx, dy in [(-120, 40), (90, -30), (10, -120), (160, 80), (-60, -60)]])),
"iyilik": lambda: S(gok("safak"), '<circle cx="600" cy="470" r="320" fill="url(#gIsik)" opacity=".6"/>', ibrik(470, 600, 1.1),
    '<path d="M682 330 Q730 420 712 640" stroke="#9fd8f0" stroke-width="10" fill="none" stroke-linecap="round"/>', kase(720, 760, 300)),
"kalp": lambda: S(gok("gece"), yildizlar(60, 20), kalp_suslu(600, 450, 1.35)),
"kanaat": lambda: S(gok("gece"), yildizlar(50, 21), '<ellipse cx="600" cy="690" rx="420" ry="70" fill="url(#gSu)"/>',
    S(*[f'<ellipse cx="600" cy="690" rx="{60+i*70}" ry="{10+i*12}" fill="none" stroke="#bfe6f6" stroke-width="3" opacity="{.8-i*.15:.2f}"/>' for i in range(5)]),
    damla(600, 380, 70)),
"kardeslik": lambda: S(gok("gun"), '<rect x="0" y="720" width="1200" height="180" fill="#4f8a4a"/>',
    agac(420, 760, 520, 220, 3, seed=7), agac(780, 760, 520, 220, 3, seed=8),
    '<path d="M420 760 Q600 640 780 760" stroke="#5b3a22" stroke-width="20" fill="none"/>', kus(600, 200, .6)),
"kavusma": lambda: S(gok("col"), gunes(600, 400, 60, False), '<rect x="0" y="420" width="1200" height="120" fill="url(#gSu)"/>',
    dalgalar(440, 3, "#9fd0ea", 6, 120, 3, .6), '<rect x="0" y="530" width="1200" height="370" fill="#4f7a44"/>',
    '<path d="M0 900 C160 800 420 700 560 540 L640 540 C500 700 330 820 300 900Z" fill="url(#gSu)"/>',
    '<path d="M1200 900 C1040 800 780 700 640 540 L560 540 C700 700 870 820 900 900Z" fill="url(#gSu)"/>',
    '<path d="M60 900 C220 800 440 690 590 545" stroke="#bfe6f6" stroke-width="4" fill="none" opacity=".6" stroke-dasharray="30 22"/>',
    '<path d="M1140 900 C980 800 760 690 610 545" stroke="#bfe6f6" stroke-width="4" fill="none" opacity=".6" stroke-dasharray="30 22"/>',
    '<circle cx="600" cy="545" r="160" fill="url(#gIsik)" opacity=".7"/>'),
"marifet": lambda: S(gok("gece"), yildizlar(40, 22), deniz(600), istiridye(600, 560, 1.15)),
"merhamet": lambda: S(gok("gun"), gunes(600, 330, 120), '<path d="M0 740 Q300 660 600 720 T1200 700 V900 H0Z" fill="#4f8a4a"/>',
    S(*[lale(x, 820, 120 + (x % 3) * 20, ["#c8323f", "#e2a64a", "#d65a8a"][x % 3]) for x in range(80, 1150, 90)])),
"nefes": lambda: S(gok("gece"), yildizlar(50, 23), ney(160, 600, 640, -18, 28), ruzgar(840, 360, 1.1)),
"ney": lambda: S(gok("gece"), yildizlar(70, 24), kemer(), ney(330, 760, 740, -52, 34), ses_dalgalari(820, 230, 4, aci=-50)),
"niyet": lambda: S(gok("gece"), yildizlar(50, 25), fidan(600, 700, 1.4)),
"olgunluk": lambda: S(gok("col"), '<rect x="0" y="740" width="1200" height="160" fill="#5c3b26"/>',
    agac(600, 770, 620, 280, 14, "#2a6a42", seed=11)),
"ozlem": lambda: S(gok("gece"), yildizlar(80, 26), hilal(860, 210, 80, gokrenk="#0f2245"), kum_saati(450, 470, 460, 260, .3), kus(880, 470, .5)),
"ruh": lambda: S(gok("gece"), yildizlar(110, 27), isik_huzmesi(600, 0, 760, 700, 160, .2),
    tuy(600, 380, 1.2, -18), S(*[yildiz8(600 + dx, 700 - abs(dx)*1.2 - k*120, 10, P['gold'], .8)
                                for k, dx in enumerate([-180, 160, -90, 110, -30])])),
"sabir": lambda: S(gok("safak"), gunes(600, 330, 70, False), dag(600, 760, 900, 560, "#2b3f6a"), dag(220, 780, 500, 300, "#1f3156", False),
    dag(1000, 780, 520, 320, "#1f3156", False), f'<rect x="0" y="760" width="{W}" height="140" fill="#14223f"/>',
    '<path d="M560 420 C540 520 640 560 600 660 C580 720 640 760 620 780" stroke="#bfe6f6" stroke-width="7" fill="none" opacity=".75"/>',
    gul(860, 700, 30), gul(330, 720, 26)),
"sadakat": lambda: S(gok("gece"), yildizlar(60, 28), hilal(260, 170, 60, gokrenk="#0d1d3c"), deniz(560), capa(600, 420, 1.15)),
"samimiyet": lambda: S(gok("gece"), yildizlar(40, 29), ayna(600, 420, 220, 290, ic=gul(600, 380, 90, sap=False, yaprak=False) + '<rect x="0" y="0" width="1200" height="900" fill="#fff" opacity=".08"/>'),
    gul(600, 690, 42)),
"sir": lambda: S(gok("gece"), yildizlar(60, 30), kapi(600, 800, 340, 520), anahtar(880, 640, .55, -30)),
"sukur": lambda: S(gok("safak"), gunes(600, 340, 80), '<rect x="0" y="560" width="1200" height="340" fill="#3f7a44"/>',
    S(*[lale(x, 900 - (x % 4) * 30, 150, ["#c8323f", "#e2a64a", "#d65a8a", "#f4ead5"][x % 4]) for x in range(60, 1180, 64)])),
"tevazu": lambda: S(gok("col"), gunes(600, 640, 70, False), f'<rect x="0" y="740" width="{W}" height="160" fill="url(#gToprak)"/>',
    golge_elips(600, 770, 170, .45), semazen(600, 770, 470, eller="selam")),
"vefa": lambda: S(gok("col"), agac(560, 800, 560, 260, 0, "#355a3a", seed=12),
    f'<path d="M640 360 q40 30 80 0 q-10 30 -40 34 q-30 -4 -40 -34z" fill="#6b4a2a"/>',
    kus(800, 220, .45, ters=True), kus(980, 300, .38, ters=True), kus_suru(1000, 160, 3, .8)),
"yol": lambda: S(gok("safak"), tepeler(560, "#3a3f62", "#2b2f50"), f'<rect x="0" y="520" width="{W}" height="380" fill="#5f6a3a"/>',
    yol_sahnesi(600, 470), turbe(600, 470, .35, "#1d2442")),
"yolculuk": lambda: S(gok("gece"), yildizlar(90, 31, 560), hilal(980, 160, 60, gokrenk="#0e1e3f"), kum_tepeleri(640),
    deve(320, 730, .9), deve(600, 720, .9), deve(880, 710, .9), insan(140, 740, 150, "#1b1430", "#1b1430")),
}

def uret(cikti_dir):
    d = json.load(open("sozluk.json", encoding="utf-8"))
    for x in d:
        govde = SAHNE[x["slug"]]()
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{defs()}{govde}</svg>'
        open(f"{cikti_dir}/{x['slug']}.svg", "w").write(svg)
    return d

if __name__ == "__main__":
    d = uret(sys.argv[1] if len(sys.argv) > 1 else "img")
    print("ok", len(d))
