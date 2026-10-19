# Yaşayan Sözlük — minyatür üslubunda sahne kütüphanesi (1200x900 SVG)
import math, random

W, H = 1200, 900
P = dict(lac1="#0b1a33", lac2="#17325e", lac3="#24508a", tur="#1f8a7a", tur2="#3fb3a0", gold="#e2c27d",
         gold2="#c9a24a", ivory="#f4ead5", rose="#c8323f", rose2="#e2566a", leaf="#2e7d5b", leaf2="#4aa36f",
         earth="#7a4e2e", sand="#d8b27a", dome="#3aa58e", flame="#ffb347", flame2="#ffd97a", night="#08122a")

def f(x): return f"{x:.1f}"

# ------------------------------------------------------------------ zemin
def defs():
    return f'''<defs>
<linearGradient id="gGece" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['night']}"/><stop offset=".6" stop-color="{P['lac2']}"/><stop offset="1" stop-color="{P['lac3']}"/></linearGradient>
<linearGradient id="gSafak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14254a"/><stop offset=".55" stop-color="#3a4f86"/><stop offset=".85" stop-color="#d98c6a"/><stop offset="1" stop-color="#f2c27a"/></linearGradient>
<linearGradient id="gGun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a6fa8"/><stop offset=".7" stop-color="#7fb8d8"/><stop offset="1" stop-color="#f1dfb0"/></linearGradient>
<linearGradient id="gCol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2b55"/><stop offset=".6" stop-color="#7a4f6a"/><stop offset="1" stop-color="#e6a35a"/></linearGradient>
<radialGradient id="gIsik" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff2c4" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd97a" stop-opacity=".45"/><stop offset="1" stop-color="#ffd97a" stop-opacity="0"/></radialGradient>
<radialGradient id="gAlev" cx="50%" cy="70%" r="60%"><stop offset="0" stop-color="#fff8d6"/><stop offset=".4" stop-color="{P['flame2']}"/><stop offset="1" stop-color="{P['flame']}"/></radialGradient>
<linearGradient id="gEtek" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9d2c2"/><stop offset=".5" stop-color="#fffaf0"/><stop offset="1" stop-color="#cfc6b3"/></linearGradient>
<linearGradient id="gKubbe" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a8a74"/><stop offset=".5" stop-color="#5fd0b6"/><stop offset="1" stop-color="#2a8a74"/></linearGradient>
<linearGradient id="gSu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8fc0"/><stop offset="1" stop-color="#173f6e"/></linearGradient>
<linearGradient id="gToprak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6a3e"/><stop offset="1" stop-color="#4e2f1a"/></linearGradient>
<linearGradient id="gAltin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6e2a8"/><stop offset=".5" stop-color="{P['gold']}"/><stop offset="1" stop-color="{P['gold2']}"/></linearGradient>
<linearGradient id="gGul" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['rose2']}"/><stop offset="1" stop-color="#8e1f2c"/></linearGradient>
<filter id="fParilti" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="fYumusak" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2"/></filter>
</defs>'''

def gok(tur="gece"):
    g = {"gece": "gGece", "safak": "gSafak", "gun": "gGun", "col": "gCol"}[tur]
    return f'<rect width="{W}" height="{H}" fill="url(#{g})"/>'

def yildizlar(n=70, seed=1, ymax=520):
    r = random.Random(seed); out = []
    for _ in range(n):
        x, y, s = r.uniform(0, W), r.uniform(0, ymax), r.uniform(.8, 2.6)
        o = r.uniform(.35, 1)
        if s > 2.2:
            out.append(yildiz8(x, y, s * 3, P['gold'], o))
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(s)}" fill="#fff6dc" opacity="{o:.2f}"/>')
    return "".join(out)

def yildiz8(cx, cy, r, renk, o=1):
    pts = []
    for i in range(16):
        a = math.pi / 8 * i - math.pi / 2; rr = r if i % 2 == 0 else r * .42
        pts.append(f"{f(cx + rr * math.cos(a))},{f(cy + rr * math.sin(a))}")
    return f'<polygon points="{" ".join(pts)}" fill="{renk}" opacity="{o:.2f}"/>'

def hilal(cx, cy, r, renk=None, gokrenk="#0f2245"):
    renk = renk or P['gold']
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*1.8}" fill="url(#gIsik)" opacity=".5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{renk}"/>'
            f'<circle cx="{cx + r*.38}" cy="{cy - r*.18}" r="{r*.86}" fill="{gokrenk}"/>')

def gunes(cx, cy, r, isinlar=True):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r*2.6}" fill="url(#gIsik)"/>'
    if isinlar:
        for i in range(24):
            a = 2 * math.pi * i / 24; L = r * (1.55 if i % 2 else 1.85)
            x1, y1 = cx + r * 1.12 * math.cos(a), cy + r * 1.12 * math.sin(a)
            x2, y2 = cx + L * math.cos(a), cy + L * math.sin(a)
            s += f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{P["gold"]}" stroke-width="{f(r*.09)}" stroke-linecap="round" opacity=".85"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gAltin)"/><circle cx="{cx}" cy="{cy}" r="{r*.72}" fill="none" stroke="#fff3cf" stroke-width="3" opacity=".7"/>'
    return s

def tepeler(y=720, renk1="#132a4f", renk2="#0d1f3d", seed=3):
    r = random.Random(seed)
    def tepe(yb, amp, renk):
        pts = [f"0,{H}"]; x = 0
        while x <= W:
            pts.append(f"{x},{f(yb - amp * (0.5 + 0.5 * math.sin(x / 140 + r.uniform(0, 1))) )}"); x += 60
        pts.append(f"{W},{H}")
        return f'<polygon points="{" ".join(pts)}" fill="{renk}"/>'
    return tepe(y - 40, 50, renk1) + tepe(y, 30, renk2)

def zemin(y=780, renk="#0d1f3d"):
    return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{renk}"/>'

# ------------------------------------------------------------------ mimari
def turbe(cx, yb, s=1.0, renk="#0e1c36", kubbe=True):
    """Mevlânâ Türbesi silueti: gövde, kasnak, yeşil dilimli konik kubbe, minare."""
    w = 260 * s; h = 120 * s
    o = f'<g>'
    o += f'<rect x="{f(cx - w/2)}" y="{f(yb - h)}" width="{f(w)}" height="{f(h)}" fill="{renk}"/>'
    for i in range(5):
        ax = cx - w/2 + w * (i + .5) / 5
        o += f'<path d="M{f(ax-14*s)} {f(yb)} v{-50*s} a{14*s} {14*s} 0 0 1 {28*s} 0 v{50*s}z" fill="#1d3358"/>'
    o += f'<path d="M{f(cx-w/2-20*s)} {f(yb-h)} q{w/2+20*s} {-60*s} {w+40*s} 0z" fill="{renk}"/>'
    o += f'<circle cx="{f(cx-w*.33)}" cy="{f(yb-h)}" r="{f(38*s)}" fill="{renk}"/><circle cx="{f(cx+w*.33)}" cy="{f(yb-h)}" r="{f(34*s)}" fill="{renk}"/>'
    dx = cx; dy = yb - h - 40 * s; dw = 70 * s
    o += f'<rect x="{f(dx-dw/2)}" y="{f(dy-70*s)}" width="{f(dw)}" height="{f(110*s)}" fill="{renk}"/>'
    if kubbe:
        tip = dy - 230 * s
        o += f'<path d="M{f(dx-dw/2-6*s)} {f(dy-70*s)} Q{f(dx-dw/2)} {f(tip+60*s)} {f(dx)} {f(tip)} Q{f(dx+dw/2)} {f(tip+60*s)} {f(dx+dw/2+6*s)} {f(dy-70*s)}Z" fill="url(#gKubbe)"/>'
        for k in range(-3, 4):
            o += f'<path d="M{f(dx + k*9*s)} {f(dy-70*s)} Q{f(dx + k*5*s)} {f(tip+70*s)} {f(dx)} {f(tip)}" stroke="#1e6e5c" stroke-width="{f(2*s)}" fill="none"/>'
        o += f'<line x1="{f(dx)}" y1="{f(tip)}" x2="{f(dx)}" y2="{f(tip-30*s)}" stroke="{P["gold"]}" stroke-width="{f(3*s)}"/>'
        o += f'<circle cx="{f(dx)}" cy="{f(tip-34*s)}" r="{f(6*s)}" fill="{P["gold"]}"/>'
    mx = cx + w/2 + 40 * s
    o += f'<rect x="{f(mx-9*s)}" y="{f(yb-300*s)}" width="{f(18*s)}" height="{f(300*s)}" fill="{renk}"/>'
    o += f'<rect x="{f(mx-15*s)}" y="{f(yb-230*s)}" width="{f(30*s)}" height="{f(8*s)}" fill="{renk}"/>'
    o += f'<path d="M{f(mx-10*s)} {f(yb-300*s)} L{f(mx)} {f(yb-360*s)} L{f(mx+10*s)} {f(yb-300*s)}z" fill="{renk}"/>'
    o += '</g>'
    return o

def sehir(yb=800, renk="#0c1a33", s=1.0):
    o = ""
    for x, r in [(90, 46), (230, 60), (980, 52), (1110, 40)]:
        o += f'<circle cx="{x}" cy="{yb-70*s}" r="{r*s}" fill="{renk}"/><rect x="{x-r*s}" y="{yb-70*s}" width="{2*r*s}" height="{70*s}" fill="{renk}"/>'
    for x in [160, 1045]:
        o += f'<rect x="{x}" y="{yb-230*s}" width="{12*s}" height="{230*s}" fill="{renk}"/><path d="M{x} {yb-230*s} l{6*s} {-40*s} l{6*s} {40*s}z" fill="{renk}"/>'
    o += f'<rect x="0" y="{yb-40}" width="{W}" height="{H-yb+40}" fill="{renk}"/>'
    return o

def kemer(renk=P['gold'], x=260, y=110, w=680, h=760):
    """Mihrap kemeri çerçevesi."""
    r = w / 2
    return (f'<path d="M{x} {y+h} V{y+r} Q{x} {y} {x+r} {y-40} Q{x+w} {y} {x+w} {y+r} V{y+h}" fill="none" stroke="{renk}" stroke-width="6" opacity=".85"/>'
            f'<path d="M{x+18} {y+h} V{y+r+6} Q{x+18} {y+22} {x+r} {y-14} Q{x+w-18} {y+22} {x+w-18} {y+r+6} V{y+h}" fill="none" stroke="{P["tur"]}" stroke-width="3" opacity=".8"/>')

# ------------------------------------------------------------------ figürler
def semazen(cx, yb, h=300, ters=False, renk_etek="url(#gEtek)", donme=0, eller="sema"):
    """Semâ eden derviş: sikke, tennure, açık kollar. eller='sema' | 'selam'"""
    s = h / 300
    sg = -1 if ters else 1
    o = f'<g transform="translate({f(cx)} {f(yb)}) rotate({donme}) scale({f(s*sg)} {f(s)})">'
    # tennure (çan etek) — kıvrımlı alt kenar
    o += '<path d="M-28 -150 C-60 -110 -120 -40 -150 -6 Q-120 6 -96 -2 Q-70 10 -44 0 Q-20 12 4 0 Q30 12 54 0 Q80 10 104 -2 Q130 6 156 -10 C120 -44 62 -112 30 -150Z" fill="' + renk_etek + '"/>'
    for k in [-100, -60, -20, 22, 64, 106]:
        o += f'<path d="M{k*0.2:.1f} -146 Q{k*0.55:.1f} -80 {k:.1f} -4" stroke="#bdb39e" stroke-width="2" fill="none" opacity=".7"/>'
    o += '<path d="M-150 -6 Q-120 6 -96 -2 Q-70 10 -44 0 Q-20 12 4 0 Q30 12 54 0 Q80 10 104 -2 Q130 6 156 -10" stroke="#a89c84" stroke-width="2.5" fill="none"/>'
    # gövde (destegül)
    o += '<path d="M-30 -150 Q-34 -200 -22 -232 L22 -232 Q34 -200 30 -150Z" fill="#f7f1e4"/>'
    o += '<path d="M-30 -152 Q0 -142 30 -152" stroke="#2b2118" stroke-width="5" fill="none"/>'
    if eller == "sema":
        o += '<path d="M-20 -224 Q-60 -258 -92 -300" stroke="#f7f1e4" stroke-width="16" stroke-linecap="round" fill="none"/>'
        o += '<path d="M20 -222 Q62 -214 104 -236" stroke="#f7f1e4" stroke-width="16" stroke-linecap="round" fill="none"/>'
        o += '<ellipse cx="-97" cy="-307" rx="8" ry="11" fill="#e8c7a0" transform="rotate(-30 -97 -307)"/>'
        o += '<ellipse cx="112" cy="-238" rx="10" ry="7" fill="#e8c7a0"/>'
    else:  # selam: kollar göğüste çapraz
        o += '<path d="M-24 -222 Q-6 -200 18 -214" stroke="#efe7d6" stroke-width="15" stroke-linecap="round" fill="none"/>'
        o += '<path d="M24 -222 Q6 -200 -18 -214" stroke="#e6dcc8" stroke-width="15" stroke-linecap="round" fill="none"/>'
    # baş (hafif yana eğik) ve sikke
    o += '<g transform="rotate(14 0 -246)"><circle cx="0" cy="-252" r="17" fill="#e8c7a0"/>'
    o += '<path d="M-14 -262 Q-18 -318 -8 -336 Q0 -344 8 -336 Q18 -318 14 -262Z" fill="#a9825a"/>'
    o += '<path d="M-14 -266 Q0 -262 14 -266" stroke="#7a5a3a" stroke-width="2" fill="none"/></g>'
    o += '</g>'
    return o

def golge_elips(cx, yb, rx, o=.35):
    return f'<ellipse cx="{cx}" cy="{yb+4}" rx="{rx}" ry="{rx*.12}" fill="#000" opacity="{o}"/>'

def insan(cx, yb, h=150, renk="#e9d9b6", bas="#e8c7a0"):
    s = h / 150
    return (f'<g transform="translate({cx} {yb}) scale({s})"><path d="M-26 0 Q-30 -70 -18 -96 L18 -96 Q30 -70 26 0Z" fill="{renk}"/>'
            f'<circle cx="0" cy="-114" r="17" fill="{bas}"/></g>')

# ------------------------------------------------------------------ nesneler
def ney(x, y, uzunluk=700, aci=-20, kalinlik=26):
    L, k = uzunluk, kalinlik
    o = f'<g transform="translate({x} {y}) rotate({aci})">'
    o += f'<rect x="0" y="{-k/2}" width="{L}" height="{k}" rx="{k/2}" fill="#c9a06a"/>'
    o += f'<rect x="0" y="{-k/2}" width="{L}" height="{k*.35}" rx="{k/4}" fill="#e3c393" opacity=".8"/>'
    for i in range(1, 9):
        bx = L * i / 9
        o += f'<rect x="{f(bx-3)}" y="{-k/2-1}" width="6" height="{k+2}" fill="#8a6a40"/>'
    for i, hx in enumerate([.42, .5, .58, .66, .74, .82]):
        o += f'<ellipse cx="{f(L*hx)}" cy="0" rx="{k*.18}" ry="{k*.22}" fill="#3a2414"/>'
    o += f'<path d="M{L-4} {-k/2-3} h{k*1.1} l{k*.4} {k*.25} v{k*.5} l{-k*.4} {k*.25} h{-k*1.1}z" fill="url(#gAltin)"/>'
    o += f'<rect x="-4" y="{-k/2-2}" width="{k*.6}" height="{k+4}" rx="3" fill="url(#gAltin)"/>'
    o += '</g>'
    return o

def ses_dalgalari(cx, cy, n=4, renk=None, aci=0):
    renk = renk or P['gold']; o = f'<g transform="rotate({aci} {cx} {cy})">'
    for i in range(n):
        r = 40 + i * 38
        o += f'<path d="M{cx+r*math.cos(-.6):.1f} {cy+r*math.sin(-.6):.1f} A{r} {r} 0 0 1 {cx+r*math.cos(.6):.1f} {cy+r*math.sin(.6):.1f}" stroke="{renk}" stroke-width="5" fill="none" stroke-linecap="round" opacity="{.9-i*.18:.2f}"/>'
    return o + '</g>'

def gul(cx, cy, r=60, renk="url(#gGul)", sap=True, yaprak=True):
    o = ""
    if sap:
        o += f'<path d="M{cx} {cy+r*.6} Q{cx-r*.3} {cy+r*2.2} {cx+r*.1} {cy+r*3.6}" stroke="{P["leaf"]}" stroke-width="{r*.12:.1f}" fill="none"/>'
    if yaprak:
        o += f'<path d="M{cx-r*.18} {cy+r*1.8} q{-r*1.1} {-r*.2} {-r*1.3} {-r*.9} q{r*.9} {-r*.1} {r*1.3} {r*.9}z" fill="{P["leaf2"]}"/>'
        o += f'<path d="M{cx-r*.05} {cy+r*2.6} q{r*1.1} {-r*.1} {r*1.3} {-r*.9} q{-r*.95} {0} {-r*1.3} {r*.9}z" fill="{P["leaf"]}"/>'
    # dış taç yapraklar
    for i in range(6):
        a = i * 60 + 15
        o += f'<ellipse cx="{cx}" cy="{cy - r*.45}" rx="{r*.55}" ry="{r*.62}" fill="{renk}" transform="rotate({a} {cx} {cy})" stroke="#7d1824" stroke-width="2"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r*.72}" fill="#b52a38"/>'
    for i in range(5):
        a = i * 72
        o += f'<ellipse cx="{cx}" cy="{cy - r*.28}" rx="{r*.38}" ry="{r*.42}" fill="{P["rose2"]}" opacity=".85" transform="rotate({a} {cx} {cy})" stroke="#8e1f2c" stroke-width="1.5"/>'
    o += f'<path d="M{cx-r*.25} {cy} q{r*.25} {-r*.4} {r*.5} 0 q{-r*.25} {r*.25} {-r*.5} 0z" fill="#8e1f2c"/>'
    o += f'<path d="M{cx} {cy-r*.15} a{r*.15} {r*.15} 0 1 1 -{r*.01} 0" stroke="#7d1824" stroke-width="2" fill="none"/>'
    return o

def lale(cx, yb, h=140, renk=P['rose']):
    return (f'<path d="M{cx} {yb} Q{cx-6} {yb-h*.5} {cx} {yb-h*.72}" stroke="{P["leaf"]}" stroke-width="5" fill="none"/>'
            f'<path d="M{cx-4} {yb-h*.2} q{-30} {-20} {-26} {-70} q{20} {30} {26} {60}z" fill="{P["leaf2"]}"/>'
            f'<path d="M{cx-18} {yb-h*.7} Q{cx-24} {yb-h*.95} {cx-12} {yb-h*1.08} L{cx-6} {yb-h*.92} L{cx} {yb-h*1.12} L{cx+6} {yb-h*.92} L{cx+12} {yb-h*1.08} Q{cx+24} {yb-h*.95} {cx+18} {yb-h*.7} Q{cx} {yb-h*.62} {cx-18} {yb-h*.7}z" fill="{renk}" stroke="#7d1824" stroke-width="1.5"/>')

def kandil(cx, ust, alt, r=70, zincir=True):
    o = f'<circle cx="{cx}" cy="{alt}" r="{r*3.2}" fill="url(#gIsik)"/>'
    if zincir:
        for dx in (-r*.8, 0, r*.8):
            o += f'<line x1="{cx}" y1="{ust}" x2="{cx+dx}" y2="{alt-r*.55}" stroke="{P["gold"]}" stroke-width="3" stroke-dasharray="6 4"/>'
    o += f'<path d="M{cx-r} {alt-r*.5} Q{cx-r*1.05} {alt+r*.7} {cx} {alt+r*.85} Q{cx+r*1.05} {alt+r*.7} {cx+r} {alt-r*.5}Z" fill="#7fc8b8" fill-opacity=".55" stroke="{P["gold"]}" stroke-width="3"/>'
    o += f'<ellipse cx="{cx}" cy="{alt-r*.5}" rx="{r}" ry="{r*.18}" fill="#bfe8de" fill-opacity=".6" stroke="{P["gold"]}" stroke-width="3"/>'
    for i in range(-2, 3):
        o += f'<path d="M{cx+i*r*.35:.1f} {alt-r*.4:.1f} q{i*4} {r*.6:.1f} 0 {r*1.1:.1f}" stroke="{P["gold"]}" stroke-width="1.5" fill="none" opacity=".7"/>'
    o += alev(cx, alt + r * .25, r * .55)
    o += f'<path d="M{cx-12} {alt+r*.85} h24 l-6 {r*.35} h-12z" fill="url(#gAltin)"/>'
    return o

def alev(cx, yb, h=120):
    w = h * .45
    return (f'<ellipse cx="{cx}" cy="{yb-h*.4}" rx="{w*1.8}" ry="{h*.9}" fill="url(#gIsik)"/>'
            f'<path d="M{cx} {yb-h} C{cx+w*.2} {yb-h*.7} {cx+w} {yb-h*.45} {cx+w*.7} {yb-h*.12} Q{cx} {yb+h*.08} {cx-w*.7} {yb-h*.12} C{cx-w} {yb-h*.45} {cx-w*.15} {yb-h*.6} {cx} {yb-h}Z" fill="url(#gAlev)"/>'
            f'<path d="M{cx} {yb-h*.55} C{cx+w*.35} {yb-h*.35} {cx+w*.35} {yb-h*.1} {cx} {yb-h*.05} C{cx-w*.35} {yb-h*.1} {cx-w*.3} {yb-h*.3} {cx} {yb-h*.55}Z" fill="#fffbe8"/>')

def mum(cx, yb, h=220, w=56):
    return (f'<rect x="{cx-w/2}" y="{yb-h}" width="{w}" height="{h}" rx="6" fill="#f2e6cc"/>'
            f'<rect x="{cx-w/2}" y="{yb-h}" width="{w*.35}" height="{h}" rx="6" fill="#fffaf0" opacity=".7"/>'
            f'<path d="M{cx-w/2} {yb-h+6} q{w*.25} 18 {w*.3} 4 q{w*.2} 26 {w*.4} 2 q{w*.15} 14 {w*.3} -2" fill="#fffaf0"/>'
            f'<line x1="{cx}" y1="{yb-h}" x2="{cx}" y2="{yb-h-12}" stroke="#3a2a1a" stroke-width="3"/>'
            f'<ellipse cx="{cx}" cy="{yb}" rx="{w*1.3}" ry="{w*.28}" fill="url(#gAltin)"/>'
            + alev(cx, yb - h - 8, 90))

def pervane(cx, cy, s=1.0, aci=0, renk="#efe2c2"):
    return (f'<g transform="translate({cx} {cy}) rotate({aci}) scale({s})">'
            f'<path d="M0 0 C-40 -50 -80 -30 -70 0 C-62 22 -24 14 0 0Z" fill="{renk}" opacity=".95"/>'
            f'<path d="M0 0 C40 -50 80 -30 70 0 C62 22 24 14 0 0Z" fill="{renk}" opacity=".95"/>'
            f'<path d="M0 2 C-30 30 -46 46 -28 52 C-14 56 -6 28 0 2Z" fill="#d9c79e"/>'
            f'<path d="M0 2 C30 30 46 46 28 52 C14 56 6 28 0 2Z" fill="#d9c79e"/>'
            f'<circle cx="-42" cy="-12" r="7" fill="none" stroke="#b8a37a" stroke-width="2"/><circle cx="42" cy="-12" r="7" fill="none" stroke="#b8a37a" stroke-width="2"/>'
            f'<ellipse cx="0" cy="8" rx="5" ry="24" fill="#6e5b3e"/>'
            f'<path d="M-2 -14 q-10 -18 -20 -22 M2 -14 q10 -18 20 -22" stroke="#6e5b3e" stroke-width="2" fill="none"/></g>')

def kitap(cx, cy, w=420, h=230, isik=True):
    o = ""
    if isik: o += f'<ellipse cx="{cx}" cy="{cy-h*.6}" rx="{w*.75}" ry="{h*1.2}" fill="url(#gIsik)" opacity=".8"/>'
    o += f'<path d="M{cx} {cy+12} Q{cx-w*.25} {cy-10} {cx-w/2-14} {cy+18} L{cx-w/2-14} {cy-h+24} Q{cx-w*.25} {cy-h-4} {cx} {cy-h+16}Z" fill="#7a3b2a"/>'
    o += f'<path d="M{cx} {cy+12} Q{cx+w*.25} {cy-10} {cx+w/2+14} {cy+18} L{cx+w/2+14} {cy-h+24} Q{cx+w*.25} {cy-h-4} {cx} {cy-h+16}Z" fill="#7a3b2a"/>'
    o += f'<path d="M{cx} {cy} Q{cx-w*.25} {cy-22} {cx-w/2} {cy+4} L{cx-w/2} {cy-h+10} Q{cx-w*.25} {cy-h-16} {cx} {cy-h}Z" fill="{P["ivory"]}"/>'
    o += f'<path d="M{cx} {cy} Q{cx+w*.25} {cy-22} {cx+w/2} {cy+4} L{cx+w/2} {cy-h+10} Q{cx+w*.25} {cy-h-16} {cx} {cy-h}Z" fill="#efe3c8"/>'
    for sg in (-1, 1):
        for i in range(7):
            yy = cy - h + 40 + i * (h - 60) / 7
            x1, x2 = cx + sg * 24, cx + sg * (w / 2 - 26)
            o += f'<path d="M{f(x1)} {f(yy)} Q{f((x1+x2)/2)} {f(yy-8 + (i%2)*6)} {f(x2)} {f(yy+2)}" stroke="#5a4630" stroke-width="2.4" fill="none" opacity=".65"/>'
    o += f'<rect x="{cx-w/2+20}" y="{cy-h+18}" width="{w/2-40}" height="16" fill="{P["tur"]}" opacity=".5"/>'
    o += f'<rect x="{cx+20}" y="{cy-h+18}" width="{w/2-40}" height="16" fill="{P["tur"]}" opacity=".5"/>'
    return o

def terazi(cx, yb, h=460, egim=0):
    o = f'<rect x="{cx-70}" y="{yb-26}" width="140" height="26" rx="6" fill="url(#gAltin)"/>'
    o += f'<rect x="{cx-9}" y="{yb-h}" width="18" height="{h-24}" fill="url(#gAltin)"/>'
    o += yildiz8(cx, yb - h - 18, 26, P['gold'])
    by = yb - h + 40
    o += f'<g transform="rotate({egim} {cx} {by})"><rect x="{cx-240}" y="{by-6}" width="480" height="12" rx="6" fill="url(#gAltin)"/>'
    for sx in (-230, 230):
        px = cx + sx; py = by + 190
        o += f'<line x1="{px}" y1="{by}" x2="{px-70}" y2="{py}" stroke="{P["gold"]}" stroke-width="3"/><line x1="{px}" y1="{by}" x2="{px+70}" y2="{py}" stroke="{P["gold"]}" stroke-width="3"/>'
        o += f'<path d="M{px-86} {py} Q{px} {py+70} {px+86} {py}Z" fill="url(#gAltin)"/>'
    o += '</g>'
    return o

def kalp_suslu(cx, cy, s=1.0):
    o = f'<g transform="translate({cx} {cy}) scale({s})">'
    o += '<circle cx="0" cy="0" r="290" fill="url(#gIsik)" opacity=".7"/>'
    yol = "M0 120 C-60 70 -200 10 -200 -90 C-200 -170 -110 -200 -50 -160 C-20 -140 -6 -110 0 -90 C6 -110 20 -140 50 -160 C110 -200 200 -170 200 -90 C200 10 60 70 0 120Z"
    o += f'<path d="{yol}" fill="url(#gGul)" stroke="{P["gold"]}" stroke-width="8"/>'
    o += f'<path d="{yol}" transform="scale(.78) translate(0 -14)" fill="none" stroke="{P["gold"]}" stroke-width="3"/>'
    # rumi kıvrımları
    for sg in (-1, 1):
        o += f'<path d="M0 60 C{sg*40} 20 {sg*120} 0 {sg*120} -70 C{sg*120} -110 {sg*80} -120 {sg*64} -96 C{sg*52} -78 {sg*70} -62 {sg*86} -74" stroke="{P["gold"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M{sg*86} -74 q{sg*14} 6 {sg*10} 20 q{-sg*14} 0 {-sg*10} -20z" fill="{P["gold"]}"/>'
    o += yildiz8(0, -40, 34, P['ivory'])
    o += '</g>'
    return o

def damla(cx, cy, r=40, renk="#7fd0f0"):
    return f'<path d="M{cx} {cy-r*1.9} C{cx+r*.4} {cy-r} {cx+r} {cy-r*.4} {cx+r} {cy+r*.1} A{r} {r} 0 1 1 {cx-r} {cy+r*.1} C{cx-r} {cy-r*.4} {cx-r*.4} {cy-r} {cx} {cy-r*1.9}Z" fill="{renk}" stroke="#e8f8ff" stroke-width="3"/><ellipse cx="{cx-r*.35}" cy="{cy}" rx="{r*.18}" ry="{r*.32}" fill="#fff" opacity=".7"/>'

def dalgalar(y0, n=6, renk="#2b6fa3", amp=14, dalga=90, kalin=6, o=.9):
    out = ""
    for j in range(n):
        y = y0 + j * 26; d = f"M0 {y}"
        x = 0
        while x < W + dalga:
            d += f" q{dalga/4} {-amp} {dalga/2} 0 t{dalga/2} 0"; x += dalga
        out += f'<path d="{d}" stroke="{renk}" stroke-width="{kalin}" fill="none" opacity="{o - j*.08:.2f}" stroke-linecap="round"/>'
    return out

def deniz(y0=560):
    return f'<rect x="0" y="{y0}" width="{W}" height="{H-y0}" fill="url(#gSu)"/>' + dalgalar(y0 + 30, 9, "#6fb6dd", 10, 110, 4, .7)

def dag(cx, yb, w, h, renk="#2a3f6a", kar=True):
    o = f'<path d="M{cx-w/2} {yb} L{cx-w*.08} {yb-h} L{cx+w*.05} {yb-h*.9} L{cx+w/2} {yb}Z" fill="{renk}"/>'
    o += f'<path d="M{cx} {yb} L{cx-w*.08} {yb-h} L{cx+w*.05} {yb-h*.9} L{cx+w/2} {yb}Z" fill="#000" opacity=".18"/>'
    if kar: o += f'<path d="M{cx-w*.08} {yb-h} L{cx-w*.17} {yb-h*.78} L{cx-w*.1} {yb-h*.82} L{cx-w*.04} {yb-h*.74} L{cx+w*.02} {yb-h*.83} L{cx+w*.1} {yb-h*.76} L{cx+w*.05} {yb-h*.9}Z" fill="#eef2f7"/>'
    return o

def servi(cx, yb, h=420, w=70, renk="#14432f"):
    return (f'<path d="M{cx} {yb-h} C{cx+w*.6} {yb-h*.6} {cx+w*.55} {yb-h*.15} {cx+w*.2} {yb-10} L{cx-w*.2} {yb-10} C{cx-w*.55} {yb-h*.15} {cx-w*.6} {yb-h*.6} {cx} {yb-h}Z" fill="{renk}"/>'
            f'<path d="M{cx} {yb-h} C{cx+w*.6} {yb-h*.6} {cx+w*.55} {yb-h*.15} {cx+w*.2} {yb-10} L{cx} {yb-10}Z" fill="#000" opacity=".2"/>'
            f'<rect x="{cx-5}" y="{yb-14}" width="10" height="14" fill="#4a3020"/>')

def agac(cx, yb, h=430, r=190, meyve=0, renk="#1f5f40", seed=2, mrenk="#c8323f"):
    rnd = random.Random(seed)
    o = f'<path d="M{cx-22} {yb} Q{cx-14} {yb-h*.4} {cx-8} {yb-h+r*.6} L{cx+8} {yb-h+r*.6} Q{cx+14} {yb-h*.4} {cx+26} {yb}Z" fill="#5b3a22"/>'
    o += f'<path d="M{cx} {yb-h*.55} Q{cx-60} {yb-h*.7} {cx-110} {yb-h*.78}" stroke="#5b3a22" stroke-width="14" fill="none"/>'
    o += f'<path d="M{cx} {yb-h*.6} Q{cx+70} {yb-h*.72} {cx+120} {yb-h*.8}" stroke="#5b3a22" stroke-width="12" fill="none"/>'
    for i in range(14):
        a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0, r * .75)
        x = cx + d * math.cos(a) * 1.15; y = yb - h + r * .25 + d * math.sin(a) * .8
        rr = rnd.uniform(r * .3, r * .5)
        shade = rnd.choice([renk, "#2a7a52", "#185238"])
        o += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rr)}" fill="{shade}"/>'
    for i in range(meyve):
        a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(r * .2, r * .85)
        x = cx + d * math.cos(a) * 1.1; y = yb - h + r * .3 + d * math.sin(a) * .7
        o += nar(x, y, 20, mrenk)
    return o

def nar(x, y, r=20, renk="#c8323f"):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{renk}" stroke="#7d1824" stroke-width="2"/>'
            f'<path d="M{f(x-6)} {f(y-r+2)} l3 -9 l3 6 l3 -6 l3 9z" fill="#7d1824"/>'
            f'<circle cx="{f(x-r*.35)}" cy="{f(y-r*.3)}" r="{r*.22}" fill="#fff" opacity=".35"/>')

def bugday(cx, yb, h=300, egim=40, renk="#e2b85c"):
    o = f'<path d="M{cx} {yb} Q{cx+4} {yb-h*.6} {cx+egim} {yb-h}" stroke="#b08a3c" stroke-width="5" fill="none"/>'
    tx, ty = cx + egim, yb - h
    for i in range(8):
        t = i / 8
        px = tx - egim * .35 * t + 0; py = ty + 60 * t
        for sg in (-1, 1):
            o += f'<ellipse cx="{f(px+sg*9 + egim*.4*t)}" cy="{f(py+ 30*t)}" rx="8" ry="15" fill="{renk}" transform="rotate({sg*25 + egim*.6} {f(px+sg*9 + egim*.4*t)} {f(py+30*t)})"/>'
    o += f'<ellipse cx="{f(tx)}" cy="{f(ty-6)}" rx="7" ry="14" fill="{renk}" transform="rotate({egim*.5} {f(tx)} {f(ty-6)})"/>'
    return o

def kus(cx, cy, s=1.0, ters=False, renk="#f7f3ea", dal=False):
    sg = -1 if ters else 1
    o = f'<g transform="translate({cx} {cy}) scale({s*sg} {s})">'
    o += f'<path d="M-90 10 C-60 -10 -20 -6 10 6 C40 -4 70 -14 92 -30 C84 -4 70 10 44 18 C30 30 -10 34 -40 26 C-60 30 -80 24 -90 10Z" fill="{renk}"/>'
    o += f'<path d="M-20 4 C-10 -60 30 -110 90 -120 C60 -80 50 -40 30 4Z" fill="{renk}" stroke="#d8d0bd" stroke-width="2"/>'
    o += f'<path d="M-30 6 C-40 -40 -30 -80 0 -100 C-6 -60 0 -30 10 6Z" fill="#e6dfcf"/>'
    o += f'<circle cx="74" cy="-16" r="3.5" fill="#222"/><path d="M90 -26 l16 4 l-14 6z" fill="#e2a64a"/>'
    if dal:
        o += f'<path d="M104 -18 q30 -6 52 10" stroke="#4a6a2a" stroke-width="3" fill="none"/>'
        for k in range(4):
            o += f'<ellipse cx="{112+k*12}" cy="{-18+k*3 - (k%2)*10}" rx="9" ry="4" fill="#6f9a3a" transform="rotate({-30+(k%2)*60} {112+k*12} {-18+k*3-(k%2)*10})"/>'
    return o + '</g>'

def kus_suru(x, y, n=5, s=1.0, renk="#f4ead5", seed=4):
    r = random.Random(seed); o = ""
    for i in range(n):
        px, py, k = x + r.uniform(-120, 120), y + r.uniform(-60, 60), s * r.uniform(.6, 1.1)
        o += f'<path d="M{f(px-22*k)} {f(py)} Q{f(px-10*k)} {f(py-14*k)} {f(px)} {f(py)} Q{f(px+10*k)} {f(py-14*k)} {f(px+22*k)} {f(py)}" stroke="{renk}" stroke-width="{f(3.5*k)}" fill="none" stroke-linecap="round"/>'
    return o

def kum_saati(cx, cy, h=420, w=240, ust_kum=.35):
    o = f'<rect x="{cx-w/2-20}" y="{cy-h/2-24}" width="{w+40}" height="24" rx="6" fill="url(#gAltin)"/>'
    o += f'<rect x="{cx-w/2-20}" y="{cy+h/2}" width="{w+40}" height="24" rx="6" fill="url(#gAltin)"/>'
    for sx in (-w/2-6, w/2-6):
        o += f'<rect x="{cx+sx}" y="{cy-h/2}" width="12" height="{h}" fill="#8a6a3a"/>'
    cam = f"M{cx-w/2+20} {cy-h/2} Q{cx-w/2+10} {cy-30} {cx-10} {cy} Q{cx-w/2+10} {cy+30} {cx-w/2+20} {cy+h/2} L{cx+w/2-20} {cy+h/2} Q{cx+w/2-10} {cy+30} {cx+10} {cy} Q{cx+w/2-10} {cy-30} {cx+w/2-20} {cy-h/2}Z"
    o += f'<path d="{cam}" fill="#cfe9f0" fill-opacity=".22" stroke="#e8f4f7" stroke-width="3"/>'
    uy = cy - h/2 + h * (.5 - ust_kum) * .9
    o += f'<path d="M{cx-w/2+40} {uy} L{cx+w/2-40} {uy} Q{cx+40} {cy-40} {cx} {cy-6} Q{cx-40} {cy-40} {cx-w/2+40} {uy}Z" fill="{P["sand"]}"/>'
    o += f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+h/2-60}" stroke="{P["sand"]}" stroke-width="3"/>'
    o += f'<path d="M{cx-w/2+26} {cy+h/2} Q{cx} {cy+h/2-110} {cx+w/2-26} {cy+h/2}Z" fill="{P["sand"]}"/>'
    return o

def anahtar(cx, cy, s=1.0, aci=-30):
    return (f'<g transform="translate({cx} {cy}) rotate({aci}) scale({s})">'
            f'<circle cx="0" cy="0" r="70" fill="none" stroke="url(#gAltin)" stroke-width="18"/>'
            + yildiz8(0, 0, 42, P['gold']) +
            f'<rect x="64" y="-12" width="260" height="24" rx="10" fill="url(#gAltin)"/>'
            f'<rect x="250" y="10" width="20" height="50" fill="url(#gAltin)"/><rect x="290" y="10" width="20" height="36" fill="url(#gAltin)"/></g>')

def kapi(cx, yb, w=320, h=520):
    r = w / 2
    o = f'<path d="M{cx-w/2-30} {yb} V{yb-h+r} Q{cx-w/2-30} {yb-h-40} {cx} {yb-h-70} Q{cx+w/2+30} {yb-h-40} {cx+w/2+30} {yb-h+r} V{yb}Z" fill="#1a2c4f" stroke="{P["gold"]}" stroke-width="5"/>'
    o += f'<path d="M{cx-w/2} {yb} V{yb-h+r} Q{cx-w/2} {yb-h-10} {cx} {yb-h-36} Q{cx+w/2} {yb-h-10} {cx+w/2} {yb-h+r} V{yb}Z" fill="#6b3d22"/>'
    o += f'<line x1="{cx}" y1="{yb}" x2="{cx}" y2="{yb-h-30}" stroke="#3e2213" stroke-width="5"/>'
    for i in range(4):
        y = yb - 80 - i * 110
        for sg in (-1, 1):
            o += yildiz8(cx + sg * w * .25, y, 26, P['gold'], .9)
    o += f'<circle cx="{cx-20}" cy="{yb-h*.45}" r="10" fill="url(#gAltin)"/><circle cx="{cx+20}" cy="{yb-h*.45}" r="10" fill="url(#gAltin)"/>'
    return o

def ayna(cx, cy, rx=200, ry=260, ic=""):
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx+34}" ry="{ry+34}" fill="url(#gAltin)"/>'
    for i in range(16):
        a = 2 * math.pi * i / 16
        o += f'<circle cx="{f(cx+(rx+34)*math.cos(a))}" cy="{f(cy+(ry+34)*math.sin(a))}" r="14" fill="{P["tur"]}" stroke="{P["gold"]}" stroke-width="3"/>'
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#9fc4d6"/>'
    o += f'<clipPath id="cAyna"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath><g clip-path="url(#cAyna)">{ic}'
    o += f'<path d="M{cx-rx} {cy-ry*.2} L{cx-rx*.2} {cy-ry} L{cx+rx*.05} {cy-ry} L{cx-rx} {cy+ry*.1}Z" fill="#fff" opacity=".25"/></g>'
    return o

def istiridye(cx, cy, s=1.0):
    o = f'<g transform="translate({cx} {cy}) scale({s})">'
    o += '<path d="M-230 40 Q-240 -40 -170 -60 L170 -60 Q240 -40 230 40 Q0 120 -230 40Z" fill="#c9b8a0"/>'
    o += '<path d="M-220 -40 Q-200 -230 0 -260 Q200 -230 220 -40 Q0 -90 -220 -40Z" fill="#e6d6bd"/>'
    for i in range(-5, 6):
        o += f'<path d="M0 -60 Q{i*20} -160 {i*40} -245" stroke="#b9a582" stroke-width="4" fill="none"/>'
    o += '<path d="M-200 -30 Q0 -80 200 -30 Q0 40 -200 -30Z" fill="#f0c9cf"/>'
    o += '<circle cx="0" cy="-30" r="200" fill="url(#gIsik)" opacity=".6"/>'
    o += '<circle cx="0" cy="-30" r="46" fill="#fbf7ef"/><circle cx="-14" cy="-44" r="14" fill="#fff"/>'
    return o + '</g>'

def ibrik(cx, yb, s=1.0):
    o = f'<g transform="translate({cx} {yb}) scale({s})">'
    o += '<path d="M-60 0 Q-110 -80 -70 -160 Q-50 -190 -40 -230 L40 -230 Q50 -190 70 -160 Q110 -80 60 0Z" fill="url(#gAltin)" stroke="#9a7a3a" stroke-width="3"/>'
    o += '<path d="M-40 -230 Q0 -250 40 -230 L36 -260 Q0 -275 -36 -260Z" fill="#c9a24a"/>'
    o += '<path d="M70 -150 Q160 -170 190 -250 L176 -256 Q150 -190 70 -180" fill="url(#gAltin)" stroke="#9a7a3a" stroke-width="3"/>'
    o += '<path d="M-72 -140 Q-150 -150 -120 -60 Q-110 -40 -78 -50" fill="none" stroke="#c9a24a" stroke-width="10"/>'
    o += '<path d="M-56 -110 Q0 -90 56 -110" stroke="#1f8a7a" stroke-width="10" fill="none"/>'
    o += yildiz8(0, -70, 22, P['tur'])
    return o + '</g>'

def kase(cx, yb, w=260, renk="url(#gAltin)"):
    return (f'<path d="M{cx-w/2} {yb-80} Q{cx} {yb+40} {cx+w/2} {yb-80}Z" fill="{renk}" stroke="#9a7a3a" stroke-width="3"/>'
            f'<ellipse cx="{cx}" cy="{yb-80}" rx="{w/2}" ry="16" fill="#2f6f9a"/>'
            f'<rect x="{cx-40}" y="{yb-12}" width="80" height="14" rx="5" fill="#9a7a3a"/>')

def deve(cx, yb, s=1.0, renk="#1b1430"):
    o = f'<g transform="translate({cx} {yb}) scale({s})" fill="{renk}">'
    o += '<path d="M-110 -110 Q-120 -150 -90 -170 Q-60 -230 -20 -170 Q0 -200 30 -165 Q60 -140 70 -120 L90 -150 Q100 -210 130 -220 L160 -214 L160 -200 L140 -198 Q130 -170 120 -110 Q110 -90 90 -84 L80 0 L66 0 L62 -76 L-40 -80 L-56 0 L-70 0 L-74 -84 Q-100 -86 -110 -110Z"/>'
    o += '<path d="M-90 -104 L-106 0 L-92 0 L-78 -90Z"/><path d="M40 -80 L50 0 L64 0 L56 -82Z"/>'
    o += '<path d="M-60 -200 l10 -14 l70 0 l10 14z" fill="#6a2a2a"/>'
    return o + '</g>'

def fener(cx, cy, s=1.0):
    o = f'<g transform="translate({cx} {cy}) scale({s})">'
    o += '<circle cx="0" cy="20" r="240" fill="url(#gIsik)"/>'
    o += '<path d="M-10 -170 q10 -40 20 0" stroke="url(#gAltin)" stroke-width="8" fill="none"/>'
    o += '<path d="M-70 -110 L0 -170 L70 -110Z" fill="url(#gAltin)"/>'
    o += '<path d="M-60 -110 L-70 110 L70 110 L60 -110Z" fill="#ffe7a6" fill-opacity=".55" stroke="url(#gAltin)" stroke-width="8"/>'
    for x in (-24, 24):
        o += f'<line x1="{x}" y1="-110" x2="{x*1.15}" y2="110" stroke="#c9a24a" stroke-width="5"/>'
    o += '<rect x="-80" y="110" width="160" height="24" rx="6" fill="url(#gAltin)"/>'
    o += alev(0, 70, 90)
    return o + '</g>'

def yol_sahnesi(hedef_x=600, ufuk=430):
    o = f'<path d="M420 {H} C520 760 760 700 640 600 C560 540 560 480 {hedef_x} {ufuk} L{hedef_x+12} {ufuk} C620 480 640 540 720 600 C860 710 720 780 820 {H}Z" fill="#c9a26a"/>'
    o += f'<path d="M620 {H} C640 780 760 720 680 600 C620 530 610 480 {hedef_x+6} {ufuk}" stroke="#f4ead5" stroke-width="5" stroke-dasharray="22 18" fill="none" opacity=".7"/>'
    return o

def sazlik(x0, x1, yb, n=24, seed=5, renk="#3f6b3a"):
    r = random.Random(seed); o = ""
    for i in range(n):
        x = x0 + (x1 - x0) * i / n + r.uniform(-8, 8); h = r.uniform(180, 330); b = r.uniform(-30, 30)
        o += f'<path d="M{f(x)} {yb} Q{f(x+b*.3)} {f(yb-h*.6)} {f(x+b)} {f(yb-h)}" stroke="{renk}" stroke-width="{r.uniform(4,7):.1f}" fill="none" stroke-linecap="round"/>'
        if r.random() < .5:
            o += f'<path d="M{f(x+b*.3)} {f(yb-h*.5)} q{r.choice([-1,1])*40} -30 {r.choice([-1,1])*60} -10" stroke="#5c8f4f" stroke-width="4" fill="none"/>'
    return o

def eller_dua(cx, cy, s=1.0, renk="#e8c7a0"):
    o = f'<g transform="translate({cx} {cy}) scale({s})">'
    for sg in (-1, 1):
        o += f'<g transform="scale({sg} 1)"><path d="M10 120 C14 60 16 10 30 -40 C36 -62 44 -86 60 -96 C74 -100 80 -88 76 -70 L66 -10 C86 -40 106 -70 118 -80 C130 -88 140 -78 134 -64 L104 0 C110 30 100 80 90 120Z" fill="{renk}" stroke="#b58e66" stroke-width="3"/>'
        o += '<path d="M14 120 L90 120 L94 170 L10 170Z" fill="#f4ead5"/></g>'
    return o + '</g>'

def insan_halkasi(cx, yb, n=6, w=900):
    o = ""
    renkler = ["#e9d9b6", "#c8a27a", "#9a6b48", "#e2c9a2", "#6e4a32", "#d8b892", "#b98a62"]
    for i in range(n):
        x = cx - w / 2 + w * (i + .5) / n
        o += insan(x, yb, 170 + (i % 2) * 20, renk=["#2a9d8f", "#c8323f", "#e2c27d", "#3a5ea8", "#7a4e9a", "#d97a3a"][i % 6], bas=renkler[i % 7])
        if i < n - 1:
            nx = cx - w / 2 + w * (i + 1.5) / n
            o += f'<path d="M{f(x+24)} {yb-100} Q{f((x+nx)/2)} {yb-70} {f(nx-24)} {yb-100}" stroke="#e8c7a0" stroke-width="12" fill="none" stroke-linecap="round"/>'
    return o

def fidan(cx, yb, s=1.0):
    o = f'<g transform="translate({cx} {yb}) scale({s})">'
    o += '<ellipse cx="0" cy="0" rx="220" ry="46" fill="url(#gToprak)"/>'
    o += '<circle cx="0" cy="-120" r="200" fill="url(#gIsik)" opacity=".8"/>'
    o += '<path d="M0 -10 Q-6 -90 4 -170" stroke="#4aa36f" stroke-width="10" fill="none" stroke-linecap="round"/>'
    o += '<path d="M2 -120 C-50 -150 -110 -130 -120 -90 C-70 -80 -30 -90 2 -120Z" fill="#4aa36f"/>'
    o += '<path d="M4 -160 C50 -200 110 -190 126 -150 C80 -130 40 -136 4 -160Z" fill="#5fbf80"/>'
    return o + '</g>'

def capa(cx, cy, s=1.0):
    o = f'<g transform="translate({cx} {cy}) scale({s})" fill="url(#gAltin)" stroke="#9a7a3a" stroke-width="3">'
    o += '<circle cx="0" cy="-230" r="34" fill="none" stroke="url(#gAltin)" stroke-width="16"/>'
    o += '<rect x="-14" y="-200" width="28" height="360" rx="10"/><rect x="-110" y="-150" width="220" height="24" rx="10"/>'
    o += '<path d="M-200 60 Q-160 200 0 200 Q160 200 200 60 L240 90 L200 0 L170 80 Q140 160 0 160 Q-140 160 -170 80 L-200 0 L-240 90Z"/>'
    return o + '</g>'

def tuy(cx, cy, s=1.0, aci=-30, renk="#f4ead5"):
    o = f'<g transform="translate({cx} {cy}) rotate({aci}) scale({s})">'
    o += f'<path d="M0 -220 C70 -160 80 -40 30 120 L0 200 L-30 120 C-80 -40 -70 -160 0 -220Z" fill="{renk}"/>'
    o += '<path d="M0 -210 L0 230" stroke="#b9ab8e" stroke-width="5"/>'
    for i in range(10):
        y = -170 + i * 30
        o += f'<path d="M0 {y} q{30} {-20} {48 - abs(i-4)*4} {-8}" stroke="#d6cbb2" stroke-width="2" fill="none"/><path d="M0 {y} q{-30} {-20} {-(48 - abs(i-4)*4)} {-8}" stroke="#d6cbb2" stroke-width="2" fill="none"/>'
    return o + '</g>'

def hokka_kalem(cx, yb, s=1.0):
    o = f'<g transform="translate({cx} {yb}) scale({s})">'
    o += '<path d="M-80 0 Q-100 -70 -60 -100 L60 -100 Q100 -70 80 0Z" fill="#1f3a6e" stroke="url(#gAltin)" stroke-width="5"/>'
    o += '<ellipse cx="0" cy="-100" rx="60" ry="12" fill="#0b1426" stroke="url(#gAltin)" stroke-width="4"/>'
    o += '<path d="M-50 -60 Q0 -40 50 -60" stroke="url(#gAltin)" stroke-width="4" fill="none"/>'
    o += '<path d="M20 -96 L190 -380 L204 -372 L36 -88Z" fill="#c9a06a"/><path d="M190 -380 L214 -404 L204 -372Z" fill="#6b4a2a"/>'
    return o + '</g>'

def tomar(cx, cy, w=520, h=330):
    o = f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="{P["ivory"]}"/>'
    for sg in (-1, 1):
        o += f'<rect x="{cx+sg*w/2-18}" y="{cy-h/2-14}" width="36" height="{h+28}" rx="18" fill="#d9c49a" stroke="#9a7a3a" stroke-width="3"/>'
    for i in range(6):
        y = cy - h/2 + 50 + i * 46
        o += f'<path d="M{cx+w/2-60} {y} q-60 -16 -120 0 t-120 0 t-120 0 t-100 6" stroke="#2a2118" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>'
        o += f'<circle cx="{cx+w/2-150 - i*12}" cy="{y-18}" r="3.5" fill="#2a2118"/>'
    o += f'<rect x="{cx-w/2+40}" y="{cy-h/2+12}" width="{w-80}" height="10" fill="{P["tur"]}" opacity=".6"/>'
    return o

def kum_tepeleri(y=700):
    return (f'<path d="M0 {y} Q200 {y-80} 420 {y-20} T860 {y-40} T{W} {y-10} V{H} H0Z" fill="#c8945a"/>'
            f'<path d="M0 {y+60} Q260 {y-10} 560 {y+50} T{W} {y+30} V{H} H0Z" fill="#a8743f"/>')

def nehir():
    return ('<path d="M560 420 C600 470 520 520 560 580 C620 660 460 720 420 900 L820 900 C760 760 760 680 680 600 C620 540 660 470 600 420Z" fill="url(#gSu)"/>'
            '<path d="M585 440 C610 490 540 530 580 590 C630 650 500 730 480 880" stroke="#bfe6f6" stroke-width="5" fill="none" opacity=".6" stroke-dasharray="40 30"/>')

def ruzgar(cx, cy, s=1.0, renk="#e9dcc0"):
    o = f'<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{renk}" stroke-linecap="round" stroke-width="10">'
    o += '<path d="M-260 -60 H80 a60 60 0 1 0 -60 -60"/><path d="M-300 20 H180 a70 70 0 1 1 -70 70"/><path d="M-220 100 H20" opacity=".7"/>'
    return o + '</g>'

def spiral(cx, cy, r=320, tur=3, renk=P['gold'], o=.6, w=4):
    pts = []
    for i in range(400):
        t = i / 400 * tur * 2 * math.pi; rr = r * i / 400
        pts.append(f"{f(cx + rr*math.cos(t))},{f(cy + rr*math.sin(t)*.45)}")
    return f'<polyline points="{" ".join(pts)}" stroke="{renk}" stroke-width="{w}" fill="none" opacity="{o}"/>'

def isik_huzmesi(cx, ust, alt, w1=40, w2=420, o=.35):
    return f'<path d="M{cx-w1/2} {ust} L{cx+w1/2} {ust} L{cx+w2/2} {alt} L{cx-w2/2} {alt}Z" fill="#ffe9a8" opacity="{o}"/>'
