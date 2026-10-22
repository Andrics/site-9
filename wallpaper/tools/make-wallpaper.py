#!/usr/bin/env python3
"""SITE-9 wallpaper: the "facility wall" (BUILD_SPEC.md §3 "Wallpaper").

The desktop is a riveted wall inside SITE-9. Every pixel is one of the
§3 tokens; shading and grit come from ordered (Bayer) dithering between
them, no blends or gradients. Seeded, so the same arguments give the same
image.

    make-wallpaper.py [--variant V1|V2] [--seed N] [--logo PATH] [--out PATH]
                      [--no-placard]

V1: everything. V2: calmer — no big stencil, lighter grime.
--no-placard: the wall without the placard (and so without the logo) —
the login screen's background (BUILD_SPEC.md §3 "Login screen").
Logo (optional, never in the repo): recolored to the tokens and placed in
the placard; without it the slot is a plain recessed square.
Output: an indexed PNG holding only token colors, written outside the
repo because it may contain the logo.

Not a stow package — run it from the repo. Needs Pillow (python-pillow).
"""
import argparse
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "/usr/share/fonts/OTF/DepartureMonoNerdFont-Regular.otf"
FONT_PX = 11  # DepartureMono's pixel grid: 1 font pixel = 1 screen pixel

# §3 tokens, as palette indices.
TOKENS = [
    ("panel", 0x445435), ("field", 0x303f25), ("bevel-light", 0x667359),
    ("bevel-dark", 0x1f2719), ("text", 0xcbcfc8), ("text-bright", 0xffffff),
    ("text-dim", 0x8f9a85), ("warning", 0xe6a84f), ("critical", 0xff7a5c),
]
PANEL, FIELD, LIGHT, DARK, TEXT, BRIGHT, DIM, WARN, CRIT = range(9)

# Screen layout (measured, hyprland.lua): bar y 0-29, windows 20px in from
# every edge below it, so the gaps that show around windows are
# y 30-49 (top), y 1060-1079 (bottom), x 0-19 and 1900-1919. The pipe
# sits in the top gap; the bottom gap shows plain wall (the hazard band
# from the concept was dropped — user, 2026-10-20: too distracting).
TOP_GAP = (30, 50)
PANEL_W, PANEL_H = 240, 180  # wall panels: an 8x6 grid


# --- dithering -----------------------------------------------------------

def _bayer(n):
    m = [[0]]
    while len(m) < n:
        s = len(m)
        m = [[4 * m[y % s][x % s] + [[0, 2], [3, 1]][y // s][x // s]
              for x in range(2 * s)] for y in range(2 * s)]
    return m

_B = _bayer(8)
BAYER = [[(_B[y][x] + 0.5) / 64 for x in range(8)] for y in range(8)]


def dith(x, y, density):
    """True where a pixel should take the 'ink' color at this density."""
    return density > BAYER[y & 7][x & 7]


# --- noise (value noise, seeded) -----------------------------------------

class Noise:
    """Smooth 0..1 noise: a random lattice, smoothstep-interpolated."""

    def __init__(self, rng, cell, w=W, h=H):
        self.cell = cell
        self.gw, self.gh = w // cell + 2, h // cell + 2
        self.g = [rng.random() for _ in range(self.gw * self.gh)]

    def __call__(self, x, y):
        c = self.cell
        gx, gy = x // c, y // c
        fx, fy = (x % c) / c, (y % c) / c
        fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        g, gw = self.g, self.gw
        i = gy * gw + gx
        a = g[i] + (g[i + 1] - g[i]) * fx
        b = g[i + gw] + (g[i + gw + 1] - g[i + gw]) * fx
        return a + (b - a) * fy


def fbm(rng, cells, weights):
    """Sum of noise layers at several scales, normalised to 0..1."""
    layers = [Noise(rng, c) for c in cells]
    total = sum(weights)
    return lambda x, y: sum(n(x, y) * w for n, w in zip(layers, weights)) / total


# --- canvas --------------------------------------------------------------

class Canvas:
    def __init__(self, w, h, fill):
        self.w, self.h = w, h
        self.px = bytearray([fill]) * (w * h)

    def get(self, x, y):
        return self.px[y * self.w + x]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = c

    def rect(self, x0, y0, x1, y1, c):  # half-open box
        x0, x1 = max(x0, 0), min(x1, self.w)
        for y in range(max(y0, 0), min(y1, self.h)):
            o = y * self.w
            self.px[o + x0:o + x1] = bytes([c]) * (x1 - x0)

    def bevel(self, x0, y0, x1, y1, raised=True):
        """1px two-tone edge on box [x0,x1)x[y0,y1), VOX style."""
        tl, br = (LIGHT, DARK) if raised else (DARK, LIGHT)
        self.rect(x0, y0, x1, y0 + 1, tl)
        self.rect(x0, y0, x0 + 1, y1, tl)
        self.rect(x0, y1 - 1, x1, y1, br)
        self.rect(x1 - 1, y0, x1, y1, br)


def text_mask(s, scale=1):
    """Pixel mask of s in DepartureMono at 11px, antialiasing off, then
    scaled up by an integer factor (stays on the font's pixel grid)."""
    font = ImageFont.truetype(FONT, FONT_PX)
    l, t, r, b = font.getbbox(s)
    img = Image.new("1", (r, b))
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    d.text((0, 0), s, font=font, fill=1)
    img = img.crop((0, t, r, b))
    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    return img


def stamp(cv, mask, x0, y0, color, keep=None):
    """Paint mask's set pixels; keep(x, y) -> False skips a pixel (wear)."""
    data = mask.load()
    for my in range(mask.height):
        for mx in range(mask.width):
            if data[mx, my]:
                x, y = x0 + mx, y0 + my
                if keep is None or keep(x, y):
                    cv.set(x, y, color)


def line(cv, x0, y0, x1, y1, c):
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        cv.set(x0, y0, c)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


# --- layers, in painting order -------------------------------------------

def wall(cv, rng):
    """--field base; a few panels a shade lighter (dithered to --panel)."""
    cells = [(cx, cy) for cx in range(W // PANEL_W) for cy in range(H // PANEL_H)]
    for cx, cy in rng.sample(cells, 7):
        density = rng.choice((0.19, 0.25, 0.31))
        for y in range(cy * PANEL_H, (cy + 1) * PANEL_H):
            for x in range(cx * PANEL_W, (cx + 1) * PANEL_W):
                if dith(x, y, density):
                    cv.set(x, y, PANEL)


def stencil(cv, rng):
    """Huge SITE-9 in --bevel-light (264px = 24 x 11), worn in patches,
    with a stencil bridge cut through each letter."""
    scale = 24
    word = "SITE-9"
    font = ImageFont.truetype(FONT, FONT_PX)
    adv = round(font.getlength("M"))  # monospace advance at 11px
    glyphs = [text_mask(ch, 1) for ch in word]
    top = min(font.getbbox(ch)[1] for ch in word if ch != "-")
    width = adv * len(word) * scale
    x0, y0 = (W - width) // 2, 300
    wear = fbm(rng, (90, 31, 9), (3, 2, 1))
    keep = lambda x, y: wear(x, y) + (BAYER[y & 7][x & 7] - 0.5) * 0.12 > 0.31
    for i, (ch, g) in enumerate(zip(word, glyphs)):
        g = g.resize((g.width * scale, g.height * scale), Image.NEAREST)
        gx = x0 + i * adv * scale
        gy = y0 + (font.getbbox(ch)[1] - top) * scale
        if ch != "-":  # bridge: a gap across the middle of the letter
            mid = g.height // 2 - scale // 2
            ImageDraw.Draw(g).rectangle((0, mid, g.width, mid + 7), fill=0)
        stamp(cv, g, gx, gy, LIGHT, keep)


def grime(cv, rng, amount):
    """--bevel-dark soot: heavier toward the bottom and the left edge."""
    blotch = fbm(rng, (160, 47, 13, 4), (4, 3, 2, 1))
    for y in range(H):
        fy = (y / H) ** 2.2
        for x in range(W):
            fx = (1 - x / W) ** 3
            d = (0.04 + 0.42 * fy + 0.30 * fx) * amount
            d *= max(0.0, blotch(x, y) * 1.8 - 0.45)
            if dith(x, y, d):
                cv.set(x, y, DARK)


def streaks(cv, rng, amount):
    """Soot running down from the horizontal seams."""
    for sy in range(PANEL_H, H, PANEL_H):
        for _ in range(int(9 * amount)):
            x = rng.randrange(0, W)
            length = rng.randint(25, 150)
            width = rng.randint(1, 3)
            start = rng.uniform(0.35, 0.7)
            for dy in range(length):
                d = start * (1 - dy / length)
                for dx in range(width):
                    if dith(x + dx, sy + 2 + dy, d):
                        cv.set(x + dx, sy + 2 + dy, DARK)


def seams(cv):
    """1px recessed seams: dark line, light line beside it."""
    for sx in range(0, W, PANEL_W):
        cv.rect(sx, 0, sx + 1, H, DARK)
        cv.rect(sx + 1, 0, sx + 2, H, LIGHT)
    for sy in range(PANEL_H, H, PANEL_H):
        cv.rect(0, sy, W, sy + 1, DARK)
        for x in range(W):
            if x % PANEL_W != 0:  # vertical dark lines stay unbroken
                cv.set(x, sy + 1, LIGHT)


def rivet(cv, x, y):
    """2x2: light top-left, dark bottom-right."""
    cv.set(x, y, LIGHT)
    cv.set(x + 1, y, PANEL)
    cv.set(x, y + 1, PANEL)
    cv.set(x + 1, y + 1, DARK)


def rivets(cv):
    for cx in range(0, W, PANEL_W):
        for cy in range(0, H, PANEL_H):
            for rx, ry in ((7, 7), (PANEL_W - 8, 7), (7, PANEL_H - 8), (PANEL_W - 8, PANEL_H - 8)):
                rivet(cv, cx + rx, cy + ry)


def scratches(cv, rng, count):
    """Sparse 1px --bevel-light scratches."""
    for _ in range(count):
        x, y = rng.randrange(W), rng.randrange(60, H - 30)
        length = rng.randint(3, 13)
        slope = rng.choice((-1, 0, 0, 1)) * rng.randint(0, 3)
        line(cv, x, y, x + length, y + slope, LIGHT)


def pipe(cv, rng):
    """A bevelled --panel pipe under the bar (shows in the 20px top gap),
    with dark brackets."""
    y0, y1 = TOP_GAP[0] + 4, TOP_GAP[1] - 4  # 12px tall
    cv.rect(0, y0, W, y1, PANEL)
    cv.rect(0, y0, W, y0 + 1, LIGHT)
    for x in range(W):  # soft highlight and underside, dithered
        if dith(x, y0 + 2, 0.5):
            cv.set(x, y0 + 2, LIGHT)
        if dith(x, y1 - 2, 0.5):
            cv.set(x, y1 - 2, DARK)
    cv.rect(0, y1 - 1, W, y1, DARK)
    for x in range(120, W, PANEL_W):  # brackets bolted to the wall
        cv.rect(x - 5, TOP_GAP[0] + 1, x + 5, TOP_GAP[1] - 1, DARK)
        cv.rect(x - 3, y0 - 1, x + 3, y1 + 1, DARK)
        cv.rect(x - 5, TOP_GAP[0] + 1, x + 5, TOP_GAP[0] + 2, PANEL)
        rivet(cv, x - 1, TOP_GAP[0] + 2)
        rivet(cv, x - 1, TOP_GAP[1] - 4)
    for x in range(360, W, 2 * PANEL_W):  # couplings
        cv.rect(x - 2, y0 - 1, x + 2, y1 + 1, PANEL)
        cv.rect(x - 2, y0 - 1, x - 1, y1 + 1, LIGHT)
        cv.rect(x + 1, y0 - 1, x + 2, y1 + 1, DARK)


def signage(cv, rng):
    """Small painted text, top left, --text-dim."""
    mask = text_mask("◄ TEST CHAMBERS   LEVEL 3 // SECTOR C", 2)
    wear = fbm(rng, (14, 4), (2, 1))
    stamp(cv, mask, 44, 74, DIM, lambda x, y: wear(x, y) > 0.22)


def logo_pixels(path, size, rng):
    """User's logo as paint on the slot: its ink (opaque pixels, or, with
    no alpha, pixels unlike the corner color) in --text, antialiased
    edges turned into ordered dither, a few worn spots. Tones inside the
    logo are not kept — one paint color, like the stencil. A wide logo
    (emblem + wordmark) is cut to its left square, the emblem.
    Returns {(x, y): index}."""
    img = Image.open(path).convert("RGBA")
    if img.width > 1.5 * img.height:
        img = img.crop((0, 0, img.height, img.height))
    bg = img.getpixel((0, 0))
    has_alpha = img.getextrema()[3][0] < 255
    cov = Image.new("L", img.size)
    src, dst = img.load(), cov.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = src[x, y]
            if has_alpha:
                dst[x, y] = a
            else:
                dst[x, y] = min(255, 2 * max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2])))
    cov.thumbnail((size, size), Image.LANCZOS)
    wear = Noise(rng, 4)
    ox, oy = (size - cov.width) // 2, (size - cov.height) // 2
    out = {}
    for y in range(cov.height):
        for x in range(cov.width):
            c = cov.getpixel((x, y)) / 255
            if c > 0 and wear(x, y) > 0.14 and dith(x, y, c):
                out[(ox + x, oy + y)] = TEXT
    return out


def placard(cv, rng, logo):
    """A raised VOX panel, bottom right, with four screw heads."""
    w, h = 340, 196
    x0, y0 = 1540, 836
    cv.rect(x0 - 1, y0 - 1, x0 + w + 1, y0 + h + 1, DARK)  # sits on the wall
    cv.rect(x0, y0, x0 + w, y0 + h, PANEL)
    cv.bevel(x0, y0, x0 + w, y0 + h, raised=True)
    for sx, sy in ((5, 5), (w - 8, 5), (5, h - 8), (w - 8, h - 8)):
        x, y = x0 + sx, y0 + sy  # 3x3 dome with a dark slot
        cv.rect(x, y, x + 3, y + 3, PANEL)
        cv.set(x, y, LIGHT)
        cv.set(x + 1, y, LIGHT)
        cv.set(x, y + 1, LIGHT)
        cv.set(x + 2, y + 2, DARK)
        line(cv, x, y + 2, x + 2, y, DARK)

    # Logo slot: a recessed square.
    lx, ly, ls = x0 + 16, y0 + 16, 74
    cv.rect(lx, ly, lx + ls, ly + ls, FIELD)
    cv.bevel(lx, ly, lx + ls, ly + ls, raised=False)
    if logo:
        for (x, y), c in logo_pixels(logo, ls - 10, rng).items():
            cv.set(lx + 5 + x, ly + 5 + y, c)

    stamp(cv, text_mask("SITE-9", 2), x0 + 108, y0 + 24, BRIGHT)
    stamp(cv, text_mask("RESEARCH FACILITY"), x0 + 108, y0 + 58, TEXT)

    sy = y0 + 104  # recessed seam
    cv.rect(x0 + 12, sy, x0 + w - 12, sy + 1, DARK)
    cv.rect(x0 + 12, sy + 1, x0 + w - 12, sy + 2, LIGHT)

    stamp(cv, text_mask("OPERATOR ..... ANDR1CS"), x0 + 16, y0 + 118, TEXT)
    stamp(cv, text_mask("CLEARANCE .... LEVEL 3"), x0 + 16, y0 + 136, TEXT)

    bx, by, bw, bh = x0 + 16, y0 + 158, 214, 24  # barcode, recessed
    cv.rect(bx, by, bx + bw, by + bh, FIELD)
    cv.bevel(bx, by, bx + bw, by + bh, raised=False)
    x = bx + 6
    while x < bx + bw - 8:
        bar = rng.choice((1, 1, 2, 3))
        cv.rect(x, by + 4, x + bar, by + bh - 4, TEXT)
        x += bar + rng.choice((1, 2, 2, 3))

    for i, color in enumerate((WARN, CRIT)):  # unlit lamps: half-lit dither
        lx = x0 + w - 70 + i * 28
        cv.rect(lx, by + 2, lx + 18, by + 22, FIELD)
        cv.bevel(lx, by + 2, lx + 18, by + 22, raised=False)
        for y in range(by + 5, by + 19):
            for x in range(lx + 3, lx + 15):
                cv.set(x, y, color if dith(x, y, 0.5) else DARK)


# --- main ----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--variant", choices=("V1", "V2"), default="V1")
    ap.add_argument("--seed", type=int, default=9)
    ap.add_argument("--logo", default=os.path.expanduser("~/.local/share/site-9/logo.png"))
    ap.add_argument("--out", default=os.path.expanduser("~/.local/share/site-9/wallpaper.png"))
    ap.add_argument("--no-placard", action="store_true",
                    help="leave out the placard (login screen background)")
    a = ap.parse_args()

    v1 = a.variant == "V1"
    rng = random.Random(a.seed)
    logo = a.logo if os.path.isfile(a.logo) and not a.no_placard else None
    if not logo and not a.no_placard:
        print(f"no logo at {a.logo}: plain slot", file=sys.stderr)

    cv = Canvas(W, H, FIELD)
    wall(cv, rng)
    if v1:
        stencil(cv, rng)
    grime(cv, rng, 1.0 if v1 else 0.55)
    streaks(cv, rng, 1.0 if v1 else 0.5)
    seams(cv)
    rivets(cv)
    scratches(cv, rng, 90 if v1 else 40)
    pipe(cv, rng)
    signage(cv, rng)
    if not a.no_placard:
        placard(cv, rng, logo)

    img = Image.frombytes("P", (W, H), bytes(cv.px))
    pal = []
    for _, v in TOKENS:
        pal += [v >> 16, v >> 8 & 255, v & 255]
    img.putpalette(pal)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    img.save(a.out, optimize=True)
    used = sorted({c for _, c in img.getcolors()})
    print(f"{a.out}: {a.variant}, seed {a.seed}"
          + (", no placard" if a.no_placard else "") + ", colors used: "
          + ", ".join(TOKENS[i][0] for i in used))


if __name__ == "__main__":
    main()
