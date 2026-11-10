"""Character + set kit, drawn as SVG strings.
Convention: every character is drawn around its FEET at (0,0), about 900 units tall
(the crown goes higher). Place it with x, y, s. Parts that animate get ids:
  {pid}      outer group (placement)          {pid}b   inner group (breathing / falling / poses)
  {pid}aL    left arm (pivot = shoulder)      {pid}aR  right arm
  {pid}eyes  open eyes (blink = scaleY)       {pid}shut closed eyes (hidden by default)
  {pid}mo    open mouth (lip-sync)            {pid}hd  head
"""
import random

INK = "#2b1408"
H_SKIN, H_SHADE, H_MUZ = "#e8742a", "#c4581a", "#f7cf9f"
RED, RED_D = "#c0262d", "#8e1a20"
GOLD, GOLD_D = "#f2b631", "#b57d0e"
W = 1080; H = 1920

def _o(d, fill, sw=6, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'

def limb(pts, w, color):
    """A thick rounded stroke with an ink outline (draw the ink copy first, a bit wider)."""
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+12}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

def place(pid, x, y, s, inner, flip=False, rot=0):
    sx = -s if flip else s
    return (f'<g id="{pid}" transform="translate({x},{y}) rotate({rot}) scale({sx},{s})">'
            f'<g id="{pid}b">{inner}</g></g>')

# ---------------------------------------------------------------- Hanuman
def _gada(x, y):
    """Mace held at (x,y): shaft goes up to a ribbed gold head."""
    return (limb([(x, y + 120), (x + 40, y - 330)], 22, "#8a4b1c")
            + f'<circle cx="{x+48}" cy="{y-400}" r="78" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<path d="M{x+48+dx},{y-470} Q{x+48+dx*1.6},{y-400} {x+48+dx},{y-330}" fill="none" stroke="{GOLD_D}" stroke-width="6"/>' for dx in (-40, 0, 40))
            + f'<circle cx="{x+48}" cy="{y-485}" r="16" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'
            + f'<rect x="{x+18}" y="{y-322}" width="60" height="20" rx="6" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" transform="rotate(7 {x+48} {y-312})"/>')

def _h_arm(side, gada=False):
    k = -1 if side == "L" else 1
    sh, el, wr = (k * 150, -712), (k * 192, -565), (k * 200, -440)
    o = limb([sh, el], 74, H_SKIN) + limb([el, wr], 62, H_SKIN)
    o += limb([(k * 168, -655), (k * 176, -620)], 30, GOLD)            # armband
    o += limb([(k * 199, -468), (k * 200, -458)], 34, GOLD)            # bracelet
    o += f'<circle cx="{k*201}" cy="{-412}" r="38" fill="{H_SKIN}" stroke="{INK}" stroke-width="6"/>'
    if gada:
        o += _gada(k * 201, -412)
    return o

def hanuman(pid, x, y, s=1.0, arms=(0, 0), gada=True, mood="smile", flip=False, rot=0, tail=True):
    """arms = static rotation in degrees of (left, right) arm about the shoulder.
    Overhead: arms=(160,-160).  mood: smile | think | determined"""
    o = ""
    if tail:
        d = "M70,-440 C230,-420 290,-600 250,-740 C228,-815 150,-820 152,-760 C154,-712 214,-718 214,-752"
        o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="46" stroke-linecap="round"/>'
        o += f'<path d="{d}" fill="none" stroke="{H_SKIN}" stroke-width="34" stroke-linecap="round"/>'
    # legs + feet
    o += limb([(-62, -230), (-66, -40)], 72, H_SKIN) + limb([(62, -230), (66, -40)], 72, H_SKIN)
    o += limb([(-66, -70), (-66, -62)], 80, GOLD) + limb([(66, -70), (66, -62)], 80, GOLD)
    o += _o("M-120,-28 Q-66,-58 -20,-28 L-14,0 L-126,0 Z", H_SKIN) + _o("M120,-28 Q66,-58 20,-28 L14,0 L126,0 Z", H_SKIN)
    # dhoti
    o += _o("M-122,-462 L122,-462 L142,-205 Q70,-170 0,-222 Q-70,-170 -142,-205 Z", RED)
    o += '<path d="M-138,-215 Q-70,-182 0,-232 Q70,-182 138,-215" fill="none" stroke="' + GOLD + '" stroke-width="10"/>'
    o += f'<path d="M0,-450 L-18,-240 M-60,-440 L-80,-230 M60,-440 L80,-230" stroke="{RED_D}" stroke-width="6" fill="none"/>'
    # torso
    o += _o("M-152,-738 Q-182,-640 -124,-560 Q-104,-505 -112,-468 L112,-468 Q104,-505 124,-560 Q182,-640 152,-738 Q0,-778 -152,-738 Z", H_SKIN)
    o += f'<path d="M-98,-640 Q-52,-596 -6,-636 M6,-636 Q52,-596 98,-640 M-40,-560 L-34,-500 M40,-560 L34,-500" fill="none" stroke="{H_SHADE}" stroke-width="7" stroke-linecap="round"/>'
    o += '<path d="M-118,-722 L104,-476" stroke="#fff4d6" stroke-width="7"/>'      # sacred thread
    o += f'<rect x="-122" y="-490" width="244" height="40" rx="12" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
    o += _o("M-22,-458 L16,-458 L30,-330 L-8,-318 Z", GOLD, 5)
    o += f'<path d="M-84,-740 Q0,-640 84,-740" fill="none" stroke="{GOLD}" stroke-width="14"/>'
    o += "".join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{RED}" stroke="{INK}" stroke-width="3"/>' for cx, cy in [(-50, -700), (0, -688), (50, -700)])
    # arms (pivot at shoulders)
    aL, aR = arms
    o += f'<g transform="rotate({aL} -150 -712)"><g id="{pid}aL">{_h_arm("L")}</g></g>'
    o += f'<g transform="rotate({aR} 150 -712)"><g id="{pid}aR">{_h_arm("R", gada)}</g></g>'
    # neck + head
    o += f'<rect x="-44" y="-800" width="88" height="80" fill="{H_SKIN}" stroke="{INK}" stroke-width="6"/>'
    hd = ""
    for k in (-1, 1):
        hd += f'<circle cx="{k*110}" cy="-862" r="34" fill="{H_SKIN}" stroke="{INK}" stroke-width="6"/><circle cx="{k*110}" cy="-862" r="17" fill="{H_MUZ}"/>'
    hd += f'<circle cx="0" cy="-868" r="112" fill="{H_SKIN}" stroke="{INK}" stroke-width="6"/>'
    hd += f'<ellipse cx="0" cy="-806" rx="92" ry="64" fill="{H_MUZ}" stroke="{INK}" stroke-width="6"/>'   # the famous jaw
    # eyes
    if mood == "determined":
        brows = f'<path d="M-72,-922 L-14,-904 M72,-922 L14,-904" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    elif mood == "think":
        brows = f'<path d="M-72,-916 Q-44,-934 -14,-918 M72,-930 Q44,-944 14,-924" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    else:
        brows = f'<path d="M-72,-914 Q-44,-930 -14,-914 M72,-914 Q44,-930 14,-914" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    hd += brows
    hd += (f'<g id="{pid}eyes">'
           f'<ellipse cx="-42" cy="-880" rx="25" ry="19" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="-39" cy="-879" r="11" fill="{INK}"/>'
           f'<ellipse cx="42" cy="-880" rx="25" ry="19" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="39" cy="-879" r="11" fill="{INK}"/></g>')
    hd += f'<ellipse cx="0" cy="-836" rx="17" ry="10" fill="#7a3a1a"/>'
    mouth = {"smile": "M-38,-792 Q0,-764 38,-792", "think": "M-26,-786 Q4,-794 30,-782",
             "determined": "M-30,-786 L30,-786"}[mood]
    hd += f'<path d="{mouth}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    hd += f'<path id="{pid}mo" d="M-30,-794 Q0,-752 30,-794 Z" fill="#7a1a1a" stroke="{INK}" stroke-width="4" opacity="0"/>'
    hd += f'<path d="M-14,-952 L0,-912 L14,-952" fill="none" stroke="{RED}" stroke-width="8" stroke-linecap="round"/>'  # tilak
    # crown
    hd += _o("M-104,-992 Q-150,-1030 -122,-1072 Q-108,-1018 -86,-1004 Z", GOLD, 5) + _o("M104,-992 Q150,-1030 122,-1072 Q108,-1018 86,-1004 Z", GOLD, 5)
    hd += _o("M-88,-990 L-62,-1090 L62,-1090 L88,-990 Z", GOLD)
    hd += _o("M-48,-1088 Q0,-1215 48,-1088 Z", GOLD)
    hd += f'<circle cx="0" cy="-1212" r="11" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'
    hd += f'<rect x="-104" y="-996" width="208" height="44" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
    hd += f'<circle cx="0" cy="-974" r="15" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
    hd += "".join(f'<circle cx="{cx}" cy="-974" r="6" fill="{GOLD_D}"/>' for cx in (-76, -50, 50, 76))
    hd += f'<path d="M-50,-1050 L50,-1050" stroke="{GOLD_D}" stroke-width="6"/><circle cx="0" cy="-1130" r="12" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
    o += f'<g id="{pid}hd">{hd}</g>'
    return place(pid, x, y, s, o, flip, rot)

# ---------------------------------------------------------------- Lakshman
L_SKIN, L_DHOTI, L_SASH = "#f2c49a", "#e4a627", "#2f7d57"

def lakshman(pid, x, y, s=1.0, rot=0, bow=True, eyes_shut=False):
    o = ""
    o += limb([(-50, -220), (-54, -40)], 60, L_SKIN) + limb([(50, -220), (54, -40)], 60, L_SKIN)
    o += _o("M-100,-26 Q-54,-52 -14,-26 L-10,0 L-104,0 Z", L_SKIN) + _o("M100,-26 Q54,-52 14,-26 L10,0 L104,0 Z", L_SKIN)
    o += _o("M-104,-450 L104,-450 L122,-200 Q60,-172 0,-214 Q-60,-172 -122,-200 Z", L_DHOTI)
    o += f'<path d="M-118,-210 Q-60,-180 0,-224 Q60,-180 118,-210" fill="none" stroke="{RED}" stroke-width="9"/>'
    o += _o("M-124,-722 Q-150,-620 -100,-540 Q-90,-490 -96,-456 L96,-456 Q90,-490 100,-540 Q150,-620 124,-722 Q0,-758 -124,-722 Z", L_SKIN)
    o += f'<path d="M-110,-710 L96,-470" stroke="{L_SASH}" stroke-width="26"/>'
    o += f'<rect x="-104" y="-478" width="208" height="36" rx="10" fill="{L_SASH}" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M-70,-724 Q0,-650 70,-724" fill="none" stroke="{GOLD}" stroke-width="12"/>'
    for k in (-1, 1):
        o += limb([(k * 124, -700), (k * 158, -560), (k * 164, -436)], 58, L_SKIN)
        o += limb([(k * 162, -468), (k * 163, -460)], 30, GOLD)
        o += f'<circle cx="{k*165}" cy="-412" r="32" fill="{L_SKIN}" stroke="{INK}" stroke-width="6"/>'
    if bow:
        o += f'<path d="M-175,-700 Q-300,-412 -175,-124" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
        o += f'<path d="M-175,-700 Q-300,-412 -175,-124" fill="none" stroke="#9a5a22" stroke-width="12" stroke-linecap="round"/>'
        o += f'<path d="M-175,-700 L-175,-124" stroke="#f5e6c4" stroke-width="3"/>'
    o += f'<rect x="-36" y="-780" width="72" height="70" fill="{L_SKIN}" stroke="{INK}" stroke-width="6"/>'
    hd = "".join(f'<path d="M{k*80},-880 Q{k*124},-790 {k*112},-660 L{k*64},-672 Q{k*76},-780 {k*52},-860 Z" fill="#1d1410" stroke="{INK}" stroke-width="5"/>' for k in (-1, 1))  # hair locks
    hd += f'<ellipse cx="0" cy="-836" rx="86" ry="96" fill="{L_SKIN}" stroke="{INK}" stroke-width="6"/>'
    hd += f'<path d="M-86,-860 Q-60,-930 0,-918 Q60,-930 86,-860 Q60,-890 0,-886 Q-60,-890 -86,-860 Z" fill="#1d1410"/>'
    hd += f'<path d="M-58,-866 Q-38,-878 -16,-866 M58,-866 Q38,-878 16,-866" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    hd += (f'<g id="{pid}eyes" opacity="{0 if eyes_shut else 1}">'
           f'<path d="M-62,-842 Q-38,-862 -14,-842 Q-38,-830 -62,-842 Z" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="-38" cy="-845" r="9" fill="{INK}"/>'
           f'<path d="M62,-842 Q38,-862 14,-842 Q38,-830 62,-842 Z" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="38" cy="-845" r="9" fill="{INK}"/></g>')
    hd += (f'<g id="{pid}shut" opacity="{1 if eyes_shut else 0}">'
           f'<path d="M-62,-842 Q-38,-830 -14,-842 M62,-842 Q38,-830 14,-842" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></g>')
    hd += f'<path d="M-6,-830 Q-12,-804 4,-800" fill="none" stroke="#b07a52" stroke-width="5"/>'
    hd += f'<path d="M-24,-778 Q0,-764 24,-778" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    hd += f'<path d="M-10,-912 L0,-884 L10,-912" fill="none" stroke="{RED}" stroke-width="6"/>'
    hd += _o("M-74,-918 L-50,-1000 L50,-1000 L74,-918 Z", GOLD) + _o("M-32,-998 Q0,-1080 32,-998 Z", GOLD)
    hd += f'<rect x="-82" y="-930" width="164" height="30" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="-915" r="11" fill="{L_SASH}" stroke="{INK}" stroke-width="3"/>'
    o += f'<g id="{pid}hd">{hd}</g>'
    return place(pid, x, y, s, o, rot=rot)

# ---------------------------------------------------------------- Sushen Vaidya
def sushen(pid, x, y, s=1.0):
    SK, ROBE = "#b9774a", "#f3ede0"
    o = _o("M-118,-690 Q-160,-320 -150,0 L150,0 Q160,-320 118,-690 Q0,-730 -118,-690 Z", ROBE)
    o += _o("M-118,-690 Q-40,-600 60,-300 L120,-330 Q60,-560 118,-690 Q40,-720 -118,-690 Z", "#e2862f", 5)   # saffron shawl
    o += f'<path d="M-40,-640 L-30,-40 M40,-600 L50,-40" stroke="#d8cdb7" stroke-width="6"/>'
    o += limb([(-110, -660), (-150, -520), (-110, -420)], 52, ROBE)                 # left arm holds a pouch
    o += _o("M-150,-450 Q-110,-470 -80,-440 L-90,-360 Q-120,-340 -150,-360 Z", "#8a5a2a", 5)
    o += f'<g id="{pid}aR">' + limb([(110, -660), (178, -790), (196, -910)], 50, ROBE) + \
         f'<circle cx="198" cy="-938" r="28" fill="{SK}" stroke="{INK}" stroke-width="5"/>' + \
         limb([(200, -960), (204, -1006)], 12, SK) + '</g>'
    o += f'<rect x="-34" y="-760" width="68" height="60" fill="{SK}" stroke="{INK}" stroke-width="6"/>'
    hd = f'<ellipse cx="0" cy="-812" rx="84" ry="92" fill="{SK}" stroke="{INK}" stroke-width="6"/>'
    hd += f'<path d="M-84,-830 Q-108,-860 -86,-900 Q-70,-860 -70,-820 Z M84,-830 Q108,-860 86,-900 Q70,-860 70,-820 Z" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    hd += "".join(f'<path d="M-40,{yy} L40,{yy}" stroke="#fff" stroke-width="6" stroke-linecap="round"/>' for yy in (-880, -866, -852))
    hd += f'<circle cx="0" cy="-866" r="7" fill="{RED}"/>'
    hd += f'<path d="M-62,-834 Q-40,-848 -16,-834 M62,-834 Q40,-848 16,-834" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>'
    hd += (f'<g id="{pid}eyes"><ellipse cx="-38" cy="-814" rx="14" ry="11" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="-36" cy="-813" r="6" fill="{INK}"/>'
           f'<ellipse cx="38" cy="-814" rx="14" ry="11" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="36" cy="-813" r="6" fill="{INK}"/></g>')
    hd += f'<path d="M-4,-800 Q-12,-776 6,-772" fill="none" stroke="#7d4c2c" stroke-width="5"/>'
    hd += _o("M-74,-780 Q-90,-700 -40,-620 Q0,-560 40,-620 Q90,-700 74,-780 Q40,-756 0,-762 Q-40,-756 -74,-780 Z", "#ffffff", 5)   # beard
    hd += f'<path d="M-46,-772 Q0,-790 46,-772" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/>'
    hd += f'<ellipse id="{pid}mo" cx="0" cy="-748" rx="18" ry="13" fill="#5a1a14" opacity="0"/>'
    o += f'<g id="{pid}hd">{hd}</g>'
    return place(pid, x, y, s, o)

# ---------------------------------------------------------------- props + sets
def mountain(pid, x, y, s=1.0, herbs=0, underside=False, seed=7):
    """Dronagiri. Base centre at (0,0), ~480 tall, ~640 wide."""
    o = ""
    if underside:
        o += _o("M-320,0 Q-250,70 -170,60 Q-90,120 0,90 Q90,130 170,70 Q260,80 320,0 Z", "#7a5235")
        o += f'<path d="M-200,40 L-160,70 M-40,70 L0,100 M120,60 L160,90" stroke="#4e321f" stroke-width="8"/>'
    o += _o("M-320,0 L-210,-250 L-140,-200 L0,-480 L130,-250 L190,-300 L320,0 Z", "#3f7d4e")
    o += '<path d="M0,-480 L130,-250 L190,-300 L320,0 L60,0 L20,-300 Z" fill="#2f6340"/>'
    o += _o("M-62,-362 L0,-480 L62,-360 L32,-378 L0,-348 L-30,-380 Z", "#eef4f8", 5)
    o += _o("M-235,-195 L-210,-250 L-180,-215 L-200,-205 Z", "#eef4f8", 4)
    r = random.Random(seed)
    for _ in range(14):
        tx, ty = r.randint(-250, 250), r.randint(-160, -20)
        if abs(tx) < 320 - (-ty) * 0.6:
            o += f'<path d="M{tx},{ty-46} L{tx+20},{ty} L{tx-20},{ty} Z" fill="#1f4a2e"/>'
    if herbs:
        o += f'<g id="{pid}herbs">'
        for i in range(herbs):
            hx, hy = r.randint(-260, 260), r.randint(-330, -20)
            if abs(hx) > 300 - (-hy) * 0.62:
                continue
            o += (f'<g class="herb"><circle cx="{hx}" cy="{hy}" r="26" fill="url(#herbglow)"/>'
                  f'<path d="M{hx},{hy+8} Q{hx-12},{hy-6} {hx-2},{hy-16} Q{hx+12},{hy-6} {hx},{hy+8} Z" fill="#d8ff7a" stroke="#4a7a1a" stroke-width="2"/></g>')
        o += '</g>'
    return f'<g id="{pid}" transform="translate({x},{y}) scale({s})">{o}</g>'

def herb_icon(pid, x, y, s=1.0):
    return (f'<g id="{pid}" transform="translate({x},{y}) scale({s})"><circle r="120" fill="url(#herbglow)"/>'
            f'<path d="M0,60 L0,-10" stroke="#3c6a18" stroke-width="10"/>'
            + "".join(f'<path d="M0,{yy} Q{k*70},{yy-30} {k*80},{yy-70} Q{k*20},{yy-60} 0,{yy} Z" fill="#c9f26a" stroke="#3c6a18" stroke-width="5"/>' for yy, k in [(30, -1), (10, 1), (-10, -1)])
            + '<circle cx="0" cy="-40" r="16" fill="#fffbd0" stroke="#e0b84a" stroke-width="4"/></g>')

def arrow(pid, x, y, s=1.0):
    return (f'<g id="{pid}" transform="translate({x},{y}) scale({s})">'
            f'<path d="M-260,0 L40,0" stroke="#ffdf6a" stroke-width="40" stroke-linecap="round" opacity=".35"/>'
            f'<path d="M-240,0 L30,0" stroke="{INK}" stroke-width="12"/><path d="M-240,0 L30,0" stroke="#d7a43a" stroke-width="6"/>'
            f'<path d="M30,-22 L80,0 L30,22 Z" fill="#dfe6ee" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-240,0 L-275,-26 L-200,0 L-275,26 Z" fill="{RED}" stroke="{INK}" stroke-width="4"/></g>')

def sky(sid, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return (f'<defs><linearGradient id="{sid}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{sid})"/>')

def stars(seed, n, ymax=1100):
    r = random.Random(seed)
    return "".join(f'<circle class="star" cx="{r.randint(0,W)}" cy="{r.randint(0,ymax)}" r="{r.uniform(1.5,4.5):.1f}" fill="#fff" opacity="{r.uniform(.3,.95):.2f}"/>' for _ in range(n))

def glow(x, y, r, gid="warmglow", op=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})" opacity="{op}"/>'

def ground(y, color, edge):
    return f'<path d="M0,{y} Q270,{y-30} 540,{y} Q810,{y+30} 1080,{y} L1080,{H} L0,{H} Z" fill="{color}" stroke="{edge}" stroke-width="6"/>'

def lanka_skyline(y):
    o, r = "", random.Random(3)
    x = -20
    while x < W:
        w, h = r.randint(90, 160), r.randint(220, 520)
        o += f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#2a0e1c"/>'
        o += f'<circle cx="{x+w/2}" cy="{y-h}" r="{w*0.42:.0f}" fill="#2a0e1c"/>'
        o += f'<path d="M{x+w/2},{y-h-w*0.42-70} L{x+w/2-8},{y-h-w*0.3} L{x+w/2+8},{y-h-w*0.3} Z" fill="#2a0e1c"/>'
        for _ in range(r.randint(2, 5)):
            o += f'<rect x="{x+r.randint(12,w-30)}" y="{y-r.randint(40,h-20)}" width="14" height="22" rx="7" fill="#ffb347" opacity=".85"/>'
        x += w + r.randint(-10, 30)
    return o

def cloud(cid, x, y, s=1.0, op=0.9):
    return (f'<g id="{cid}" transform="translate({x},{y}) scale({s})" opacity="{op}">'
            '<ellipse cx="0" cy="0" rx="160" ry="55" fill="#fff"/><ellipse cx="-70" cy="-30" rx="80" ry="60" fill="#fff"/>'
            '<ellipse cx="50" cy="-45" rx="95" ry="75" fill="#fff"/></g>')

def peaks(y, color, snow, seed, n=5, hmin=300, hmax=650):
    r, o = random.Random(seed), ""
    xs = [i * W / (n - 1) for i in range(n)]
    for i, x in enumerate(xs):
        h, w = r.randint(hmin, hmax), r.randint(260, 380)
        o += f'<path d="M{x-w},{y} L{x},{y-h} L{x+w},{y} Z" fill="{color}"/>'
        o += f'<path d="M{x-w*0.28:.0f},{y-h*0.72:.0f} L{x},{y-h} L{x+w*0.28:.0f},{y-h*0.72:.0f} L{x+w*0.1:.0f},{y-h*0.78:.0f} L{x},{y-h*0.7:.0f} L{x-w*0.1:.0f},{y-h*0.78:.0f} Z" fill="{snow}"/>'
    return o

SHARED_DEFS = f"""<svg width="0" height="0" style="position:absolute"><defs>
<radialGradient id="warmglow"><stop offset="0" stop-color="#ffcf6a" stop-opacity=".75"/><stop offset="1" stop-color="#ffcf6a" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#fff6d6" stop-opacity=".55"/><stop offset="1" stop-color="#fff6d6" stop-opacity="0"/></radialGradient>
<radialGradient id="herbglow"><stop offset="0" stop-color="#eaff8a" stop-opacity=".95"/><stop offset=".4" stop-color="#b8ff5a" stop-opacity=".45"/><stop offset="1" stop-color="#b8ff5a" stop-opacity="0"/></radialGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#fff2b0" stop-opacity="1"/><stop offset=".25" stop-color="#ffc24a" stop-opacity=".8"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>
<radialGradient id="fireglow"><stop offset="0" stop-color="#ff9a3a" stop-opacity=".7"/><stop offset="1" stop-color="#ff5a1a" stop-opacity="0"/></radialGradient>
</defs></svg>"""
