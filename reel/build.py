"""Steps 3-5: scenes + animation + captions + sound -> index.html and assets/mix.wav."""
import json, random
import numpy as np, soundfile as sf
from art import *
from script import LINES

T = json.load(open("timings.json"))
# --- refine caption word times with the transcriber's real word starts when the counts line up
try:
    WW = json.load(open("whisper_words.json"))
    for L in T:
        got = [w for w in WW if L["start"] - 0.15 <= w["s"] <= L["end"] - 0.05]
        if len(got) == len(L["words"]):
            for cw, ww in zip(L["words"], got):
                cw["t"] = max(L["start"], ww["s"])
except FileNotFoundError:
    pass

def wt(i, word):
    """Time of the first caption word in line i that starts with `word`."""
    for w in T[i]["words"]:
        if w["w"].lower().strip(".,!?:").startswith(word.lower().strip(".,!?:")):
            return w["t"]
    raise KeyError((i, word))

TOTAL = round(T[-1]["end"] + 1.0, 2)
FADE = 0.35
starts = [0.0] + [L["start"] - 0.2 for L in T[1:]]
ends = [s + FADE for s in starts[1:]] + [TOTAL]

A = []   # GSAP lines
def ft(sel, frm, to, t, d, ease="power2.out", extra=""):
    A.append(f'tl.fromTo("{sel}", {{{frm}}}, {{{to}, duration:{d}, ease:"{ease}"{extra}}}, {t:.3f});')
def to(sel, to_, t, d, ease="power2.out", extra=""):
    A.append(f'tl.to("{sel}", {{{to_}, duration:{d}, ease:"{ease}"{extra}}}, {t:.3f});')

def breathe(pid, t0, t1):
    n = max(1, int((t1 - t0) / 1.6))
    A.append(f'tl.to("#{pid}b", {{scaleY:1.014, transformOrigin:"50% 100%", duration:0.8, yoyo:true, repeat:{2*n-1}, ease:"sine.inOut"}}, {t0:.3f});')

def blink(pid, *ts):
    for t in ts:
        A.append(f'tl.to("#{pid}eyes", {{scaleY:0.1, transformOrigin:"50% 50%", duration:0.07, yoyo:true, repeat:1}}, {t:.3f});')

def lipsync(pid, i, from_word):
    ws = T[i]["words"]; k = [w["w"] for w in ws].index(next(w["w"] for w in ws if w["w"].startswith(from_word)))
    for j in range(k, len(ws)):
        t0 = ws[j]["t"]; t1 = ws[j + 1]["t"] if j + 1 < len(ws) else T[i]["end"]
        A.append(f'tl.set("#{pid}mo", {{opacity:1}}, {t0:.3f}); tl.set("#{pid}mo", {{opacity:0}}, {t0 + (t1-t0)*0.6:.3f});')

def flash(t, color="#fff", op=0.8, d=0.18):
    A.append(f'tl.fromTo("#flash", {{opacity:{op}, backgroundColor:"{color}"}}, {{opacity:0, duration:{d}, ease:"none", immediateRender:false}}, {t:.3f});')

def shake(scene, t, amp=18):
    A.append(f'tl.to("#{scene}", {{x:{amp}, duration:0.04, yoyo:true, repeat:5, ease:"none"}}, {t:.3f}); tl.set("#{scene}", {{x:0}}, {t+0.25:.3f});')

def svg(body):
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{body}</svg>'

def wrap(gid, inner):
    return f'<g id="{gid}">{inner}</g>'

SFX = []  # (kind, time)
scenes = []

# ---------------- S1  hook: the mountain drops into his hands
i = 0; s0, s1 = starts[i], ends[i]
b = sky("k1", [(0, "#0b0a2a"), (.55, "#2a1b4f"), (1, "#5a2a4a")]) + stars(1, 70)
b += glow(540, 760, 460, "moonglow") + '<circle cx="540" cy="760" r="170" fill="#fff1c9"/>'
b += '<circle cx="480" cy="720" r="30" fill="#efe0b0"/><circle cx="600" cy="800" r="20" fill="#efe0b0"/>'
b += ground(1480, "#1d1630", INK)
b += wrap("s1mtw", mountain("s1mt", 540, 700, .62, herbs=18, underside=True))
b += hanuman("s1h", 540, 1490, .78, gada=False)
b += wrap("s1herbw", herb_icon("s1herb", 540, 520, .7))
scenes.append(b)
tp = wt(0, "pahaad")
ft("#s1herbw", "opacity:0, scale:0, transformOrigin:'50% 50%'", "opacity:1, scale:1", wt(0, "booti"), .35, "back.out(2)")
to("#s1herbw", "opacity:0, y:-200", tp - .5, .3)
ft("#s1haL", "rotation:0, transformOrigin:'100% 0%'", "rotation:160", tp - .45, .4, "back.out(1.2)")
ft("#s1haR", "rotation:0, transformOrigin:'0% 0%'", "rotation:-160", tp - .45, .4, "back.out(1.2)")
ft("#s1mtw", "y:-1300", "y:0", tp - .2, .35, "power3.in")
ft("#s1hb", "scaleY:1, transformOrigin:'50% 100%'", "scaleY:0.95", tp + .15, .12, "power1.out", ", yoyo:true, repeat:1")
flash(tp + .15); shake("sc1", tp + .15); SFX += [("chime", wt(0, "booti")), ("boom", tp + .15)]
blink("s1h", 1.4, tp + 1.2)

# ---------------- S2  Lanka: the arrow, Lakshman falls
i = 1; s0, s1 = starts[i], ends[i]
b = sky("k2", [(0, "#2a0a1a"), (.5, "#8a1f2a"), (1, "#f07a3a")])
b += glow(540, 1130, 380, "fireglow") + '<circle cx="540" cy="1130" r="190" fill="#e8452a" opacity=".85"/>'
b += lanka_skyline(1300) + ground(1450, "#2a120e", INK)
b += lakshman("s2l", 300, 1470, .7)
b += wrap("s2aw", arrow("s2a", 150, 1050, 1))
scenes.append(b)
tb, tbe = wt(1, "baan"), wt(1, "behosh")
ft("#s2aw", "x:-900, opacity:1", "x:0", tb - .12, .14, "none")
flash(tb + .02, "#ff3b2a", .55); SFX += [("zing", tb - .14), ("hit", tb + .02)]
ft("#s2lb", "rotation:0, transformOrigin:'50% 100%'", "rotation:84", tbe, .55, "power2.in")
to("#s2aw", "opacity:0", tbe, .2)
ft("#s2leyes", "opacity:1", "opacity:0", tbe + .1, .05, "none")
ft("#s2lshut", "opacity:0", "opacity:1", tbe + .1, .05, "none")
SFX.append(("thud", tbe + .55)); shake("sc2", tbe + .55, 10)
breathe("s2l", s0, tbe); blink("s2l", s0 + 1.0)

# ---------------- S3  camp: Sushen names the herb
i = 2; s0, s1 = starts[i], ends[i]
b = sky("k3", [(0, "#0a1230"), (1, "#24345e")]) + stars(3, 50, 900)
b += ground(1450, "#22301f", INK) + glow(540, 1400, 260, "fireglow")
b += '<g id="s3fire">' + "".join(f'<path d="M{540+dx},1440 Q{520+dx},{1360-h} {540+dx},{1300-h} Q{560+dx},{1360-h} {540+dx},1440 Z" fill="{c}"/>'
                               for dx, h, c in [(-30, 0, "#ff7a1a"), (30, 10, "#ff7a1a"), (0, 50, "#ffc23a")]) + '</g>'
b += sushen("s3s", 280, 1470, .74)
b += hanuman("s3h", 810, 1470, .72, mood="determined", flip=True)
b += wrap("s3herbw", herb_icon("s3herb", 450, 560, .85))
scenes.append(b)
ts = wt(2, "Sanjeevni")
ft("#s3herbw", "opacity:0, scale:0, transformOrigin:'50% 50%'", "opacity:1, scale:1", ts, .4, "back.out(2.2)")
A.append(f'tl.to("#s3fire", {{scaleY:1.12, transformOrigin:"50% 100%", duration:0.18, yoyo:true, repeat:{int((s1-s0)/0.18)}, ease:"sine.inOut"}}, {s0:.3f});')
lipsync("s3s", 2, "Suraj"); SFX.append(("chime", ts))
breathe("s3s", s0, s1); breathe("s3h", s0, s1); blink("s3h", s0 + 1.1, s0 + 3.2); blink("s3s", s0 + 2.0)

# ---------------- S4  the leap to the Himalaya
i = 3; s0, s1 = starts[i], ends[i]
b = sky("k4", [(0, "#2d5ea8"), (.6, "#8fbde9"), (1, "#e6f2ff")])
b += wrap("s4cl", cloud("c1", 200, 420, 1.1) + cloud("c2", 860, 300, .8) + cloud("c3", 700, 760, 1.2, .8))
b += wrap("s4pk", peaks(1650, "#7f99c4", "#f4f8ff", 4, 5, 500, 900) + peaks(1800, "#5a76a8", "#e8f0ff", 9, 4, 350, 600))
b += wrap("s4lines", "".join(f'<path d="M{x},{y} L{x-260},{y+150}" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".7"/>' for x, y in [(700, 700), (820, 860), (600, 980), (900, 1060)]))
b += wrap("s4hw", hanuman("s4h", 540, 1060, .6, rot=62, arms=(160, 0)))
scenes.append(b)
tj = wt(3, "chhalaang")
ft("#s4pk", "y:500", "y:0", s0, s1 - s0, "power1.out")
ft("#s4cl", "x:0, y:0", "x:-300, y:250", s0, s1 - s0, "none")
ft("#s4hw", "x:-900, y:700", "x:0, y:0", tj - .25, .7, "power3.out")
to("#s4hw", "x:-110, y:-40", tj + .45, s1 - tj - .45, "sine.inOut")
ft("#s4lines", "opacity:0, x:200, y:-120", "opacity:1, x:-300, y:180", tj, .5, "none", ", repeat:3")
SFX.append(("whoosh_big", tj - .2))

# ---------------- S5  a thousand glowing herbs
i = 4; s0, s1 = starts[i], ends[i]
b = sky("k5", [(0, "#101a40"), (1, "#3a3f78")]) + stars(5, 40, 700)
b += mountain("s5m", 620, 1600, 1.6, herbs=90, seed=11)
b += '<path d="M0,1500 L380,1500 L420,1600 L0,1600 Z" fill="#3a2a22" stroke="#2b1408" stroke-width="6"/>'
b += hanuman("s5h", 210, 1500, .6, mood="think")
b += wrap("s5q", "".join(f'<text x="{x}" y="{y}" font-family="Yatra One" font-size="{fs}" fill="#ffd27a" stroke="#2b1408" stroke-width="5" paint-order="stroke">?</text>' for x, y, fs in [(300, 640, 130), (380, 560, 90), (230, 560, 80)]))
scenes.append(b)
th, tk = wt(4, "hazaaron"), wt(4, "Kaun")
A.append(f'tl.fromTo("#s5mherbs .herb", {{scale:0, transformOrigin:"50% 50%"}}, {{scale:1, duration:0.3, ease:"back.out(3)", stagger:{{each:0.012, from:"random"}}}}, {th - .1:.3f});')
A.append(f'tl.to("#s5mherbs .herb", {{opacity:0.45, duration:0.4, yoyo:true, repeat:5, ease:"sine.inOut", stagger:{{each:0.02, from:"random"}}}}, {th + .9:.3f});')
ft("#s5q", "opacity:0, y:40", "opacity:1, y:0", tk, .3, "back.out(2)")
SFX += [("sparkle", th), ("chime", tk)]
breathe("s5h", s0, s1); blink("s5h", s0 + .8, tk + .6)

# ---------------- S6  he lifts the whole mountain
i = 5; s0, s1 = starts[i], ends[i]
b = sky("k6", [(0, "#1b1d4a"), (.6, "#4a3a7a"), (1, "#c86a5a")]) + stars(6, 30, 600)
b += ground(1470, "#2c2438", INK)
b += wrap("s6mw", mountain("s6m", 540, 1470, .95, herbs=30, underside=True, seed=5))
b += hanuman("s6h", 540, 1500, .78, gada=False)
b += wrap("s6dust", "".join(f'<circle cx="{540+dx}" cy="{1470+dy}" r="{r}" fill="#b79a7a" opacity=".8"/>' for dx, dy, r in [(-300, -10, 40), (-200, 10, 30), (220, 0, 44), (320, -20, 30), (-80, 20, 26), (90, 15, 34)]))
scenes.append(b)
tu = wt(5, "utha")
ft("#s6haL", "rotation:0, transformOrigin:'100% 0%'", "rotation:160", tu - .2, .4, "back.out(1.3)")
ft("#s6haR", "rotation:0, transformOrigin:'0% 0%'", "rotation:-160", tu - .2, .4, "back.out(1.3)")
ft("#s6mw", "y:0", "y:-760", tu - .1, .55, "back.out(1.1)")
ft("#s6dust", "opacity:0, scale:.6, transformOrigin:'50% 100%'", "opacity:1, scale:1.4", tu, .4)
to("#s6dust", "opacity:0, y:-80", tu + .4, .6)
flash(tu + .1); shake("sc6", tu + .1, 24); to("#t5", "opacity:0, y:-60", tu - .15, .25); SFX += [("rumble", tu - .15), ("boom", tu + .1)]
breathe("s6h", s0, s1); blink("s6h", s0 + .7, wt(5, "muskuraaye") + .3)

# ---------------- S7  dawn: back in time, Lakshman wakes
i = 6; s0, s1 = starts[i], ends[i]
b = sky("k7", [(0, "#2a3a7a"), (.55, "#f08a5a"), (1, "#ffd27a")])
b += wrap("s7sun", glow(540, 1260, 420, "sunglow") + '<circle cx="540" cy="1260" r="150" fill="#fff0b0"/>')
b += ground(1430, "#4a5a2a", INK)
b += ''.join(f'<rect x="{x}" y="1230" width="22" height="210" fill="#6a3c1c" stroke="#2b1408" stroke-width="5"/>' for x in (110, 640))
b += '<rect x="90" y="1210" width="600" height="40" rx="10" fill="#a0662c" stroke="#2b1408" stroke-width="6"/><ellipse cx="390" cy="1208" rx="300" ry="22" fill="#3f7d34" stroke="#2b1408" stroke-width="5"/>'
b += lakshman("s7l", 150, 1200, .5, bow=False, eyes_shut=True)
b += wrap("s7spark", "".join(f'<path d="M{x},{y-22} L{x+6},{y-6} L{x+22},{y} L{x+6},{y+6} L{x},{y+22} L{x-6},{y+6} L{x-22},{y} L{x-6},{y-6} Z" fill="#fff6c0"/>' for x, y in [(60, 760), (260, 700), (230, 900), (40, 980), (300, 1000)]))
b += hanuman("s7h", 830, 1440, .62, arms=(0, -160), gada=False)
b += mountain("s7m", 960, 805, .3, herbs=8, underside=True, seed=2)
scenes.append(b)
tkh = wt(6, "khul")
ft("#s7sun", "y:260", "y:0", s0, s1 - s0, "sine.out")
ft("#s7lb", "rotation:88, transformOrigin:'50% 100%'", "rotation:0", tkh + .35, .8, "power2.out")
ft("#s7leyes", "opacity:0", "opacity:1", tkh, .05, "none")
ft("#s7lshut", "opacity:1", "opacity:0", tkh, .05, "none")
ft("#s7spark", "opacity:0, scale:0, transformOrigin:'50% 50%'", "opacity:1, scale:1", tkh + .3, .4, "back.out(3)")
to("#s7spark", "opacity:0", tkh + 1.3, .5)
SFX.append(("chime", tkh)); breathe("s7h", s0, s1); blink("s7h", s0 + 1.0, tkh + .9)

# ---------------- S8  moral: Jai Bajrangbali
i = 7; s0, s1 = starts[i], ends[i]
b = sky("k8", [(0, "#7a1a3a"), (.45, "#ff7a2a"), (1, "#ffcf6a")])
b += wrap("s8rays", "".join(f'<path d="M540,860 L{540+1400*np.cos(np.radians(a)):.0f},{860+1400*np.sin(np.radians(a)):.0f} L{540+1400*np.cos(np.radians(a+7)):.0f},{860+1400*np.sin(np.radians(a+7)):.0f} Z" fill="#fff3c0" opacity=".18"/>' for a in range(0, 360, 20)))
b += glow(540, 860, 520, "sunglow")
b += ground(1480, "#6a2a1a", INK)
b += hanuman("s8h", 540, 1500, .8, mood="smile")
scenes.append(b)
tjb = wt(7, "Bajrangbali")
A.append(f'tl.to("#s8rays", {{rotation:40, svgOrigin:"540 860", duration:{s1 - s0:.2f}, ease:"none"}}, {s0:.3f});')
flash(tjb, "#fff3c0", .7, .3); SFX += [("boom", tjb), ("chime", tjb + .05)]
breathe("s8h", s0, s1); blink("s8h", s0 + 1.2, tjb + .8)

# ---------------- scene transitions + camera push
for k in range(len(scenes)):
    s0, s1 = starts[k], ends[k]
    if k:
        ft(f"#sc{k+1}", "opacity:0", "opacity:1", s0, FADE, "none")
        SFX.append(("whoosh", s0))
    ft(f"#cam{k+1}", "scale:1", "scale:1.06", s0, s1 - s0, "none")

# ---------------- titles (top) and captions (word by word, chunks of <=4)
titles, caps = [], []
title_at = {0: wt(0, "pahaad") + .2, 4: wt(4, "Kaun"), 7: wt(7, "Bajrangbali")}
for k, L in enumerate(T):
    t0 = title_at.get(k, starts[k] + .25)
    titles.append(f'<div id="t{k}" class="title clip" data-start="{max(0, t0-.05):.3f}" data-duration="{ends[k]-t0+.05:.3f}">{L["title"]}</div>')
    pop = "scale:0.4" if k == 7 else "y:-40"
    ft(f"#t{k}", f"opacity:0, {pop}", "opacity:1, y:0, scale:1", t0, .45, "back.out(2)")
    if k < 7:
        to(f"#t{k}", "opacity:0", ends[k] - FADE - .1, .2)
    ws = L["words"]; chunks = [ws[j:j + 4] for j in range(0, len(ws), 4)]
    if len(chunks) > 1 and len(chunks[-1]) == 1:
        last = chunks.pop(); chunks[-1] = chunks[-1] + last
    for c, ch in enumerate(chunks):
        c0 = ch[0]["t"] - .05
        c1 = chunks[c + 1][0]["t"] - .05 if c + 1 < len(chunks) else (T[k + 1]["start"] - .1 if k + 1 < len(T) else TOTAL)
        spans = []
        for w in ch:
            n = len(caps) * 100 + len(spans)
            gold = "gold" if w["w"].lower().strip(".,!?:") == L["key"].lower().strip(".,!?:") else ""
            spans.append(f'<span id="w{k}_{c}_{len(spans)}" class="{gold}">{w["w"]}</span>')
            ft(f"#w{k}_{c}_{len(spans)-1}", "opacity:0, y:24, scale:.8", "opacity:1, y:0, scale:1", w["t"], .14, "back.out(2)")
        caps.append(f'<div id="cap{k}_{c}" class="cap clip" data-start="{c0:.3f}" data-duration="{c1-c0:.3f}">{" ".join(spans)}</div>')

scene_html = "".join(
    f'<div id="sc{k+1}" class="scene clip" data-start="{starts[k]:.3f}" data-duration="{ends[k]-starts[k]:.3f}"><div id="cam{k+1}" class="cam">{svg(sc)}</div></div>'
    for k, sc in enumerate(scenes))

HTML = f"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face {{ font-family:"Yatra One"; src:url(assets/fonts/yatra-one-latin-400-normal.woff2) format("woff2"); }}
@font-face {{ font-family:"Poppins"; font-weight:800; src:url(assets/fonts/poppins-latin-800-normal.woff2) format("woff2"); }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; }}
.scene {{ position:absolute; inset:0; }}
.cam {{ position:absolute; inset:0; transform-origin:50% 55%; }}
.title {{ position:absolute; top:150px; left:0; width:100%; text-align:center; font-family:"Yatra One"; font-size:118px; color:#ffd27a;
         -webkit-text-stroke:6px #2b1408; paint-order:stroke fill; text-shadow:0 8px 30px rgba(0,0,0,.6); letter-spacing:2px; }}
#t7 {{ font-size:104px; color:#fff3c0; }}
.cap {{ position:absolute; top:1290px; left:60px; width:960px; text-align:center; font-family:"Poppins"; font-weight:800; font-size:74px; line-height:1.15;
       color:#fff; -webkit-text-stroke:10px #1a0d05; paint-order:stroke fill; }}
.cap span {{ display:inline-block; margin:0 8px; }}
.gold {{ color:#ffc93a; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; pointer-events:none; }}
</style></head>
<body>
{SHARED_DEFS}
<div id="root" data-composition-id="root" data-width="{W}" data-height="{H}" data-duration="{TOTAL}">
{scene_html}
{"".join(titles)}
{"".join(caps)}
<div id="flash" class="clip" data-start="0" data-duration="{TOTAL}"></div>
<audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1"></audio>
</div>
<script src="assets/gsap.min.js"></script>
<script>
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + a for a in A)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["root"] = tl;
</script>
</body></html>"""
open("index.html", "w").write(HTML)

# ---------------- sound: voice + drone + synthesized effects
voice, sr = sf.read("assets/voice_raw.wav", dtype="float32")
N = int(TOTAL * sr); t = np.arange(N) / sr
mix = np.zeros(N, dtype=np.float32); mix[:len(voice)] += voice[:N]
lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.2 * t)
drone = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(110, 1), (164.81, .6), (220, .5), (329.6, .15)]) * lfo
env = np.minimum(1, t / 1.5) * np.minimum(1, (TOTAL - t) / 2)
mix += (0.045 * drone * env).astype(np.float32)
rng = np.random.default_rng(1)

def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / sr); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

def sfx(kind):
    if kind in ("whoosh", "whoosh_big"):
        d = .45 if kind == "whoosh" else .8; n = int(d * sr); x = band(rng.standard_normal(n), 400, 3500)
        e = np.sin(np.pi * np.arange(n) / n) ** 2; return x / np.abs(x).max() * e * (.12 if kind == "whoosh" else .25)
    if kind in ("boom", "thud", "hit"):
        d = {"boom": 1.1, "thud": .5, "hit": .35}[kind]; n = int(d * sr); tt = np.arange(n) / sr
        f0 = {"boom": 70, "thud": 90, "hit": 160}[kind]
        x = np.sin(2 * np.pi * (f0 * tt - 12 * tt ** 2)) * np.exp(-tt * (4 if kind == "boom" else 9))
        x += .4 * band(rng.standard_normal(n), 30, 400) / 3 * np.exp(-tt * 12)
        return x * {"boom": .55, "thud": .35, "hit": .35}[kind]
    if kind == "rumble":
        n = int(.9 * sr); x = band(rng.standard_normal(n), 25, 160); x /= np.abs(x).max()
        return x * np.sin(np.pi * np.arange(n) / n) * .35
    if kind == "zing":
        n = int(.3 * sr); tt = np.arange(n) / sr; f = 2600 - 6000 * tt
        return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 6) * .12
    if kind in ("chime", "sparkle"):
        n = int(1.6 * sr); tt = np.arange(n) / sr; x = np.zeros(n)
        notes = [(880, 0), (1320, 0), (1760, 0)] if kind == "chime" else [(1568, 0), (2093, .08), (2637, .16), (3136, .24)]
        for f, dl in notes:
            k = int(dl * sr); x[k:] += np.sin(2 * np.pi * f * tt[:n - k]) * np.exp(-tt[:n - k] * 3.5)
        return x * (.07 if kind == "chime" else .05)
    raise ValueError(kind)

for kind, at in SFX:
    x = sfx(kind).astype(np.float32); k = int(max(0, at) * sr); e = min(N, k + len(x))
    mix[k:e] += x[:e - k]
mix = mix / np.abs(mix).max() * 0.92
sf.write("assets/mix.wav", mix, sr)
print(f"index.html written: {len(scenes)} scenes, {len(A)} tweens, {len(caps)} caption chunks, total {TOTAL}s; mix.wav {len(SFX)} sfx")
