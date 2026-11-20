#!/usr/bin/env python3
"""Builds page.html — the front page of the world's news for Thursday 19 November 2026.

The page is three tiers deep: three leads that each carry a one-sentence
explanation, twelve smaller drawn cards, and twenty-eight one-line briefs
beside a numbered world map. Nothing that matters is buried: the date is
the largest thing on the page, the leads follow, everything else is
texture. The drawings carry no words — the headlines do that — and the
palette stays cream and ink with muted region markers so the whole thing
reads as one composition, not a wall of tiles.
"""
import html, sys

REG = {  # region -> colour (muted editorial tones)
    "ASIA-PACIFIC": "#8f3a32", "EUROPE": "#3c5a80", "AMERICAS": "#44684e",
    "MIDDLE EAST": "#96602c", "AFRICA": "#6e5a33", "WORLD": "#5a5468",
}

# --- illustrations (inline SVG, viewBox 0 0 300 96, no words: the headline tells the story -----
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
ART[1] = ('<rect width="300" height="96" fill="#e7e0d0"/>'
          + ''.join(f'<rect x="{x}" y="{96-h}" width="{w}" height="{h}" fill="#b8ae97"/>' for x, w, h in
                    [(6, 22, 40), (32, 16, 58), (52, 26, 34), (232, 20, 52), (256, 16, 36), (276, 20, 62)])
          + '<rect x="0" y="78" width="300" height="18" fill="#4a4438"/>'
          + ''.join(f'<rect x="{x+22}" y="24" width="2.5" height="56" fill="#2a2620"/>' for x in (72, 127, 182))
          + flag_us(49, 22) + flag_cn(104, 22) + flag_ru(159, 22)
          + ''.join(f'<rect x="{x}" y="21.5" width="46.5" height="30.5" fill="none" stroke="#2a2620" stroke-width="1"/>' for x in (49, 104, 159))
          + '<ellipse cx="128" cy="80" rx="74" ry="7" fill="#6e5a3a"/>')
ART[2] = ('<rect width="300" height="96" fill="#e9e4d4"/><rect x="0" y="80" width="300" height="16" fill="#8b9a6b"/>'
          '<rect x="60" y="46" width="180" height="36" fill="#b9a585"/><polygon points="52,46 150,22 248,46" fill="#6d5a44"/>'
          '<rect x="140" y="6" width="20" height="40" fill="#9c8767"/><polygon points="138,8 150,-6 162,8" fill="#6d5a44"/>'
          + ''.join(f'<rect x="{x}" y="54" width="10" height="28" fill="#5d4d3b"/>' for x in range(72, 232, 22))
          + '<g stroke="#2a2620" stroke-width="3" fill="none"><line x1="262" y1="20" x2="262" y2="74"/><line x1="240" y1="30" x2="284" y2="30"/>'
            '<path d="M232 50 a8 8 0 0 0 16 0 z" fill="#c8a03a"/><path d="M276 50 a8 8 0 0 0 16 0 z" fill="#c8a03a"/>'
            '<line x1="240" y1="30" x2="234" y2="50"/><line x1="240" y1="30" x2="246" y2="50"/><line x1="284" y1="30" x2="278" y2="50"/><line x1="284" y1="30" x2="290" y2="50"/></g>'
          '<rect x="250" y="74" width="24" height="5" fill="#2a2620"/>')
ART[3] = ('<rect width="300" height="96" fill="#e6e0d2"/>'
          + ''.join(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="#d4ccba" stroke-width="1"/>' for y in (24, 48, 72))
          + ''.join(f'<rect x="{20 + i * 30}" y="{96 - h}" width="18" height="{h}" fill="{c}"/>' for i, (h, c) in enumerate(
              [(22, "#7d8f80"), (30, "#7d8f80"), (26, "#a86a4e"), (40, "#7d8f80"), (36, "#a86a4e"), (52, "#7d8f80"), (62, "#7d8f80"), (74, "#7d8f80")]))
          + '<polyline points="29,70 59,62 89,66 119,52 149,56 179,40 209,30 239,18" fill="none" stroke="#8f6a1e" stroke-width="3"/>')
ART[4] = ('<rect width="300" height="96" fill="#e3dccb"/>'
          + ''.join(f'<rect x="{x}" y="{96-h}" width="{w}" height="{h}" fill="#a89c85"/>' for x, w, h in
                    [(10, 30, 26), (48, 18, 40), (72, 40, 20), (120, 14, 60), (142, 34, 30), (184, 22, 44), (214, 44, 24), (266, 24, 36)])
          + '<path d="M20 20 Q150 -10 196 34" fill="none" stroke="#8f3a32" stroke-width="2.5" stroke-dasharray="6 4"/>'
            '<path d="M286 86 Q260 50 204 38" fill="none" stroke="#3c5a80" stroke-width="2.5"/>'
            '<polygon points="200,16 205,30 220,26 210,37 222,48 206,45 200,60 195,45 178,48 190,37 180,26 195,30" fill="#c8a03a" stroke="#8f6a1e" stroke-width="2"/>')
ART[5] = ('<rect width="300" height="96" fill="#d7ddd8"/>'
          + ''.join(f'<path d="M0 {y} Q75 {y-5} 150 {y} T300 {y}" fill="none" stroke="#b7c2ba" stroke-width="1.4"/>' for y in (26, 46, 66, 86))
          + '<rect x="52" y="40" width="130" height="22" rx="4" fill="#3c4a52"/><rect x="60" y="28" width="70" height="14" rx="3" fill="#5a6a72"/>'
            '<rect x="48" y="62" width="138" height="5" fill="#2a3238"/>'
          + '<g fill="#c88a2e"><polygon points="130,26 142,44 118,44"/><polygon points="150,22 160,38 140,38"/><polygon points="112,30 120,42 104,42"/></g>'
          + '<path d="M210 84 Q216 68 230 58 Q222 72 226 84 Z" fill="#8a8478"/>'
            '<circle cx="196" cy="18" r="8" fill="#c88a2e" stroke="#8f6a1e" stroke-width="2"/>')
ART[6] = ('<rect width="300" height="96" fill="#e7e2d6"/>'
          '<rect x="0" y="72" width="300" height="24" fill="#b3aa96"/>'
          '<path d="M150 8 C120 10 108 26 106 44 L104 72 L196 72 L194 44 C192 26 180 10 150 8 Z" fill="#cfc6b2" stroke="#5a5244" stroke-width="2"/>'
          '<rect x="128" y="44" width="44" height="28" fill="#5a5244"/>'
          + ''.join(f'<rect x="{x}" y="60" width="6" height="12" fill="#8a8070"/>' for x in (86, 100, 208, 222))
          + ''.join(f'<rect x="{x}" y="{88-h}" width="14" height="{h}" fill="{c}"/>' for x, h, c in [(96, 26, "#44684e"), (118, 40, "#44684e"), (186, 34, "#8f3a32"), (208, 22, "#8f3a32")])
          + '<line x1="150" y1="8" x2="150" y2="0" stroke="#5a5244" stroke-width="2"/>')
ART[7] = ('<rect width="300" height="96" fill="#e6d3a3"/><rect x="0" y="74" width="300" height="22" fill="#c9b27c"/>'
          '<rect x="146" y="0" width="8" height="96" fill="#b3862e"/>'
          '<g fill="#4c5a3a"><rect x="168" y="50" width="86" height="20" rx="4"/><rect x="190" y="36" width="42" height="16" rx="3"/>'
          '<rect x="124" y="41" width="68" height="5"/><rect x="160" y="68" width="102" height="12" rx="6" fill="#2f3826"/></g>'
          + ''.join(f'<circle cx="{x}" cy="74" r="4" fill="#77805f"/>' for x in range(170, 258, 14))
          + '<polygon points="120,44 106,38 106,50" fill="#8f3a32"/>')
ART[8] = ('<rect width="300" height="96" fill="#e0dac9"/>'
          + ''.join(f'<rect x="{x}" y="59" width="6" height="22" fill="#8a8070"/>' for x in range(14, 300, 34))
          + '<path d="M104 52 Q150 8 196 52" fill="none" stroke="#5a5244" stroke-width="5"/>'
          + ''.join(f'<line x1="{x}" y1="52" x2="{x}" y2="{52 - (46 - abs(150 - x)) * 0.86:.0f}" stroke="#5a5244" stroke-width="2"/>' for x in range(116, 190, 12))
          + '<g fill="#4a4438"><circle cx="232" cy="38" r="12"/><circle cx="246" cy="24" r="15"/><circle cx="262" cy="10" r="13"/></g>'
            '<polygon points="224,52 230,40 236,48 240,36 246,52" fill="#c88a2e"/>')
ART[9] = ('<rect width="300" height="96" fill="#d7ddd8"/>'
          + ''.join(f'<path d="M0 {y} Q75 {y-4} 150 {y} T300 {y}" fill="none" stroke="#b7c2ba" stroke-width="1.4"/>' for y in (30, 60, 88))
          + '<path d="M10 78 Q80 60 150 74 T290 64" fill="none" stroke="#3c4a52" stroke-width="4"/>'
          + '<g fill="#3c4a52"><rect x="46" y="52" width="64" height="14" rx="3"/><rect x="54" y="42" width="30" height="10" rx="2"/><rect x="150" y="48" width="74" height="16" rx="3"/><rect x="162" y="38" width="34" height="10" rx="2"/></g>'
          + '<circle cx="252" cy="30" r="9" fill="#c88a2e" stroke="#8f6a1e" stroke-width="2"/>')
ART[10] = ('<rect width="300" height="96" fill="#d9e2dd"/>'
           + ''.join(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="#c0ccc5" stroke-width="1"/>' for y in (22, 46, 70))
           + '<circle cx="150" cy="52" r="26" fill="none" stroke="#44684e" stroke-width="3"/>'
           '<line x1="150" y1="52" x2="150" y2="34" stroke="#44684e" stroke-width="3"/><line x1="150" y1="52" x2="164" y2="58" stroke="#44684e" stroke-width="3"/>'
           + '<path d="M228 24 Q252 6 276 24" fill="none" stroke="#c88a2e" stroke-width="3"/>'
             '<circle cx="228" cy="24" r="3" fill="#c88a2e"/><circle cx="276" cy="24" r="3" fill="#c88a2e"/>')
ART[11] = ('<rect width="300" height="96" fill="#d8e0e6"/>'
           + '<circle cx="168" cy="46" r="30" fill="none" stroke="#3c5a80" stroke-width="3"/>'
           + ''.join(f'<path d="M168 {46-r} a{r} {r} 0 0 1 {r} {r}" fill="none" stroke="#3c5a80" stroke-width="2.5"/>' for r in (40, 48))
           + '<path d="M120 58 Q150 50 180 56 T240 52" fill="none" stroke="#44684e" stroke-width="2.5" stroke-dasharray="7 4"/>'
             '<polygon points="240,52 230,46 230,58" fill="#44684e"/>')
ART[12] = ('<rect width="300" height="96" fill="#d7dde2"/>'
           + '<path d="M0 72 Q80 60 160 68 T300 62 V96 H0 Z" fill="#9fb3c0"/>'
           + '<polygon points="70,72 100,28 130,72" fill="#e8edf0" stroke="#8a9aa6" stroke-width="2"/>'
             '<polygon points="120,72 150,40 184,72" fill="#d9e2e8" stroke="#8a9aa6" stroke-width="2"/>'
           + '<rect x="196" y="18" width="3" height="54" fill="#5a5244"/>'
             '<rect x="199" y="18" width="34" height="22" fill="#c8102e"/><rect x="199" y="40" width="34" height="14" fill="#fff"/>')
ART[13] = ('<rect width="300" height="96" fill="#e7e2d6"/>'
           + ''.join(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="#d4ccba" stroke-width="1"/>' for y in (22, 44, 66, 88))
           + '<path d="M24 80 L84 64 L144 68 L204 44 L264 30" fill="none" stroke="#8f3a32" stroke-width="4"/>'
             '<polygon points="264,30 250,28 258,42" fill="#8f3a32"/>'
           + '<circle cx="84" cy="64" r="4" fill="#5a5244"/><circle cx="144" cy="68" r="4" fill="#5a5244"/><circle cx="204" cy="44" r="4" fill="#5a5244"/>')
ART[15] = ('<rect width="300" height="96" fill="#d7dde2"/>'
          + ''.join(f'<path d="M0 {y} Q75 {y-4} 150 {y} T300 {y}" fill="none" stroke="#b7c2ba" stroke-width="1.6"/>' for y in (58, 72, 86))
          + '<path d="M60 58 Q90 40 120 58 T180 58 T240 58" fill="none" stroke="#5a5244" stroke-width="3"/>'
            '<polygon points="118,52 112,62 124,62" fill="#5a5244"/>'
            '<circle cx="150" cy="44" r="5" fill="#c88a2e"/><circle cx="176" cy="38" r="4" fill="#c88a2e"/><circle cx="164" cy="52" r="3" fill="#c88a2e"/>')
ART[14] = ('<rect width="300" height="96" fill="#3b2a20"/><rect x="92" y="8" width="116" height="80" fill="#c9a23a"/><rect x="101" y="17" width="98" height="62" fill="#1f3f7a"/>'
           '<g fill="none" stroke="#ffd84d" stroke-width="3" stroke-linecap="round"><path d="M112 36 q8 -10 16 0 t16 0"/><path d="M150 30 q8 -10 16 0 t16 0"/><path d="M118 52 q8 -10 16 0 t16 0"/></g>'
           '<circle cx="182" cy="56" r="9" fill="#ffd84d"/><path d="M101 79 L120 62 L136 72 L156 58 L199 79 Z" fill="#274f2a"/>'
           '<rect x="226" y="28" width="46" height="16" rx="3" fill="#8b5a2b" transform="rotate(-28 249 36)"/><rect x="246" y="40" width="6" height="40" fill="#8b5a2b" transform="rotate(-28 249 60)"/>')

def art(n):
    return f'<svg class="art" viewBox="0 0 300 96" preserveAspectRatio="xMidYMid slice">{ART[n]}</svg>'

# --- stories ----------------------------------------------------------------------------------------
HERO = [
    (1, "ASIA-PACIFIC", "SHENZHEN · SUMMIT", "Trump, Xi and Putin hold their first three-way summit",
     "The US, Chinese and Russian leaders meet at APEC and issue a “peace declaration” on nuclear risks, oil, UN reform and the ICC."),
    (2, "WORLD", "THE HAGUE · JUSTICE", "World Court finds Myanmar committed genocide",
     "In the first ruling of its kind against a state, the ICJ holds Myanmar responsible for genocide against the Rohingya in 2017 — a 9–6 judgment."),
    (3, "AMERICAS", "NEW YORK · MARKETS", "Anthropic’s debut is the biggest IPO on record",
     "The Claude maker raises $81.3bn at $83 a share and closes up 17% at $97.17; the Dow falls 1,100 points."),
]
CARDS = [
    (4, "MIDDLE EAST", "RIYADH · IRAN WAR", "Houthi missile strikes at Riyadh’s core", ""),
    (5, "MIDDLE EAST", "HORMUZ · SHIPPING", "Two supertankers ablaze after striking mines", ""),
    (6, "AMERICAS", "WASHINGTON · VOTE", "Senate rejects Iran war-powers vote 51–48", ""),
    (7, "MIDDLE EAST", "GAZA · CEASEFIRE", "Israeli troops cross Gaza’s Yellow Line", ""),
    (8, "EUROPE", "BERLIN · UKRAINE", "More than 40 allies rally behind Kyiv", ""),
    (9, "EUROPE", "KERCH · WAR", "Crimean Bridge hit a third time in four days", ""),
    (10, "WORLD", "ANTALYA · CLIMATE", "COP31 nears close amid backlash over weak draft", ""),
    (11, "ASIA-PACIFIC", "ODISHA · STORM", "India moves 300,000 from Cyclone Akvan’s path", ""),
    (12, "EUROPE", "COPENHAGEN · ARCTIC", "Denmark ratifies Greenland security deal", ""),
    (13, "AMERICAS", "WASHINGTON · ECONOMY", "IMF: AI demand will push up interest rates", ""),
    (14, "AMERICAS", "ART · AUCTION", "Van Gogh sells for a record $190.4m", ""),
    (15, "AFRICA", "DAKAR · MIGRATION", "Migrant boat capsizes off Senegal", ""),
]
BRIEFS = [
    (16, "AFRICA", "DAKAR", "Senegal: one dead, dozens missing as a migrant boat capsizes en route to Spain."),
    (17, "EUROPE", "BRUSSELS", "The European Commission is hit by a large-scale cyberattack; data leakage unknown."),
    (18, "AMERICAS", "QUITO", "Hegseth lands in Ecuador on an anti-narcotics tour; a Venezuela pact is announced."),
    (19, "WORLD", "DEEP SPACE", "Voyager 1, 25.9 billion km away, still works almost 50 years after launch."),
    (20, "AFRICA", "NAIROBI", "Kenya discharges its last Ebola patient; no community transmission recorded."),
    (21, "ASIA-PACIFIC", "SHENZHEN", "Japan’s PM Takaichi holds talks with Putin on the summit’s sidelines."),
    (22, "EUROPE", "WARSAW", "Poland’s Tusk on the three-way summit: “God, protect us from such friends.”"),
    (23, "EUROPE", "PARIS", "Macron backs reopening “the question” of Ukraine’s NATO accession."),
    (24, "EUROPE", "PARIS", "French women mark their symbolic ‘unpaid’ day over the gender pay gap."),
    (25, "MIDDLE EAST", "TEHRAN", "Iran rejects the dirty-bomb and bio-weapons claims as disinformation."),
    (26, "WORLD", "VIENNA", "The US, UK, France and Germany press Iran at the IAEA to resume inspections."),
    (27, "MIDDLE EAST", "BAGHDAD", "Iraqi forces deploy into a Kataib Hezbollah stronghold under a deal."),
    (28, "ASIA-PACIFIC", "SHENZHEN", "Xi: nuclear weapons should be “comprehensively prohibited and completely destroyed.”"),
    (29, "ASIA-PACIFIC", "SHENZHEN", "Trump calls the ICC “out of control”; Putin remains under its warrant."),
    (30, "AMERICAS", "WASHINGTON", "Trump: the US will “see what happens” in the Iran war after 1 January."),
    (31, "MIDDLE EAST", "AT SEA", "The carrier USS George Washington leaves the Mideast for the Pacific; two remain."),
    (32, "AFRICA", "FREETOWN", "A West Africa integration summit signs four regional agreements."),
    (33, "MIDDLE EAST", "BEIRUT", "84 Syrian refugees return from Lebanon through a reopened crossing."),
    (34, "ASIA-PACIFIC", "SEOUL", "South Korea holds its college entrance exam under an AI-cheating crackdown."),
    (35, "AMERICAS", "MIAMI", "GTA VI’s first-day sales pass 17 million copies."),
    (36, "EUROPE", "LYON", "Beaujolais Nouveau arrives with a nighttime barrel parade."),
    (37, "EUROPE", "PARIS", "France will monitor YouTubers for political bias ahead of the 2027 election."),
    (38, "ASIA-PACIFIC", "DELHI", "India and Japan flag “economic coercion” and deepen defence ties."),
    (39, "AFRICA", "ABUJA", "Nigerian airstrikes kill 21 militants, the military says."),
    (40, "WORLD", "ANTALYA", "Tuvalu at COP31: “We are here for the survival of our people.”"),
    (41, "AMERICAS", "CALIFORNIA", "A Russian man is arrested for spying on Palantir staff over Ukraine support."),
    (42, "ASIA-PACIFIC", "KUALA LUMPUR", "Malaysia to end visa-free entry for Indians from January."),
    (43, "MIDDLE EAST", "GAZA", "Israel says airstrikes killed two Hamas platoon commanders."),
]
ALL = [(n, r) for n, r, *_ in HERO] + [(n, r) for n, r, *_ in CARDS] + [(n, r) for n, r, *_ in BRIEFS]
COUNT = {r: sum(1 for _, x in ALL if x == r) for r in REG}
assert len({n for n, _ in ALL}) == len(ALL), "story numbers must be unique"

NUMS = [("3", "leaders at one table — a first"), ("9–6", "the World Court’s genocide verdict"),
        ("$81.3bn", "raised by the biggest IPO ever"), ("300,000", "moved from Cyclone Akvan’s path"),
        ("Day 265", "of the Iran war"), ("3rd", "strike on the Crimean Bridge in four days")]

# --- map --------------------------------------------------------------------------------------------
MW, MH = 286, 158
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
PINS = {1: (114, 22.5), 2: (1, 49), 3: (-70, 42.5), 4: (46.7, 24.7), 5: (57, 26.2), 6: (-80, 37.5), 7: (34.4, 31.4),
       8: (14.5, 50), 9: (37.5, 44), 10: (31.5, 38.5), 11: (84.9, 19.3), 12: (10, 57.5), 13: (-73, 44), 15: (-17.6, 14.8)}
NUDGE = {1: (7, 2), 9: (8, -4), 10: (-8, 5), 11: (7, -5), 3: (7, -3), 6: (-7, 4)}
DOTS = [(178, -18), (174, -41), (101.7, 3), (45, 15), (127, 37.5), (-80, 26), (-122, 37), (18, 2), (139.7, 35.7),
       (37, 55), (21, 52), (4.9, 7.5), (-78.5, 0), (12.1, 8), (3.4, 6.4), (77, 28), (135, -25), (-9.5, 12.3)]
def worldmap():
    s = f'<svg viewBox="0 0 {MW} {MH}" width="{MW}" height="{MH}"><rect width="{MW}" height="{MH}" fill="#20364a"/>'
    for poly in LAND:
        s += '<polygon points="' + ' '.join('%.1f,%.1f' % xy(*p) for p in poly) + '" fill="#d9c79a"/>'
    for lon, lat in DOTS:
        x, y = xy(lon, lat)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="#9fb4c8" stroke="#20364a" stroke-width="0.8"/>'
    rof = {n: r for n, r in ALL}
    for n, (lon, lat) in PINS.items():
        x, y = xy(lon, lat); dx, dy = NUDGE.get(n, (0, 0)); x += dx; y += dy
        s += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{REG[rof[n]]}" stroke="#fff" stroke-width="1.2"/>'
              f'<text x="{x:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8" fill="#fff">{n}</text>')
    return s + '</svg>'

# --- page -------------------------------------------------------------------------------------------
e = html.escape
def card(st, cls):
    n, reg, kick, head, body = st
    b = f'<p>{e(body)}</p>' if body else ''
    return (f'<div class="card {cls}" style="border-top-color:{REG[reg]}">{art(n)}<div class="tx">'
            f'<div class="kick" style="color:{REG[reg]}"><b class="n" style="background:{REG[reg]}">{n}</b>{e(kick)}</div>'
            f'<h2>{e(head)}</h2>{b}</div></div>')

bar = ''.join(f'<span style="background:{REG[r]};flex:{max(COUNT[r], 2.6)}">{r} {COUNT[r]}</span>' for r in REG)
nums = ''.join(f'<div><b>{e(a)}</b><i>{e(b)}</i></div>' for a, b in NUMS)
briefs = ''.join(f'<p><b style="color:{REG[r]}">{e(place)}</b> — {e(t)}</p>' for n, r, place, t in BRIEFS)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1024px;height:1024px;background:#f6f1e4;color:#161412;font-family:Inter,sans-serif;overflow:hidden}
.pg{position:absolute;inset:0;padding:10px 16px 8px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-size:11px;font-weight:800;letter-spacing:2.2px;border-bottom:3px solid #161412;padding-bottom:3px}
.top span:first-child{color:#8f3a32}
h1{font-family:'Bitstream Charter',Charter,Georgia,serif;font-weight:700;font-size:54px;line-height:58px;letter-spacing:-1.6px;margin-top:0;white-space:nowrap}
.deck{font-family:'Bitstream Charter',Charter,Georgia,serif;font-style:italic;font-size:16px;color:#6e3129;margin:1px 0 4px}
.bar{display:flex;height:14px;font-size:9.3px;font-weight:800;letter-spacing:.6px;color:#fff}
.bar span{display:flex;align-items:center;justify-content:center;white-space:nowrap}
.nums{display:grid;grid-template-columns:repeat(6,1fr);border-bottom:2px solid #161412;padding:2px 0 2px;margin-bottom:4px}
.nums div{text-align:center;padding:0 6px;border-left:1px solid #b9b1a0}
.nums div:first-child{border-left:0}
.nums b{display:block;font-family:'Bitstream Charter',Charter,Georgia,serif;font-size:18px;line-height:19px;color:#6e3129}
.nums i{display:block;font-style:normal;font-size:9px;line-height:10.2px;color:#3d3832}
.row{display:grid;gap:5px;margin-bottom:4px}
.r3{grid-template-columns:repeat(3,1fr)}
.r4{grid-template-columns:repeat(4,1fr)}
.card{background:#fffdf7;border:1px solid #b9b1a0;border-top:3px solid;overflow:hidden}
.art{display:block;width:100%}
.hero .art{height:48px}
.sm .art{height:28px}
.tx{padding:2px 8px 4px}
.kick{font-size:9.6px;font-weight:800;letter-spacing:1.1px;display:flex;align-items:center;gap:5px;white-space:nowrap}
.n{display:inline-flex;align-items:center;justify-content:center;min-width:16px;height:16px;border-radius:8px;color:#fff;font-size:10px;letter-spacing:0;padding:0 3px}
h2{font-family:'Bitstream Charter',Charter,Georgia,serif;font-weight:700;letter-spacing:-.2px}
.hero h2{font-size:21.5px;line-height:23px;margin:2px 0 2px}
.hero p{font-size:11.6px;line-height:14.2px;color:#2a2622}
.sm h2{font-size:17px;line-height:18.4px;margin:1px 0 1px}
.bot{display:grid;grid-template-columns:286px 1fr;gap:10px;flex:1;min-height:0}
.map{background:#20364a;display:flex;flex-direction:column}
.map h3{color:#fff;font-size:10.2px;letter-spacing:1.8px;font-weight:800;padding:4px 8px 2px}
.map small{color:#c9d6e2;font-size:9.2px;line-height:11.2px;padding:2px 8px 6px;display:block}
.br h3{font-size:10.2px;letter-spacing:1.6px;font-weight:800;color:#6e3129;border-bottom:1.5px solid #161412;padding-bottom:2px;margin-bottom:3px}
.cols{column-count:3;column-gap:11px}
.cols p{font-size:9.9px;line-height:11.8px;margin-bottom:2px;break-inside:avoid}
.cols b{font-weight:800;letter-spacing:.2px}
.chk{border:2px solid #6e3129;background:#fffdf7;font-size:9.6px;line-height:11.8px;padding:3px 8px;margin-top:4px}
.chk b{color:#6e3129;letter-spacing:1px}
.ft{font-size:8.8px;line-height:10.6px;color:#4a443d;margin-top:2px;white-space:nowrap}"""

total = len(ALL)
PAGE = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg">
<div class="top"><span>THE WORLD IN ONE DAY</span><span>{total} STORIES · 6 REGIONS · ONE PAGE</span></div>
<h1>Thursday 19 November 2026</h1>
<div class="deck">Three rivals at one table · A state found guilty of genocide · The biggest stock-market debut on record</div>
<div class="bar">{bar}</div>
<div class="nums">{nums}</div>
<div class="row r3">{''.join(card(s, 'hero') for s in HERO)}</div>
<div class="row r4">{''.join(card(s, 'sm') for s in CARDS[:4])}</div>
<div class="row r4">{''.join(card(s, 'sm') for s in CARDS[4:8])}</div>
<div class="row r4">{''.join(card(s, 'sm') for s in CARDS[8:])}</div>
<div class="bot"><div class="map"><h3>WHERE IT HAPPENED</h3>{worldmap()}<small>Pins match the numbered cards; grey dots mark briefs.</small></div>
<div class="br"><h3>ALSO ON THURSDAY 19 NOVEMBER — {len(BRIEFS)} MORE STORIES</h3><div class="cols">{briefs}</div></div></div>
<div class="chk"><b>DATE CHECK</b> — Reported on Wednesday 18 November, so not counted as Thursday’s news: Trump’s arrival and the banquet handshake in Shenzhen · Anthropic setting its $83 price · House Democrats nominating Jeffries for Speaker · GTA VI going on sale (its first-day sales were counted today) · Pew’s forecast on Islam by 2035.</div>
<div class="ft"><b>Every story above happened, or was first reported, on Thursday 19 November 2026.</b> Claims are attributed. Sources: Reuters, AP, The Guardian, NYT, Bloomberg, Al Jazeera, Euronews, Xinhua, The Hindu, IPS. Original drawings.</div>
</div></body></html>"""
open(sys.argv[1], 'w', encoding='utf-8').write(PAGE)
print('ok', COUNT, 'total', total)
