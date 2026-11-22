#!/usr/bin/env python3
"""news-image-20261122 entry r5: one broadsheet image summing up
Sunday 22 November 2026 in 35 stories. Drawn from scratch with PIL.

Layout: kicker + date headline + sub-headline + THE DAY IN UTC timeline
+ 6-number strip + region bar + 3 hero stories + 10 illustrated panels
+ world map + 22-story list + DATE CHECK + footer. 1024x1024, under 1 MiB.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 14
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (247, 242, 228)
INK = (22, 22, 22)
RED = (176, 30, 30)
RED_DARK = (138, 20, 20)
GREY = (105, 105, 105)
RULE = (70, 70, 70)
CARD_BG = (255, 253, 248)
SKY_DAY = (176, 212, 234)
SEA_BLUE = (54, 108, 164)
NIGHT_BLUE = (20, 32, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap_text(text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_lines(draw, x, y, lines, fnt, fill=INK, gap=None, limit=None):
    """Draw lines top-down; return the y just below the last line drawn."""
    step = gap if gap is not None else int(fnt.size * 1.28)
    if limit is not None:
        lines = lines[:limit]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def number_tag(draw, x, y, w, num, label, height=15):
    """Red tag: white story number + white dateline label."""
    draw.rectangle([x, y, x + w, y + height], fill=RED)
    draw.text((x + 4, y + 1), str(num), font=sans_b(10), fill=(255, 255, 255))
    draw.text((x + 22, y + 2), label, font=sans_b(8), fill=(255, 255, 255))


def frame(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=(95, 95, 95), width=1)


# ------------------------------------------------------------------ pictures

def scene_hormuz(draw, x, y, w, h):
    """Strait of Hormuz in daylight: coast, strait, two tankers, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_DAY)
    draw.ellipse([x + w - 50, y + 6, x + w - 20, y + 36],
                 fill=(250, 224, 138))
    sea_y = y + int(h * 0.55)
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA_BLUE)
    for wy in (sea_y + 11, sea_y + 25, sea_y + 38):
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(150, 196, 224),
                  width=2)
    # Khasab headland on the right, with its label
    draw.polygon([(x + w - 100, sea_y), (x + w - 66, y + 24),
                  (x + w - 34, y + 42), (x + w, y + 38), (x + w, sea_y)],
                 fill=(148, 126, 90))
    draw.polygon([(x + w - 66, y + 24), (x + w - 34, y + 42),
                  (x + w - 48, sea_y), (x + w - 100, sea_y)],
                 fill=(120, 100, 70))
    draw.text((x + w - 104, y + 6), "KHASAB", font=sans_b(8), fill=INK)
    # tanker one, left, stern struck
    deck = sea_y + 6
    draw.rectangle([x + 12, deck, x + 148, deck + 17], fill=(94, 54, 40))
    draw.rectangle([x + 110, deck - 13, x + 136, deck], fill=(232, 232, 232))
    draw.rectangle([x + 18, deck - 7, x + 42, deck], fill=(212, 212, 212))
    # tanker two, right, engine room struck
    x2 = x + w - 152
    draw.rectangle([x2, deck + 5, x2 + 130, deck + 21], fill=(72, 46, 36))
    draw.rectangle([x2 + 90, deck - 7, x2 + 114, deck + 5],
                   fill=(226, 226, 226))
    # smoke over both hits
    for cx, cy, r in ((x + 38, y + 24, 12), (x + 56, y + 14, 9),
                      (x2 + 102, y + 28, 11), (x2 + 118, y + 16, 8)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(118, 118, 118))
        draw.ellipse([cx - r + 4, cy - r + 3, cx + r - 2, cy + r - 4],
                     fill=(152, 152, 152))
    # dashed line marking the strait
    for xx in range(x + 6, x + w - 6, 15):
        draw.line([(xx, sea_y - 5), (xx + 8, sea_y - 5)], fill=(40, 40, 40),
                  width=2)


def scene_cop31(draw, x, y, w, h):
    """COP31: globe, rising thermometer, clock, NEW TEXT document."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 224, 238))
    gx, gy, gr = x + 50, y + 50, 38
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(72, 138, 198))
    draw.ellipse([gx - 24, gy - 28, gx + 2, gy - 4], fill=(98, 174, 98))
    draw.ellipse([gx - 4, gy + 10, gx + 24, gy + 28], fill=(98, 174, 98))
    draw.ellipse([gx - 32, gy - 32, gx - 6, gy - 10], fill=(142, 198, 142))
    # thermometer
    tx = x + 126
    draw.rounded_rectangle([tx, y + 12, tx + 14, y + 72], radius=7,
                           fill=(242, 242, 242), outline=RED, width=2)
    draw.ellipse([tx - 6, y + 64, tx + 20, y + 90], fill=RED)
    draw.rectangle([tx + 4, y + 38, tx + 10, y + 70], fill=RED)
    # clock showing 05:30
    cx, cy, cr = x + 176, y + 44, 23
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                 fill=(255, 255, 255), outline=INK, width=2)
    draw.line([(cx, cy), (cx, cy - 14)], fill=INK, width=2)
    draw.line([(cx, cy), (cx + 11, cy + 5)], fill=INK, width=2)
    draw.text((cx - 20, cy + 25), "05:30 GMT", font=sans_b(9), fill=INK)
    # the new text document
    dx = x + 220
    draw.rectangle([dx, y + 10, dx + 80, y + 86], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.text((dx + 8, y + 2), "NEW TEXT", font=sans_b(10), fill=RED)
    for ly in range(y + 22, y + 78, 9):
        draw.line([(dx + 8, ly), (dx + 72, ly)], fill=(122, 122, 122),
                  width=2)


def scene_baltic(draw, x, y, w, h):
    """Baltic at night: moon, burning cargo ship, flames, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=NIGHT_BLUE)
    draw.ellipse([x + w - 46, y + 8, x + w - 16, y + 38],
                 fill=(238, 230, 190))
    for sx, sy in ((x + 28, y + 12), (x + 88, y + 24), (x + 148, y + 10),
                   (x + 208, y + 28), (x + 258, y + 14)):
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    sea_y = y + int(h * 0.60)
    draw.rectangle([x, sea_y, x + w, y + h], fill=(26, 54, 90))
    for wy in (sea_y + 11, sea_y + 25):
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(92, 132, 182),
                  width=2)
    # ship silhouette
    draw.rectangle([x + 44, sea_y - 15, x + w - 58, sea_y + 3],
                   fill=(12, 12, 12))
    draw.rectangle([x + 188, sea_y - 32, x + 222, sea_y - 15],
                   fill=(12, 12, 12))
    draw.rectangle([x + 68, sea_y - 25, x + 98, sea_y - 15],
                   fill=(32, 32, 32))
    # flames licking up from the deck
    for fx, fh, col in ((x + 88, 42, (255, 140, 0)),
                        (x + 116, 56, (255, 190, 0)),
                        (x + 146, 38, (255, 140, 0)),
                        (x + 170, 28, (255, 210, 60))):
        draw.polygon([(fx, sea_y - 15), (fx + 13, sea_y - 15 - fh),
                      (fx + 26, sea_y - 15)], fill=col)
    # smoke drifting above the fire
    for cx, cy, r in ((x + 128, y + 20, 10), (x + 150, y + 10, 8),
                      (x + 108, y + 28, 8)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(112, 112, 112))


def scene_panel(draw, x, y, w, h, kind):
    """Small literal scene for one panel, keyed by `kind`."""
    if kind == "bahrain":  # night skyline, fire at an industrial site
        draw.rectangle([x, y, x + w, y + h], fill=(26, 30, 54))
        for bx, bw, bh in ((8, 26, 26), (44, 34, 38), (88, 26, 22),
                           (124, 34, 32), (164, 22, 26)):
            draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                           fill=(54, 58, 86))
            for wy in range(y + h - bh + 5, y + h - 4, 8):
                draw.rectangle([x + bx + 5, wy, x + bx + 10, wy + 4],
                               fill=(250, 210, 90))
        for fx, fh in ((52, 18), (66, 26), (80, 15)):
            draw.polygon([(x + fx, y + h - 38),
                          (x + fx + 8, y + h - 38 - fh),
                          (x + fx + 16, y + h - 38)], fill=(255, 150, 0))
    elif kind == "tehran":  # pylon and a lightning bolt
        draw.rectangle([x, y, x + w, y + h], fill=(88, 62, 40))
        draw.line([(x + 40, y + h), (x + 58, y + 6), (x + 76, y + h)],
                  fill=(30, 30, 30), width=3)
        draw.line([(x + 30, y + 22), (x + 86, y + 22)], fill=(30, 30, 30),
                  width=3)
        draw.polygon([(x + 128, y + 6), (x + 112, y + 30), (x + 124, y + 30),
                      (x + 108, y + 52), (x + 138, y + 24), (x + 126, y + 24)],
                     fill=(255, 220, 0))
    elif kind == "warsaw":  # hall with flags
        draw.rectangle([x, y, x + w, y + h], fill=(48, 84, 150))
        draw.rectangle([x + 20, y + 26, x + w - 20, y + h],
                       fill=(210, 205, 190))
        for fx in (36, 84, 132):
            draw.line([(x + fx, y + 8), (x + fx, y + 30)],
                      fill=(255, 255, 255), width=2)
            draw.polygon([(x + fx, y + 8), (x + fx + 20, y + 13),
                          (x + fx, y + 18)], fill=(200, 40, 40))
        draw.rectangle([x + 60, y + 34, x + 100, y + h], fill=(120, 110, 96))
    elif kind == "leningrad":  # drone and a blast
        draw.rectangle([x, y, x + w, y + h], fill=(96, 44, 32))
        dx, dy = x + 52, y + 22
        draw.ellipse([dx - 12, dy - 5, dx + 12, dy + 5], fill=(30, 30, 30))
        draw.line([(dx - 22, dy - 8), (dx + 22, dy - 8)], fill=(30, 30, 30),
                  width=2)
        draw.line([(dx - 22, dy + 8), (dx + 22, dy + 8)], fill=(30, 30, 30),
                  width=2)
        ex, ey = x + 140, y + 32
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            draw.line([(ex, ey), (ex + int(22 * math.cos(a)),
                                  ey + int(22 * math.sin(a)))],
                      fill=(255, 200, 0), width=3)
        draw.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 220, 80))
    elif kind == "gaza":  # aid van on a road
        draw.rectangle([x, y, x + w, y + h], fill=(196, 172, 128))
        draw.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 90, 90))
        draw.rectangle([x + 40, y + 12, x + 150, y + 34],
                       fill=(240, 240, 240), outline=INK, width=2)
        draw.rectangle([x + 150, y + 18, x + 176, y + 34], fill=(200, 60, 60))
        for wx in (62, 92, 158):
            draw.ellipse([x + wx, y + 32, x + wx + 12, y + 44],
                         fill=(20, 20, 20))
        draw.text((x + 48, y + 18), "AID", font=sans_b(11), fill=RED)
    elif kind == "sinaloa":  # street arrest: police car, banner, figures
        draw.rectangle([x, y, x + w, y + h], fill=(150, 150, 148))
        draw.rectangle([x, y + h - 18, x + w, y + h], fill=(70, 70, 70))
        for wx in range(x + 6, x + w - 6, 18):
            draw.line([(wx, y + h - 9), (wx + 9, y + h - 9)],
                      fill=(255, 220, 0), width=2)
        draw.rectangle([x + 56, y + 22, x + 150, y + 40],
                       fill=(245, 245, 245), outline=INK, width=2)
        draw.rectangle([x + 76, y + 12, x + 128, y + 22],
                       fill=(200, 220, 240), outline=INK, width=1)
        draw.rectangle([x + 96, y + 8, x + 112, y + 12], fill=(30, 90, 200))
        for wx in (72, 128):
            draw.ellipse([x + wx, y + 38, x + wx + 12, y + 50],
                         fill=(20, 20, 20))
        draw.rectangle([x + 8, y + 2, x + 118, y + 14], fill=RED)
        draw.text((x + 12, y + 3), "CAPTURED", font=sans_b(9),
                  fill=(255, 255, 255))
        for fx in (160, 178):
            draw.ellipse([x + fx, y + 18, x + fx + 8, y + 26],
                         fill=(40, 40, 40))
            draw.rectangle([x + fx - 1, y + 27, x + fx + 9, y + 44],
                           fill=(40, 60, 120))
    elif kind == "fbi":  # headquarters block with FBI letters
        draw.rectangle([x, y, x + w, y + h], fill=(28, 44, 84))
        draw.rectangle([x + 56, y + 10, x + 140, y + h], fill=(200, 200, 205))
        for r in range(3):
            for c in range(4):
                draw.rectangle([x + 64 + c * 19, y + 16 + r * 11,
                                x + 74 + c * 19, y + 24 + r * 11],
                               fill=(255, 220, 90))
        draw.rectangle([x + 56, y + 38, x + 140, y + 50],
                       fill=(255, 255, 255))
        draw.text((x + 76, y + 39), "FBI", font=sans_b(11),
                  fill=(20, 20, 120))
    elif kind == "kordofan":  # dirt road and a tuk-tuk
        draw.rectangle([x, y, x + w, y + h], fill=(168, 128, 84))
        draw.polygon([(x + 20, y + h), (x + 90, y), (x + 130, y),
                      (x + 80, y + h)], fill=(120, 88, 54))
        draw.rectangle([x + 78, y + 16, x + 128, y + 34], fill=(40, 120, 90))
        draw.rectangle([x + 128, y + 22, x + 148, y + 34], fill=(40, 120, 90))
        for wx in (88, 134):
            draw.ellipse([x + wx, y + 32, x + wx + 11, y + 43],
                         fill=(20, 20, 20))
    elif kind == "nigeria":  # river, overturned hull, rescue boat
        draw.rectangle([x, y, x + w, y + h], fill=(120, 168, 190))
        draw.rectangle([x, y + 22, x + w, y + h], fill=(44, 96, 140))
        for wy in (y + 30, y + 40):
            draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(140, 190, 220),
                      width=2)
        # overturned hull, keel up
        draw.polygon([(x + 30, y + 30), (x + 110, y + 30), (x + 96, y + 44),
                      (x + 44, y + 44)], fill=(120, 70, 40))
        draw.rectangle([x + 58, y + 24, x + 82, y + 30], fill=(90, 50, 30))
        # rescue boat coming in from the right
        draw.polygon([(x + 128, y + 34), (x + 184, y + 34), (x + 174, y + 46),
                      (x + 138, y + 46)], fill=(240, 240, 240))
        draw.rectangle([x + 146, y + 24, x + 168, y + 34], fill=(200, 60, 60))
        # figures in the water
        for fx in (118, 126):
            draw.ellipse([x + fx, y + 38, x + fx + 7, y + 45],
                         fill=(240, 200, 160))
    elif kind == "vegas":  # night skyline and a chequered flag
        draw.rectangle([x, y, x + w, y + h], fill=(16, 16, 40))
        for bx, bw, bh in ((10, 22, 24), (38, 18, 34), (62, 26, 20),
                           (94, 20, 38), (120, 24, 26), (150, 20, 32)):
            draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                           fill=(70, 70, 110))
            for wy in range(y + h - bh + 4, y + h - 3, 8):
                draw.rectangle([x + bx + 4, wy, x + bx + 8, wy + 4],
                               fill=(255, 210, 90))
        for r in range(3):
            for c in range(4):
                col = (255, 255, 255) if (r + c) % 2 == 0 else (0, 0, 0)
                draw.rectangle([x + 158 + c * 8, y + 4 + r * 8,
                                x + 166 + c * 8, y + 12 + r * 8], fill=col,
                               outline=(200, 200, 200), width=1)

# ------------------------------------------------------------------ content

TIMELINE = [
    ("01:58", "Bitcoin $60,112"),
    ("03:00", "COP31 objections close"),
    ("04:00", "Vegas lights out"),
    ("06:00", "COP31 approval opens"),
    ("16:30", "Liverpool v United"),
    ("17:00", "ATP final, Turin"),
    ("All day", "Hong Kong polls open"),
]

NUMBERS = [
    ("856", "CANDIDATES IN HONG KONG VOTE", "Reuters"),
    ("2", "TANKERS HIT LEAVING HORMUZ", "UKMTO"),
    ("16", "CREW OFF BURNING RUSSIAN SHIP", "Finland"),
    ("4.1 km", "RUSSIAN HELICOPTER INTO FINLAND", "MoD"),
    ("1,671", "KILLED IN GAZA SINCE 2025 TRUCE", "ministry"),
    ("22", "KILLED BY LANDMINE IN N. KORDOFAN", "Darfur24"),
]

HEROES = [
    dict(num=1, label="STRAIT OF HORMUZ \u00b7 IRAN WAR", scene="hormuz",
         head="Tankers hit in the Strait of Hormuz as Iran squeezes shipping",
         body=("TORKEL struck at 0500 UTC, 11 nm north of Khasab; ARINA hit "
               "at 0550 UTC. No casualties."),
         src="UKMTO \u00b7 Al Jazeera"),
    dict(num=2, label="ANTALYA, TURKEY \u00b7 CLIMATE", scene="cop31",
         head="COP31 closes in on a deal as new text goes to ~200 nations",
         body=("Objections due 03:00 GMT, approval session opens 06:00 GMT. "
               "Not yet adopted when drawn."),
         src="Reuters"),
    dict(num=3, label="GULF OF FINLAND \u00b7 UKRAINE WAR", scene="baltic",
         head="Russian cargo ship still burning in the Baltic after drone strike",
         body=("The fire burns on Sunday; all 16 crew were taken off. "
               "Finland says Ukraine \u2018likely\u2019 behind the strike."),
         src="Finnish Defence Forces \u00b7 Reuters"),
]

PANELS = [
    dict(num=4, label="SITRA, BAHRAIN \u00b7 IRAN WAR", scene="bahrain",
         head="Bahrain says Iranian strike set an industrial site ablaze",
         body="No injuries reported.", src="Bahrain govt, Reuters"),
    dict(num=5, label="TEHRAN \u00b7 ENERGY", scene="tehran",
         head="Iran starts rationing electricity from Sunday",
         body="Two-hour daily cuts as gas output falls.",
         src="Tavnir, RFE/RL"),
    dict(num=6, label="WARSAW \u00b7 NATO", scene="warsaw",
         head="Rutte in Warsaw: all of NATO stands with Poland",
         body="After Friday\u2019s missile incursion.",
         src="TVP World, AFP"),
    dict(num=7, label="LENINGRAD REGION \u00b7 WAR", scene="leningrad",
         head="Ukrainian drones hit Russia\u2019s Leningrad region",
         body="A Russian warship was hit nearby.",
         src="RTE, Reuters"),
    dict(num=8, label="GAZA CITY \u00b7 CEASEFIRE", scene="gaza",
         head="Drone strike on Gaza food-aid van kills three",
         body="IDF: it hit Islamic Jihad members.",
         src="Al Jazeera, Gaza ministry"),
    dict(num=9, label="SINALOA, MEXICO \u00b7 CRIME", scene="sinaloa",
         head="Mexico captures cartel boss \u2018El Chapo Isidro\u2019",
         body="Two other gang leaders also taken.",
         src="Reuters"),
    dict(num=10, label="WASHINGTON \u00b7 CYBER", scene="fbi",
         head="FBI probes reported hack of crime database",
         body="Intrusion into the NCIC police hub.",
         src="Reuters"),
    dict(num=11, label="NORTH KORDOFAN \u00b7 SUDAN WAR", scene="kordofan",
         head="Landmine kills 22 on a road to El-Obeid",
         body="Women and children among the dead.",
         src="Darfur24"),
    dict(num=12, label="BAYELSA, NIGERIA \u00b7 DISASTER", scene="nigeria",
         head="Mourners\u2019 boat capsizes in Bayelsa, 24 dead",
         body="NEMA: 24 bodies recovered.",
         src="DW, NEMA"),
    dict(num=13, label="LAS VEGAS \u00b7 FORMULA 1", scene="vegas",
         head="Verstappen on pole as Vegas races under lights",
         body="Antonelli dropped five places.",
         src="F1"),
]

# (number, place, text, source, region) — regions drive the bar and pins
REST = [
    (14, "Doha", "Iran talks to Qatari mediators; Trump wants a \u201cpermanent\u201d deal", "AJ", "ME"),
    (15, "Jerusalem", "Eisenkot invites Likud to coalition talks", "Straits Times", "ME"),
    (16, "Gulf", "US denies Iran hit on F-16; all jets accounted for", "CENTCOM", "ME"),
    (17, "New Delhi", "Nepal PM Shah lands in Delhi on first state visit", "IANS", "AS"),
    (18, "Hong Kong", "Voting opens for the Election Committee", "Reuters", "AS"),
    (19, "Washington", "US airlines warned of a plot ahead of Thanksgiving", "officials", "AM"),
    (20, "Tallinn", "Estonia to shut its Russia border from 1 Dec", "Reuters", "EU"),
    (21, "Wellington", "Pant\u2019s 128 takes India to 629 for six", "Reuters", "OC"),
    (22, "Washington", "Nvidia faces SEC probe over its accounting", "Reuters", "AM"),
    (23, "Canberra", "Marles rejects US report on AUKUS subs", "ABC", "OC"),
    (24, "DR Congo", "Cantine, 40 killed", "local officials", "AF"),
    (25, "Geneva", "UN robot-weapons talks end with no binding rules", "AP", "GL"),
    (26, "Helsinki", "Russian helicopter 4.1 km into Finland airspace", "MoD", "EU"),
    (27, "Palawan", "Philippines M5.9 quake, 688 km deep", "EMSC", "AS"),
    (28, "Tokyo", "Japan poll \u2014 record 92% feel friendly to S. Korea", "JKN", "AS"),
    (29, "Melbourne", "Australia chase 188 to beat England in 1st T20", "ABC", "OC"),
    (30, "Washington", "Trump shares senator-elect\u2019s \u201cTrumpCare\u201d plan", "AP", "AM"),
    (31, "Finland", "Finland seeks \u20ac25bn from Russia and Gazprom", "Ukrinform", "EU"),
    (32, "Poland", "Swedish Gripen cleared to down Russian missile, held fire", "Kyiv Independent", "EU"),
    (33, "London", "UK and Ukraine sign drone-production deals", "UK MoD", "EU"),
    (34, "Brussels", "EU approves \u20ac1bn military aid for Ukraine", "EU", "EU"),
    (35, "Paris", "France calls UN meeting on strikes on Kyiv embassies", "France", "GL"),
]

REGION_OF_STORY = {
    1: "ME", 2: "GL", 3: "EU", 4: "ME", 5: "ME", 6: "EU", 7: "EU",
    8: "ME", 9: "AM", 10: "AM", 11: "AF", 12: "AF", 13: "AM",
}
for _n, _p, _t, _s, _r in REST:
    REGION_OF_STORY[_n] = _r

REGION_ORDER = [
    ("EUROPE", "EU", (47, 95, 179)),
    ("MIDDLE EAST", "ME", (179, 57, 46)),
    ("AMERICAS", "AM", (122, 79, 163)),
    ("ASIA", "AS", (61, 139, 79)),
    ("AFRICA", "AF", (208, 127, 31)),
    ("OCEANIA", "OC", (42, 138, 138)),
    ("GLOBAL", "GL", (119, 119, 119)),
]
REGION_COLOUR = {code: col for _name, code, col in REGION_ORDER}

# lon/lat pins for the pictured stories and a few list ones
PINS = {
    1: (56, 26), 2: (30, 36), 3: (24, 59), 4: (50, 26), 5: (51, 35),
    6: (21, 52), 7: (30, 59), 8: (34, 31), 9: (-107, 24), 10: (-77, 38),
    11: (30, 13), 12: (6, 5), 13: (-115, 36), 20: (24, 59),
    25: (6, 46), 26: (24, 60), 31: (25, 61), 32: (19, 52),
}
PIN_SHIFT = {1: (0, 12), 4: (-14, -8), 5: (12, -10), 8: (-14, 8),
             2: (12, 8), 3: (-14, -8), 7: (14, -8), 20: (-14, 10),
             26: (12, 10), 31: (-12, -8), 32: (12, 8), 25: (0, -12),
             6: (0, -10), 12: (-10, 0)}

DATE_CHECK = ("Wires read up to 05:00 UTC, Sunday 22 November 2026. Left out "
              "on purpose, first reported Friday or Saturday, so NOT shown as "
              "Sunday\u2019s news: Peru quake (Sat 21 Nov) \u00b7 400-drone "
              "barrage (19\u201320 Nov) \u00b7 Shenzhen summit (19 Nov) \u00b7 ADNOC "
              "tanker (Tue 17 Nov) \u00b7 Russian missiles landing in Poland "
              "(Fri 20 Nov). Not yet happened: COP31\u2019s final approval, the "
              "ATP champion, the Vegas winner. Every story here happened, or "
              "was first reported, on Sunday 22 November 2026 in at least one "
              "time zone. Officials\u2019 counts and claims are attributed.")

FOOTER = ("Every story here happened, or was first reported, on Sunday "
          "22 November 2026 in at least one time zone. Counts and claims "
          "are attributed.")
FOOTER2 = "Sources named beside each story \u00b7 original drawings"


# ------------------------------------------------------------------ map

CONTINENTS = [
    # North America
    [(-166, 68), (-150, 70), (-130, 71), (-110, 73), (-90, 74), (-75, 72),
     (-68, 62), (-75, 48), (-76, 38), (-81, 31), (-90, 20), (-96, 16),
     (-104, 21), (-114, 28), (-122, 38), (-124, 48), (-150, 60)],
    # South America
    [(-79, 9), (-62, 9), (-51, 4), (-41, -3), (-35, -8), (-39, -17),
     (-48, -26), (-57, -34), (-64, -42), (-68, -50), (-72, -44),
     (-73, -30), (-77, -12), (-80, -4)],
    # Asia
    [(42, 68), (62, 70), (82, 73), (104, 77), (128, 72), (158, 69),
     (178, 65), (162, 60), (156, 51), (141, 45), (135, 35), (126, 38),
     (122, 31), (120, 24), (109, 18), (106, 9), (103, 2), (99, 8),
     (94, 16), (89, 22), (85, 20), (80, 13), (77, 8), (73, 19),
     (66, 25), (61, 25), (56, 26), (51, 28), (48, 30), (44, 29),
     (42, 36), (40, 42), (38, 52), (42, 68)],
    # Europe
    [(-10, 36), (-9, 43), (0, 44), (4, 52), (8, 57), (18, 56),
     (21, 55), (24, 59), (30, 60), (32, 70), (40, 68), (44, 60),
     (40, 50), (35, 45), (30, 43), (28, 39), (23, 36), (19, 41),
     (12, 44), (3, 43), (-2, 37)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (36, -19), (32, -27), (26, -34),
     (19, -33), (13, -17), (9, -2), (9, 4), (-8, 5), (-15, 12),
     (-17, 15), (-16, 21), (-11, 30)],
    # Australia
    [(114, -22), (114, -31), (124, -33), (130, -32), (137, -35),
     (142, -38), (147, -39), (150, -37), (153, -31), (153, -27),
     (146, -19), (142, -15), (141, -12), (136, -12), (132, -11),
     (126, -14), (122, -17), (114, -22)],
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(210, 228, 238),
                   outline=(90, 90, 90), width=1)

    def to_px(lon, lat):
        return (x + (lon + 180) / 360.0 * w,
                y + (85 - lat) / 145.0 * h)

    for poly in CONTINENTS:
        draw.polygon([to_px(lo, la) for lo, la in poly],
                     fill=(232, 222, 190), outline=(180, 168, 140))
    for num, (lon, lat) in sorted(PINS.items()):
        cx, cy = to_px(lon, lat)
        dx, dy = PIN_SHIFT.get(num, (0, 0))
        cx, cy = cx + dx, cy + dy
        r = 8
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=REGION_COLOUR[REGION_OF_STORY[num]],
                     outline=(255, 255, 255), width=1)
        lab = str(num)
        tw = sans_b(7).getlength(lab)
        draw.text((cx - tw / 2, cy - 5), lab, font=sans_b(7),
                  fill=(255, 255, 255))


def section_title(draw, x, y, text):
    draw.text((x, y), text, font=sans_b(12), fill=RED)
    return y + 16


# ------------------------------------------------------------------ compose

def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = MARGIN + CONTENT_W

    # kicker
    draw.text((x0, 10), "THE WORLD IN ONE DAY", font=sans_b(14), fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 AS REPORTED ON SUNDAY 22 NOVEMBER 2026"
    draw.text((x1 - sans_b(11).getlength(right), 12), right,
              font=sans_b(11), fill=INK)
    rule(draw, x0, x1, 30)

    # headline + sub-headline
    draw.text((x0, 33), "Sunday 22 November 2026", font=serif_b(50), fill=INK)
    sub = ("Tankers hit in the Strait of Hormuz \u00b7 COP31 nears a deal in "
           "Antalya \u00b7 Russian ship ablaze in the Baltic \u00b7 Iran starts "
           "rationing power")
    draw.text((x0, 92), sub, font=sans(12), fill=INK)

    # THE DAY IN UTC timeline strip
    ty, th = 110, 32
    draw.rectangle([x0, ty, x1, ty + th], outline=(90, 90, 90), width=1)
    draw.text((x0 + 6, ty + 2), "THE DAY IN UTC", font=sans_b(10), fill=RED)
    slot_w = (CONTENT_W - 118) / 7
    for i, (when, what) in enumerate(TIMELINE):
        sx = x0 + 118 + i * slot_w
        if i:
            draw.line([(sx - 4, ty + 4), (sx - 4, ty + th - 4)],
                      fill=(180, 180, 180), width=1)
        draw.text((sx, ty + 2), when, font=sans_b(10), fill=RED)
        lines = wrap_text(what, sans(8), slot_w - 8)
        draw_lines(draw, sx, ty + 15, lines, sans(8), gap=10, limit=2)

    # number strip
    ny, nh = 146, 54
    gap = 4
    bw = (CONTENT_W - gap * 5) // 6
    for i, (num, cap, src) in enumerate(NUMBERS):
        bx = x0 + i * (bw + gap)
        blw = x1 - bx if i == 5 else bw
        draw.rectangle([bx, ny, bx + blw, ny + nh], outline=(90, 90, 90),
                       width=1)
        draw.text((bx + 6, ny + 2), num, font=sans_b(22), fill=RED)
        cap_lines = wrap_text(cap, sans_b(9), blw - 12)
        draw_lines(draw, bx + 6, ny + 29, cap_lines, sans_b(9), gap=11,
                   limit=2)
        sw = sans(8).getlength(src)
        draw.text((bx + blw - sw - 5, ny + nh - 12), src, font=sans(8),
                  fill=GREY)

    # region bar: widths from the real story counts, must total 35
    counts = {}
    for code in REGION_OF_STORY.values():
        counts[code] = counts.get(code, 0) + 1
    assert sum(counts.values()) == 35, counts
    ry, rh = 204, 18
    rx = x0
    for idx, (name, code, col) in enumerate(REGION_ORDER):
        n = counts.get(code, 0)
        if idx == len(REGION_ORDER) - 1:
            seg = x1 - rx
        else:
            seg = int(round(n / 35.0 * CONTENT_W))
        if rx + seg > x1:
            seg = x1 - rx
        draw.rectangle([rx, ry, rx + seg, ry + rh], fill=col)
        lab = "%s %d" % (name, n)
        tw = sans_b(10).getlength(lab)
        draw.text((rx + (seg - tw) / 2, ry + 3), lab, font=sans_b(10),
                  fill=(255, 255, 255))
        rx += seg
    assert rx == x1, (rx, x1)

    # heroes
    hy, hh = 228, 176
    hgap = 8
    hw = (CONTENT_W - hgap * 2) // 3
    scenes = {"hormuz": scene_hormuz, "cop31": scene_cop31,
              "baltic": scene_baltic}
    for i, hero in enumerate(HEROES):
        hx = x0 + i * (hw + hgap)
        hw_last = x1 - hx if i == 2 else hw
        frame(draw, hx, hy, hw_last, hh)
        scenes[hero["scene"]](draw, hx + 1, hy + 1, hw_last - 2, 86)
        number_tag(draw, hx + 1, hy + 87, hw_last - 2, hero["num"],
                   hero["label"], height=15)
        cy = hy + 106
        head_lines = wrap_text(hero["head"], sans_b(13), hw_last - 10)
        cy = draw_lines(draw, hx + 5, cy, head_lines, sans_b(13), gap=16,
                        limit=2)
        body_lines = wrap_text(hero["body"], sans(10), hw_last - 10)
        cy = draw_lines(draw, hx + 5, cy + 2, body_lines, sans(10), gap=12,
                        limit=2)
        draw.text((hx + 5, hy + hh - 13), hero["src"], font=sans(8),
                  fill=GREY)

    # panels
    py = section_title(draw, x0, 410, "MORE FROM THE DAY")
    py += 2
    pgap, prow_gap = 6, 6
    ph = 106
    pw = (CONTENT_W - pgap * 4) // 5
    for row in range(2):
        for col in range(5):
            p = PANELS[row * 5 + col]
            px0 = x0 + col * (pw + pgap)
            pw_last = x1 - px0 if col == 4 else pw
            pyy = py + row * (ph + prow_gap)
            frame(draw, px0, pyy, pw_last, ph)
            scene_panel(draw, px0 + 1, pyy + 1, pw_last - 2, 44, p["scene"])
            number_tag(draw, px0 + 1, pyy + 45, pw_last - 2, p["num"],
                       p["label"], height=13)
            cy = pyy + 61
            hl = wrap_text(p["head"], sans_b(10), pw_last - 8)
            cy = draw_lines(draw, px0 + 4, cy, hl, sans_b(10), gap=11,
                            limit=2)
            # a two-line head leaves room for one body line only; the
            # source line sits at the card's foot and must never collide
            bl = wrap_text(p["body"], sans(8), pw_last - 8)
            body_limit = 1 if len(hl) > 1 else 2
            draw_lines(draw, px0 + 4, cy + 1, bl, sans(8), gap=10,
                       limit=body_limit)
            draw.text((px0 + 4, pyy + ph - 12), p["src"], font=sans(7),
                      fill=GREY)

    # bottom: map + list
    by = py + 2 * ph + prow_gap + 8
    map_w = 316
    my = section_title(draw, x0, by, "WHERE IT HAPPENED")
    draw_map(draw, x0, my, map_w, 196)
    lx = x0 + map_w + 12
    ly = section_title(draw, lx, by,
                       "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES")
    rule(draw, lx, x1, ly + 2)
    ly += 8
    for num, place, text, src, reg in REST:
        draw.text((lx, ly), "%d." % num, font=sans_b(10), fill=RED)
        tx = lx + sans_b(10).getlength("35. ") + 2
        draw.text((tx, ly), place + ": ", font=sans_b(10), fill=INK)
        off = sans_b(10).getlength(place + ": ")
        draw.text((tx + off, ly), text, font=sans(10), fill=INK)
        tw = sans(10).getlength(text)
        draw.text((tx + off + tw + 3, ly), "(%s)" % src, font=sans(10),
                  fill=GREY)
        ly += 11
    # map legend
    leg_y = my + 196 + 6
    lx2 = x0
    for _name, code, _col in REGION_ORDER[:4]:
        draw.ellipse([lx2, leg_y, lx2 + 9, leg_y + 9],
                     fill=REGION_COLOUR[code])
        draw.text((lx2 + 12, leg_y - 1), code, font=sans_b(9), fill=INK)
        lx2 += 34
    draw.text((lx2 + 6, leg_y - 1), "numbered as the stories", font=sans(8),
              fill=GREY)

    # DATE CHECK
    dy = 926
    draw.rectangle([x0, dy, x1, dy + 46], outline=RED, width=1)
    draw.text((x0 + 5, dy + 3), "DATE CHECK", font=sans_b(10), fill=RED)
    dc_lines = wrap_text(DATE_CHECK, sans(8), CONTENT_W - 12)
    draw_lines(draw, x0 + 6, dy + 16, dc_lines, sans(8), gap=10, limit=3)

    # footer
    draw.text((x0, 978), FOOTER, font=sans(9), fill=INK)
    draw.text((x0, 990), FOOTER2, font=sans(8), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print("wrote %s %dx%d %d bytes" % (out, PAGE_W, PAGE_H, size))
    assert size <= 1024 * 1024, "entry.png over 1 MiB"
    return out


if __name__ == "__main__":
    build()
