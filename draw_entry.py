# draw_entry.py — draws the news-image-20261119 front page (1024x1024 PNG)
# with PIL. Every glyph is rendered from the strings in STORIES below;
# no external images, no network, no fonts beyond Liberation on disk.
# Run: python3 draw_entry.py  -> writes entry.png beside this file.
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (179, 32, 44)
NAVY = (31, 58, 95)
GREY = (96, 92, 82)
FAINT = (128, 124, 113)
FRAME = (58, 54, 46)
MARGIN = 34

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        elif current:
            lines.append(current)
            current = word
        else:
            lines.append(word)
            current = ""
    if current:
        lines.append(current)
    return lines


def put_lines(draw, lines, x, y, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centred(draw, text, y, font, fill):
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


# ---- pictograms, drawn with lines and shapes only -------------------------

def pic_globe(d, x, y, s, c):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.42
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=4)
    d.ellipse((cx - r * 0.45, cy - r, cx + r * 0.45, cy + r), outline=c, width=3)
    d.line((cx - r, cy, cx + r, cy), fill=c, width=3)
    d.arc((cx - r, cy - r * 0.6, cx + r, cy + r * 0.6), 0, 360, fill=c, width=3)


def pic_chart_up(d, x, y, s, c):
    ox, oy = x + 6, y + s - 8
    d.line((ox, y + 8, ox, oy), fill=c, width=4)
    d.line((ox, oy, x + s - 4, oy), fill=c, width=4)
    pts = [(ox + 4, y + 52), (ox + 20, y + 44), (ox + 34, y + 48),
           (ox + 48, y + 30), (ox + 62, y + 14)]
    d.line(pts, fill=c, width=4, joint="curve")
    d.polygon([(ox + 62, y + 14), (ox + 50, y + 14), (ox + 60, y + 26)], fill=c)


def pic_scales(d, x, y, s, c):
    cx = x + s / 2
    d.line((cx, y + 6, cx, y + s - 12), fill=c, width=4)
    d.line((x + 8, y + 16, x + s - 8, y + 16), fill=c, width=4)
    d.line((cx - 5, y + 2, cx + 5, y + 2), fill=c, width=4)
    for px in (x + 8, x + s - 8):
        d.line((px, y + 16, px - 11, y + 40), fill=c, width=3)
        d.line((px, y + 16, px + 11, y + 40), fill=c, width=3)
        d.arc((px - 13, y + 32, px + 13, y + 52), 0, 180, fill=c, width=3)
    d.line((x + 14, y + s - 8, x + s - 14, y + s - 8), fill=c, width=4)


def pic_gamepad(d, x, y, s, c):
    d.rounded_rectangle((x + 4, y + s * 0.28, x + s - 4, y + s * 0.78),
                        radius=14, outline=c, width=4)
    d.line((x + s * 0.22, y + s * 0.50, x + s * 0.36, y + s * 0.50), fill=c, width=4)
    d.line((x + s * 0.29, y + s * 0.43, x + s * 0.29, y + s * 0.57), fill=c, width=4)
    for bx, by in ((0.62, 0.46), (0.72, 0.54)):
        d.ellipse((x + s * bx - 4, y + s * by - 4, x + s * bx + 4, y + s * by + 4),
                  fill=c)


def pic_bridge(d, x, y, s, c):
    d.line((x + 4, y + s * 0.62, x + s - 4, y + s * 0.62), fill=c, width=4)
    d.arc((x + s * 0.12, y + s * 0.10, x + s * 0.88, y + s * 0.90), 180, 360,
          fill=c, width=4)
    for fx in (0.22, 0.5, 0.78):
        d.line((x + s * fx, y + s * 0.30, x + s * fx, y + s * 0.62), fill=c, width=3)
    d.line((x + s * 0.14, y + s * 0.80, x + s * 0.86, y + s * 0.80), fill=c, width=3)


def pic_barrel(d, x, y, s, c):
    d.rounded_rectangle((x + s * 0.22, y + s * 0.12, x + s * 0.78, y + s * 0.88),
                        radius=8, outline=c, width=4)
    for fy in (0.32, 0.68):
        d.line((x + s * 0.22, y + s * fy, x + s * 0.78, y + s * fy), fill=c, width=3)
    d.text((x + s * 0.42, y + s * 0.40), "$", font=load(SANS_B, 22), fill=c)


# ---- stories of Thursday 19 November 2026 --------------------------------

LEAD = {
    "kick": "DIPLOMACY  —  LEAD STORY",
    "head": ["Trump, Xi and Putin hold",
             "first-ever three-way summit"],
    "body": ("Xi Jinping hosts Donald Trump and Vladimir Putin in Shenzhen "
             "at the APEC summit. Nuclear arms and the Iran war top the "
             "agenda; with New START lapsed, no deal is expected."),
    "pic": pic_globe,
}

GRID = [
    ("MARKETS",
     "Fed minutes point",
     "to more rate hikes",
     "Minutes of the 27–28 October meeting: nearly all officials "
     "expect further rises if inflation stays hot. Markets price +25bp "
     "in December, two more by summer 2027.",
     pic_chart_up),
    ("LAW  ·  THE HAGUE",
     "World court delivers",
     "Rohingya verdict",
     "The ICJ hands down its judgment in The Gambia v. Myanmar — a "
     "seven-year case over the 2017 crackdown that drove 730,000 "
     "Rohingya into Bangladesh. The ruling is final.",
     pic_scales),
    ("CULTURE  ·  GAMES",
     "GTA VI rolls out",
     "around the world",
     "After 13 years, Rockstar's sequel launches at midnight local "
     "time — New Zealand first. Early reviews give it 99 on Metacritic; "
     "pre-orders top $1.5 billion.",
     pic_gamepad),
    ("WAR  ·  UKRAINE",
     "Crimean Bridge hit",
     "a third time",
     "Just after midnight, a fresh strike halts traffic on the Kerch "
     "Bridge — the third attack this week, days after a road span "
     "collapsed into the strait.",
     pic_bridge),
]

BAND = {
    "kick": "THE AMERICAS",
    "head": "US accounts for $12bn of Venezuelan oil money",
    "body": ("The State Department publishes a 53-page report on Venezuelan "
             "oil and mineral revenue, nearly a year after US forces captured "
             "Nicolás Maduro."),
    "pic": pic_barrel,
}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    centred(d, "ONE DAY  ·  SIX STORIES  ·  AS REPORTED ON 19 NOVEMBER 2026",
            26, load(SANS_B, 15), GREY)
    centred(d, "THE WORLD IN ONE PAGE", 48, load(SERIF_B, 56), INK)
    d.rectangle((MARGIN, 118, W - MARGIN, 122), fill=INK)
    d.rectangle((MARGIN, 126, W - MARGIN, 128), fill=RED)
    centred(d, "THURSDAY  19  NOVEMBER  2026", 138, load(SERIF_B, 38), RED)
    centred(d, "Six stories that defined the day",
            182, load(SERIF_I, 20), GREY)

    # lead story
    ly0, ly1 = 214, 392
    d.rectangle((MARGIN, ly0, W - MARGIN, ly1), outline=FRAME, width=2)
    d.rectangle((MARGIN, ly0, W - MARGIN, ly0 + 4), fill=RED)
    d.text((MARGIN + 16, ly0 + 16), LEAD["kick"], font=load(SANS_B, 16), fill=RED)
    y = ly0 + 42
    for line in LEAD["head"]:
        d.text((MARGIN + 16, y), line, font=load(SERIF_B, 33), fill=INK)
        y += 40
    body_lines = wrap_text(d, LEAD["body"], load(SANS_R, 17), 770)
    assert len(body_lines) <= 2, body_lines
    put_lines(d, body_lines, MARGIN + 16, y + 6, load(SANS_R, 17), INK, 22)
    LEAD["pic"](d, W - MARGIN - 152, ly0 + 50, 122, NAVY)

    # 2x2 grid of stories
    cw, ch, gap = 468, 190, 20
    gx, gy = MARGIN, 406
    for i, (kick, h1, h2, body, pic) in enumerate(GRID):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        d.rectangle((cx, cy, cx + cw, cy + ch), outline=FRAME, width=2)
        d.text((cx + 14, cy + 12), kick, font=load(SANS_B, 15), fill=RED)
        pic(d, cx + cw - 66, cy + 10, 54, NAVY)
        d.text((cx + 14, cy + 38), h1, font=load(SERIF_B, 27), fill=INK)
        d.text((cx + 14, cy + 70), h2, font=load(SERIF_B, 27), fill=INK)
        blines = wrap_text(d, body, load(SANS_R, 16), cw - 28)
        assert len(blines) <= 3, (kick, blines)
        put_lines(d, blines, cx + 14, cy + 104, load(SANS_R, 16), INK, 21)

    # bottom band
    by0, by1 = 814, 930
    d.rectangle((MARGIN, by0, W - MARGIN, by1), outline=FRAME, width=2)
    d.rectangle((MARGIN, by0, MARGIN + 6, by1), fill=NAVY)
    d.text((MARGIN + 18, by0 + 12), BAND["kick"], font=load(SANS_B, 15), fill=RED)
    d.text((MARGIN + 18, by0 + 36), BAND["head"], font=load(SERIF_B, 28), fill=INK)
    blines = wrap_text(d, BAND["body"], load(SANS_R, 17), W - 2 * MARGIN - 36)
    assert len(blines) <= 2, blines
    put_lines(d, blines, MARGIN + 18, by0 + 70, load(SANS_R, 17), INK, 21)
    BAND["pic"](d, W - MARGIN - 92, by0 + 12, 66, NAVY)

    # footer
    d.rectangle((MARGIN, 944, W - MARGIN, 945), fill=FRAME)
    foot = ("ALSO:  NASA briefs on Voyager 1's one-light-day milestone  •  "
            "Cyclone Akvan nears India's east coast  •  APEC leaders wrap "
            "up in Shenzhen")
    d.text((MARGIN, 954), foot, font=load(SANS_R, 14), fill=INK)
    d.text((MARGIN, 976),
           "Sources: Reuters, BBC, CNN, AP, Al Jazeera, US State Department, "
           "Federal Reserve minutes.",
           font=load(SERIF_I, 13), fill=FAINT)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
