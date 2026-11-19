#!/usr/bin/env python3
"""Builds page.html: a one-page front page of the world's news for Thursday 19 November 2026."""
import html, sys

REG = {  # region -> colour
    "ASIA-PACIFIC": "#b3261e", "EUROPE": "#2b5fa8", "AMERICAS": "#2f7d4f",
    "MIDDLE EAST": "#c2691c", "AFRICA": "#7a5a1e", "WORLD": "#5b4b8a",
}

# --- illustrations (inline SVG, viewBox 0 0 300 96) -------------------------------------------------
def flag_us(x, y):
    s = f'<rect x="{x}" y="{y}" width="46" height="30" fill="#fff"/>'
    for i in range(0, 7, 2):
        s += f'<rect x="{x}" y="{y + i * 30 / 7:.1f}" width="46" height="{30 / 7:.1f}" fill="#b22234"/>'
    return s + f'<rect x="{x}" y="{y}" width="20" height="{4 * 30 / 7:.1f}" fill="#3c3b6e"/>'

def flag_cn(x, y):
    return (f'<rect x="{x}" y="{y}" width="46" height="30" fill="#de2910"/>'
            f'<polygon points="{x+9},{y+5} {x+10.8},{y+10} {x+16},{y+10} {x+11.8},{y+13} {x+13.4},{y+18} {x+9},{y+15} {x+4.6},{y+18} {x+6.2},{y+13} {x+2},{y+10} {x+7.2},{y+10}" fill="#ffde00"/>')

def flag_ru(x, y):
    return (f'<rect x="{x}" y="{y}" width="46" height="10" fill="#fff"/><rect x="{x}" y="{y+10}" width="46" height="10" fill="#0039a6"/>'
            f'<rect x="{x}" y="{y+20}" width="46" height="10" fill="#d52b1e"/>')

ART = {}
ART[1] = ('<rect width="300" height="96" fill="#dfe9f2"/>'
          + ''.join(f'<rect x="{x}" y="{96-h}" width="{w}" height="{h}" fill="#9fb3c8"/>' for x, w, h in
                    [(6, 22, 40), (32, 16, 58), (52, 26, 34), (232, 20, 52), (256, 16, 36), (276, 20, 62)])
          + '<rect x="0" y="78" width="300" height="18" fill="#3b4a5c"/>'
          + ''.join(f'<rect x="{x+22}" y="24" width="2.5" height="56" fill="#222"/>' for x in (72, 127, 182))
          + flag_us(49, 22) + flag_cn(104, 22) + flag_ru(159, 22)
          + ''.join(f'<rect x="{x}" y="21.5" width="46.5" height="30.5" fill="none" stroke="#222" stroke-width="1"/>' for x in (49, 104, 159))
          + '<ellipse cx="128" cy="80" rx="74" ry="7" fill="#7a4b2a"/>')
ART[2] = ('<rect width="300" height="96" fill="#e9e4d4"/><rect x="0" y="80" width="300" height="16" fill="#8b9a6b"/>'
          '<rect x="60" y="46" width="180" height="36" fill="#b9a585"/><polygon points="52,46 150,22 248,46" fill="#6d5a44"/>'
          '<rect x="140" y="6" width="20" height="40" fill="#9c8767"/><polygon points="138,8 150,-6 162,8" fill="#6d5a44"/>'
          + ''.join(f'<rect x="{x}" y="54" width="10" height="28" fill="#5d4d3b"/>' for x in range(72, 232, 22))
          + '<g stroke="#1b1b1b" stroke-width="3" fill="none"><line x1="262" y1="20" x2="262" y2="74"/><line x1="240" y1="30" x2="284" y2="30"/>'
            '<path d="M232 50 a8 8 0 0 0 16 0 z" fill="#c8a03a"/><path d="M276 50 a8 8 0 0 0 16 0 z" fill="#c8a03a"/>'
            '<line x1="240" y1="30" x2="234" y2="50"/><line x1="240" y1="30" x2="246" y2="50"/><line x1="284" y1="30" x2="278" y2="50"/><line x1="284" y1="30" x2="290" y2="50"/></g>'
          '<rect x="250" y="74" width="24" height="5" fill="#1b1b1b"/>')
ART[3] = ('<rect width="300" height="96" fill="#0f2f2a"/>'
          + ''.join(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="#1f4a43" stroke-width="1"/>' for y in (24, 48, 72))
          + ''.join(f'<rect x="{20 + i * 30}" y="{96 - h}" width="18" height="{h}" fill="{c}"/>' for i, (h, c) in enumerate(
              [(22, "#3fae7a"), (30, "#3fae7a"), (26, "#d9534f"), (40, "#3fae7a"), (36, "#d9534f"), (52, "#3fae7a"), (62, "#3fae7a"), (74, "#3fae7a")]))
          + '<polyline points="29,70 59,62 89,66 119,52 149,56 179,40 209,30 239,18" fill="none" stroke="#f3c64b" stroke-width="3"/>'
            '<text x="12" y="20" font-family="Inter" font-weight="800" font-size="16" fill="#fff">ANT</text>'
            '<text x="52" y="20" font-family="Inter" font-weight="600" font-size="9" fill="#9fd3c0">NASDAQ · FIRST DAY</text>'
            '<text x="292" y="22" text-anchor="end" font-family="Inter" font-weight="800" font-size="18" fill="#f3c64b">$83</text>')
ART[4] = ('<rect width="300" height="96" fill="#1c2340"/>'
          + ''.join(f'<rect x="{x}" y="{96-h}" width="{w}" height="{h}" fill="#3a4470"/>' for x, w, h in
                    [(10, 30, 26), (48, 18, 40), (72, 40, 20), (120, 14, 60), (142, 34, 30), (184, 22, 44), (214, 44, 24), (266, 24, 36)])
          + '<path d="M20 20 Q150 -10 196 34" fill="none" stroke="#ffb347" stroke-width="2.5" stroke-dasharray="6 4"/>'
            '<path d="M286 86 Q260 50 204 38" fill="none" stroke="#7fd1ff" stroke-width="2.5"/>'
            '<polygon points="200,16 205,30 220,26 210,37 222,48 206,45 200,60 195,45 178,48 190,37 180,26 195,30" fill="#ffd166" stroke="#ff7b00" stroke-width="2"/>')
ART[5] = ('<rect width="300" height="96" fill="#2c5d7c"/><polygon points="0,0 96,0 76,26 92,54 60,96 0,96" fill="#d8c79a"/>'
          '<g fill="none" stroke="#fff" stroke-linecap="round"><circle cx="196" cy="48" r="7" stroke-width="4"/>'
          '<path d="M196 30 a18 18 0 0 1 18 18" stroke-width="5"/><path d="M196 66 a18 18 0 0 1 -18 -18" stroke-width="5"/>'
          '<path d="M196 16 a32 32 0 0 1 32 32" stroke-width="5"/><path d="M196 80 a32 32 0 0 1 -32 -32" stroke-width="5"/></g>'
          '<path d="M150 58 L104 62" stroke="#ffde59" stroke-width="3" stroke-dasharray="5 4"/><polygon points="98,62 108,56 108,68" fill="#ffde59"/>'
          '<text x="8" y="36" font-family="Inter" font-weight="800" font-size="11" fill="#5a4a22">ODISHA</text>')
ART[6] = ('<rect width="300" height="96" fill="#f0dfb8"/><circle cx="238" cy="30" r="20" fill="#e2622b"/>'
          '<path d="M0 72 Q80 44 160 66 T300 58 V96 H0 Z" fill="#5f9b5a"/>'
          '<rect x="22" y="18" width="110" height="34" rx="3" fill="#1d5c4a"/>'
          '<text x="77" y="42" text-anchor="middle" font-family="Inter" font-weight="800" font-size="20" fill="#fff">COP31</text>'
          '<rect x="74" y="52" width="6" height="26" fill="#1d5c4a"/>'
          '<circle cx="170" cy="48" r="17" fill="#fff" stroke="#222" stroke-width="3"/><path d="M170 37 V48 L178 53" fill="none" stroke="#b3261e" stroke-width="3" stroke-linecap="round"/>')
ART[7] = ('<rect width="300" height="96" fill="#2a1447"/><circle cx="150" cy="78" r="40" fill="#ff8a3c"/><circle cx="150" cy="78" r="28" fill="#ffc24b"/>'
          + ''.join(f'<rect x="{x}" y="{96-h}" width="{w}" height="{h}" fill="#150a26"/>' for x, w, h in
                    [(0, 30, 30), (34, 20, 52), (58, 28, 24), (212, 24, 40), (240, 18, 60), (262, 38, 28)])
          + '<rect x="98" y="26" width="104" height="44" rx="20" fill="#f4f1ea" stroke="#111" stroke-width="3"/>'
            '<rect x="118" y="40" width="6" height="18" fill="#111"/><rect x="112" y="46" width="18" height="6" fill="#111"/>'
            '<circle cx="172" cy="42" r="4.5" fill="#e0457b"/><circle cx="182" cy="52" r="4.5" fill="#2f7d4f"/><circle cx="162" cy="52" r="4.5" fill="#2b5fa8"/>'
            '')
ART[8] = ('<rect width="300" height="96" fill="#cfe1ee"/><rect x="0" y="70" width="300" height="26" fill="#3f6f93"/>'
          '<rect x="0" y="52" width="300" height="7" fill="#444"/>'
          + ''.join(f'<rect x="{x}" y="59" width="6" height="22" fill="#555"/>' for x in range(14, 300, 34))
          + '<path d="M104 52 Q150 8 196 52" fill="none" stroke="#444" stroke-width="5"/>'
          + ''.join(f'<line x1="{x}" y1="52" x2="{x}" y2="{52 - (46 - abs(150 - x)) * 0.86:.0f}" stroke="#444" stroke-width="2"/>' for x in range(116, 190, 12))
          + '<g fill="#3a3a3a"><circle cx="232" cy="38" r="12"/><circle cx="246" cy="24" r="15"/><circle cx="262" cy="10" r="13"/></g>'
            '<polygon points="224,52 230,40 236,48 240,36 246,52" fill="#ff7b00"/>')
ART[9] = ('<rect width="300" height="96" fill="#e6d3a3"/><rect x="0" y="74" width="300" height="22" fill="#c9b27c"/>'
          '<rect x="146" y="0" width="8" height="96" fill="#f2c200"/>'
          '<text x="140" y="34" text-anchor="end" font-family="Inter" font-weight="800" font-size="9" fill="#6b5a2a">YELLOW LINE</text>'
          '<g fill="#4c5a3a"><rect x="168" y="50" width="86" height="20" rx="4"/><rect x="190" y="36" width="42" height="16" rx="3"/>'
          '<rect x="124" y="41" width="68" height="5"/><rect x="160" y="68" width="102" height="12" rx="6" fill="#2f3826"/></g>'
          + ''.join(f'<circle cx="{x}" cy="74" r="4" fill="#77805f"/>' for x in range(170, 258, 14))
          + '<polygon points="120,44 106,38 106,50" fill="#b3261e"/>')
ART[10] = ('<rect width="300" height="96" fill="#3b2a20"/><rect x="92" y="8" width="116" height="80" fill="#c9a23a"/><rect x="101" y="17" width="98" height="62" fill="#1f3f7a"/>'
           '<g fill="none" stroke="#ffd84d" stroke-width="3" stroke-linecap="round"><path d="M112 36 q8 -10 16 0 t16 0"/><path d="M150 30 q8 -10 16 0 t16 0"/><path d="M118 52 q8 -10 16 0 t16 0"/></g>'
           '<circle cx="182" cy="56" r="9" fill="#ffd84d"/><path d="M101 79 L120 62 L136 72 L156 58 L199 79 Z" fill="#274f2a"/>'
           '<rect x="226" y="28" width="46" height="16" rx="3" fill="#8b5a2b" transform="rotate(-28 249 36)"/><rect x="246" y="40" width="6" height="40" fill="#8b5a2b" transform="rotate(-28 249 60)"/>'
           '<text x="46" y="52" text-anchor="middle" font-family="Inter" font-weight="800" font-size="15" fill="#ffd84d">$190.4m</text>')
ART[11] = ('<rect width="300" height="96" fill="#dfe6ee"/><rect x="0" y="82" width="300" height="14" fill="#9aa5b1"/>'
           '<rect x="96" y="34" width="108" height="10" fill="#b79b6a"/><rect x="104" y="26" width="92" height="8" fill="#a48857"/>'
           + ''.join(f'<rect x="{x}" y="44" width="9" height="38" fill="#b79b6a"/>' for x in (100, 119, 138, 157, 176, 191))
           + '<rect x="138" y="12" width="24" height="14" fill="#7d6a45"/>'
             '<rect x="30" y="20" width="3" height="62" fill="#333"/><rect x="33" y="20" width="44" height="14" fill="#0057b7"/><rect x="33" y="34" width="44" height="14" fill="#ffd700"/>'
             '<rect x="226" y="20" width="3" height="62" fill="#333"/><rect x="229" y="20" width="44" height="28" fill="#003399"/>'
           + ''.join(f'<circle cx="{251 + 9 * __import__("math").cos(a * 0.5236):.1f}" cy="{34 + 9 * __import__("math").sin(a * 0.5236):.1f}" r="1.4" fill="#ffcc00"/>' for a in range(12)))

def art(n):
    return f'<svg class="art" viewBox="0 0 300 96" preserveAspectRatio="xMidYMid slice">{ART[n]}</svg>'

# --- stories ----------------------------------------------------------------------------------------
HERO = [
    (1, "ASIA-PACIFIC", "SHENZHEN · SUMMIT", "Trump, Xi and Putin meet for first three-way summit",
     "The US, Chinese and Russian leaders sit down together at APEC in China. Nuclear arms, the Iran war and Ukraine are on the table."),
    (2, "EUROPE", "THE HAGUE · JUSTICE", "World Court rules on Myanmar genocide case",
     "The UN’s top court delivers its judgment on the 2017 Rohingya killings, seven years after The Gambia brought the case."),
    (3, "AMERICAS", "NEW YORK · MARKETS", "Anthropic starts trading after record IPO",
     "The Claude maker lists on Nasdaq. Shares were priced at $83, above the $70–$78 range, valuing it above $1.4tn."),
]
CARDS = [
    (4, "MIDDLE EAST", "RIYADH · IRAN WAR", "Houthi missile aimed at Riyadh is shot down",
     "Falling debris causes damage, the Saudi-led coalition says."),
    (5, "ASIA-PACIFIC", "ODISHA · STORM", "India moves 50,000 as Cyclone Akvan nears",
     "Landfall is forecast for Friday between Narsapur and Puri."),
    (6, "WORLD", "ANTALYA · CLIMATE", "COP31 deadlocked with one day left",
     "Ministers are split over fossil fuels and finance, the UN says."),
    (7, "AMERICAS", "WORLDWIDE · GAMES", "GTA VI arrives after a 13-year wait",
     "The most anticipated video game in years goes on sale."),
    (8, "EUROPE", "KERCH STRAIT · WAR", "Crimean Bridge attacked again",
     "A Russian official reports a new strike on the bridge."),
    (9, "MIDDLE EAST", "GAZA · CEASEFIRE", "Israeli troops cross Gaza’s Yellow Line",
     "A rare ground operation pushes beyond the truce line."),
    (10, "AMERICAS", "ART · AUCTION", "Van Gogh sells for a record $190.4m",
     "The sale follows a dispute over the painting’s Nazi-era past."),
    (11, "EUROPE", "BERLIN · UKRAINE", "Europe’s leaders rally behind Kyiv",
     "Ukraine’s allies meet in Berlin as the big three talk in China."),
]
BRIEFS = [
    (12, "ASIA-PACIFIC", "SUVA", "Fiji declares a state of disaster over El Niño drought."),
    (13, "ASIA-PACIFIC", "WELLINGTON", "Court rules pay-equity overhaul breached women’s rights."),
    (14, "ASIA-PACIFIC", "HONG KONG", "Case dropped against captain over Baltic pipeline damage."),
    (15, "ASIA-PACIFIC", "KUALA LUMPUR", "UN refugee agency halts registration in Malaysia."),
    (16, "MIDDLE EAST", "SANAA", "UNICEF: 64 children killed in Yemen since 3 September."),
    (17, "ASIA-PACIFIC", "SHENZHEN", "Japan’s PM Takaichi holds talks with Putin at APEC."),
    (18, "ASIA-PACIFIC", "SHENZHEN", "Putin tells APEC Russia is an “integral part” of Asia-Pacific."),
    (19, "WORLD", "UNITED NATIONS", "UN committee passes North Korea rights resolution, 22nd year running."),
    (20, "ASIA-PACIFIC", "SEOUL", "College entrance exam held under an AI-cheating crackdown."),
    (21, "AMERICAS", "MIAMI", "Torrential rain floods South Florida."),
    (22, "AMERICAS", "CALIFORNIA", "Waymo pulls driverless cars off freeways after a state ban."),
    (23, "AMERICAS", "WASHINGTON", "Musk says he felt “pretty foolish” over his midterm spending."),
    (24, "MIDDLE EAST", "IRAN WAR", "Trump claims Iran is seeking biological weapons."),
    (25, "MIDDLE EAST", "KAFR QASIM", "Eight Palestinians hurt as a settler drives into them."),
    (26, "MIDDLE EAST", "RIYADH", "Saudi crown prince meets the US Central Command chief."),
    (27, "ASIA-PACIFIC", "CRICKET", "Bumrah strikes: New Zealand 60–4 at lunch, first Test v India."),
    (28, "AFRICA", "CONGO BASIN", "More floods forecast for DR Congo, Somalia and South Africa."),
    (29, "ASIA-PACIFIC", "SHENZHEN", "Trump and Canada’s Carney discuss trade, Ottawa says."),
]
ALL = [(n, r) for n, r, *_ in HERO + CARDS + BRIEFS]
COUNT = {r: sum(1 for _, x in ALL if x == r) for r in REG}
assert sum(COUNT.values()) == len(ALL) == 29

NUMS = [("3", "leaders at one table in Shenzhen — a first"), ("$83", "Anthropic’s IPO price; trading starts today"),
        ("7 yrs", "since the Rohingya case was filed"), ("50,000", "moved from Cyclone Akvan’s path"),
        ("13 yrs", "the wait for GTA VI, out today"), ("$190.4m", "a record for a Van Gogh")]

# --- map --------------------------------------------------------------------------------------------
MW, MH = 262, 134
def xy(lon, lat):
    return (lon + 170) / 350 * MW, (78 - lat) / 136 * MH
LAND = [
    [(-165, 65), (-140, 70), (-95, 72), (-75, 62), (-55, 50), (-75, 35), (-80, 26), (-97, 18), (-105, 22), (-118, 33), (-125, 48), (-150, 60)],
    [(-97, 18), (-83, 9), (-78, 8), (-70, 12), (-50, 0), (-35, -7), (-40, -22), (-58, -38), (-68, -54), (-74, -45), (-70, -18), (-80, -5), (-78, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (5, 53), (8, 57), (5, 61), (15, 69), (30, 70), (40, 66), (60, 68), (60, 50), (40, 45), (28, 40), (22, 37), (12, 38), (3, 43), (-5, 36)],
    [(-17, 15), (-10, 30), (0, 36), (11, 37), (32, 31), (43, 11), (51, 11), (40, -15), (33, -27), (20, -35), (12, -17), (9, 3), (-8, 5)],
    [(60, 68), (100, 77), (140, 72), (170, 66), (160, 58), (142, 48), (128, 38), (122, 30), (110, 20), (105, 9), (100, 14), (92, 21), (80, 8), (72, 20), (60, 25), (57, 18), (45, 13), (35, 29), (28, 40), (40, 45), (60, 50)],
    [(114, -22), (130, -12), (142, -11), (153, -27), (146, -39), (131, -32), (115, -34)],
    [(172, -35), (178, -38), (171, -46), (167, -45)], [(131, 32), (141, 36), (142, 44), (136, 36)], [(-6, 50), (1, 52), (-3, 58), (-6, 56)],
    [(96, 5), (106, -6), (118, -8), (117, 4), (104, 1)], [(-50, 60), (-22, 70), (-30, 78), (-60, 78)],
]
PINS = {1: (114, 22.5), 2: (4.3, 52), 3: (-74, 40.7), 4: (46.7, 24.7), 5: (85, 20), 6: (30.7, 36.9), 8: (36.5, 45.3), 9: (34.4, 31.4), 11: (13.4, 52.5)}
NUDGE = {2: (-7, -4), 11: (6, -6), 6: (-6, 4), 9: (-4, 9), 8: (7, -3), 4: (7, 5)}
DOTS = [(178, -18), (174, -41), (101.7, 3), (45, 15), (127, 37.5), (-80, 26), (-122, 37), (18, 2), (139.7, 35.7)]
def worldmap():
    s = f'<svg viewBox="0 0 {MW} {MH}" width="{MW}" height="{MH}"><rect width="{MW}" height="{MH}" fill="#17324d"/>'
    for poly in LAND:
        s += '<polygon points="' + ' '.join('%.1f,%.1f' % xy(*p) for p in poly) + '" fill="#d9c79a"/>'
    for lon, lat in DOTS:
        x, y = xy(lon, lat)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#9fb4c8" stroke="#17324d" stroke-width="0.8"/>'
    rof = dict(ALL)
    for n, (lon, lat) in PINS.items():
        x, y = xy(lon, lat); dx, dy = NUDGE.get(n, (0, 0)); x += dx; y += dy
        s += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{REG[rof[n]]}" stroke="#fff" stroke-width="1.2"/>'
              f'<text x="{x:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.5" fill="#fff">{n}</text>')
    return s + '</svg>'

# --- page -------------------------------------------------------------------------------------------
e = html.escape
def card(st, cls):
    n, reg, kick, head, body = st
    return (f'<div class="card {cls}" style="border-top-color:{REG[reg]}">{art(n)}<div class="tx">'
            f'<div class="kick" style="color:{REG[reg]}"><b class="n" style="background:{REG[reg]}">{n}</b>{e(kick)}</div>'
            f'<h2>{e(head)}</h2><p>{e(body)}</p></div></div>')

bar = ''.join(f'<span style="background:{REG[r]};flex:{max(COUNT[r], 2.6)}">{r} {COUNT[r]}</span>' for r in REG)
nums = ''.join(f'<div><b>{e(a)}</b><i>{e(b)}</i></div>' for a, b in NUMS)
briefs = ''.join(f'<p><b style="color:{REG[r]}">{n} {e(place)}</b> — {e(t)}</p>' for n, r, place, t in BRIEFS)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1024px;height:1024px;background:#f6f1e4;color:#161412;font-family:Inter,sans-serif;overflow:hidden}
.pg{position:absolute;inset:0;padding:12px 18px 10px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;letter-spacing:2.2px;border-bottom:3px solid #161412;padding-bottom:4px}
.top span:first-child{color:#b3261e}
h1{font-family:'Bitstream Charter',Charter,serif;font-weight:700;font-size:67px;line-height:68px;letter-spacing:-1.6px;margin-top:2px;white-space:nowrap}
.deck{font-family:'Bitstream Charter',serif;font-style:italic;font-size:17.5px;color:#8f1d17;margin:1px 0 6px}
.bar{display:flex;height:17px;font-size:9.5px;font-weight:800;letter-spacing:.6px;color:#fff}
.bar span{display:flex;align-items:center;justify-content:center;white-space:nowrap}
.nums{display:grid;grid-template-columns:repeat(6,1fr);border-bottom:2px solid #161412;padding:4px 0 4px;margin-bottom:6px}
.nums div{text-align:center;padding:0 6px;border-left:1px solid #b9b1a0}.nums div:first-child{border-left:0}
.nums b{display:block;font-family:'Bitstream Charter',serif;font-size:23px;line-height:24px;color:#8f1d17}
.nums i{display:block;font-style:normal;font-size:9.6px;line-height:11.5px;color:#3d3832}
.row{display:grid;gap:7px;margin-bottom:7px}.r3{grid-template-columns:repeat(3,1fr)}.r4{grid-template-columns:repeat(4,1fr)}
.card{background:#fffdf7;border:1px solid #b9b1a0;border-top:5px solid;overflow:hidden}
.art{display:block;width:100%}.hero .art{height:86px}.sm .art{height:49px}
.tx{padding:5px 9px 7px}
.kick{font-size:9.8px;font-weight:800;letter-spacing:1.3px;display:flex;align-items:center;gap:6px;white-space:nowrap}
.n{display:inline-flex;align-items:center;justify-content:center;min-width:17px;height:17px;border-radius:9px;color:#fff;font-size:10.5px;letter-spacing:0;padding:0 3px}
h2{font-family:'Bitstream Charter',serif;font-weight:700;letter-spacing:-.2px}
.hero h2{font-size:23.5px;line-height:25px;margin:4px 0 4px}.hero p{font-size:12.3px;line-height:15.4px;color:#2a2622}
.sm h2{font-size:15.6px;line-height:17px;margin:3px 0 3px}.sm p{font-size:10.8px;line-height:13px;color:#2a2622}
.bot{display:grid;grid-template-columns:262px 1fr;gap:12px;flex:1;min-height:0}
.map{background:#17324d;display:flex;flex-direction:column}
.map h3{color:#fff;font-size:10.5px;letter-spacing:1.8px;font-weight:800;padding:6px 8px 3px}
.map small{color:#c9d6e2;font-size:9.4px;line-height:11.4px;padding:3px 8px 6px;display:block}
.br h3{font-size:10.8px;letter-spacing:1.6px;font-weight:800;color:#8f1d17;border-bottom:1.5px solid #161412;padding-bottom:3px;margin-bottom:4px}
.cols{column-count:3;column-gap:12px}
.cols p{font-size:10.3px;line-height:12.3px;margin-bottom:3px;break-inside:avoid}
.cols b{font-weight:800;letter-spacing:.2px}
.chk{border:2px solid #8f1d17;background:#fffdf7;font-size:10px;line-height:12.4px;padding:4px 9px;margin-top:6px}
.chk b{color:#8f1d17;letter-spacing:1px}
.ft{font-size:9.2px;line-height:11.5px;color:#4a443d;margin-top:4px;white-space:nowrap}
"""

PAGE = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg">
<div class="top"><span>THE WORLD IN ONE DAY</span><span>29 STORIES · 6 REGIONS · ONE PAGE</span></div>
<h1>Thursday 19 November 2026</h1>
<div class="deck">Three rival powers at one table · A genocide verdict in The Hague · The biggest stock-market debut on record</div>
<div class="bar">{bar}</div>
<div class="nums">{nums}</div>
<div class="row r3">{''.join(card(s, 'hero') for s in HERO)}</div>
<div class="row r4">{''.join(card(s, 'sm') for s in CARDS[:4])}</div>
<div class="row r4">{''.join(card(s, 'sm') for s in CARDS[4:])}</div>
<div class="bot"><div class="map"><h3>WHERE IT HAPPENED</h3>{worldmap()}<small>Pins match the numbered cards; grey dots mark briefs.</small></div>
<div class="br"><h3>ALSO ON THURSDAY 19 NOVEMBER — 18 MORE STORIES</h3><div class="cols">{briefs}</div></div></div>
<div class="chk"><b>DATE CHECK</b> — Reported on Wednesday 18 Nov, so not counted as Thursday’s news: Trump’s arrival in Shenzhen and the banquet handshake · Anthropic setting its $83 price · House Democrats nominating Jeffries for Speaker · Pew’s forecast on Islam by 2035.</div>
<div class="ft"><b>Every story above happened, or was first reported, on Thursday 19 November 2026.</b> Claims are attributed. Sources: Reuters, AP, BBC, Al Jazeera, Bloomberg, UN News, Indian Express. Original drawings.</div>
</div></body></html>"""
open(sys.argv[1], 'w', encoding='utf-8').write(PAGE)
print('ok', COUNT)
