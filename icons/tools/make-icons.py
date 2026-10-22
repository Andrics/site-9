#!/usr/bin/env python3
"""SITE-9 icon theme: Chicago95 remapped to the §3 tokens (BUILD_SPEC.md,
Phase 2.5 pick C2).

Chicago95's icons are Win95 16-colour pixel art, so each palette colour
maps to one token (table below) and the icons stay pixel-exact. Colours
outside that palette go to their nearest Win95 colour first. Partial
alpha is cut at 50% so every pixel is a token or transparent.

    make-icons.py [--src /usr/share/icons/Chicago95] [--out ~/.local/share/icons/SITE-9]

Reads the installed Chicago95 theme (AUR chicago95-icon-theme-git) and
writes a full copy, remapped, outside the repo (generated, ~thousands of
files; rerun after a Chicago95 update). Symlinks stay symlinks. Not a
stow package — run it from the repo. Needs Pillow (python-pillow).
"""
import argparse
import os
import re
import shutil
import subprocess

from PIL import Image, UnidentifiedImageError

# Win95 palette -> SITE-9 token
W95 = {
    0x000000: 0x1f2719,  # black   -> --bevel-dark
    0x808080: 0x667359,  # grey    -> --bevel-light
    0xc0c0c0: 0xcbcfc8,  # silver  -> --text
    0xffffff: 0xffffff,  # white   -> --text-bright
    0x808000: 0x445435,  # olive   -> --panel
    0xffff00: 0xe6a84f,  # yellow  -> --warning (folders)
    0x800000: 0x1f2719,  # maroon  -> --bevel-dark
    0xff0000: 0xff7a5c,  # red     -> --critical
    0x008000: 0x445435,  # green   -> --panel
    0x00ff00: 0x8f9a85,  # lime    -> --text-dim
    0x000080: 0x303f25,  # navy    -> --field (title bars)
    0x0000ff: 0x667359,  # blue    -> --bevel-light
    0x008080: 0x445435,  # teal    -> --panel
    0x00ffff: 0xcbcfc8,  # cyan    -> --text
    0x800080: 0x445435,  # purple  -> --panel
    0xff00ff: 0xff7a5c,  # magenta -> --critical
}


def nearest(v):
    r, g, b = v >> 16, v >> 8 & 255, v & 255
    k = min(W95, key=lambda c: (r - (c >> 16)) ** 2 + (g - (c >> 8 & 255)) ** 2 + (b - (c & 255)) ** 2)
    return W95[k]


_cache = {}


def token(v):
    if v not in _cache:
        _cache[v] = W95.get(v) or nearest(v)
    return _cache[v]


def png(src, dst):
    try:
        img = Image.open(src).convert("RGBA")
    except UnidentifiedImageError:
        # upstream has a few SVGs named .png; remap by content
        with open(src, "rb") as f:
            head = f.read(512)
        if b"<svg" in head:
            return svg(src, dst)
        shutil.copy2(src, dst)
        return
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a < 128:
                px[x, y] = (0, 0, 0, 0)
                continue
            t = token((r << 16) | (g << 8) | b)
            px[x, y] = (t >> 16, t >> 8 & 255, t & 255, 255)
    img.save(dst, optimize=True)


HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def svg(src, dst):
    def sub(m):
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return "#%06x" % token(int(h, 16))
    with open(src, encoding="utf-8", errors="surrogateescape") as f:
        data = f.read()
    with open(dst, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(HEX.sub(sub, data))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--src", default="/usr/share/icons/Chicago95")
    ap.add_argument("--out", default=os.path.expanduser("~/.local/share/icons/SITE-9"))
    a = ap.parse_args()

    if os.path.exists(a.out):
        shutil.rmtree(a.out)
    counts = {"png": 0, "svg": 0, "link": 0, "copy": 0}
    for root, dirs, files in os.walk(a.src):
        rel = os.path.relpath(root, a.src)
        os.makedirs(os.path.join(a.out, rel), exist_ok=True)
        for d in dirs:  # directory symlinks
            s = os.path.join(root, d)
            if os.path.islink(s):
                os.symlink(os.readlink(s), os.path.join(a.out, rel, d))
                counts["link"] += 1
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        for n in files:
            s, t = os.path.join(root, n), os.path.join(a.out, rel, n)
            if os.path.islink(s):
                os.symlink(os.readlink(s), t)
                counts["link"] += 1
            elif n.endswith(".png"):
                png(s, t)
                counts["png"] += 1
            elif n.endswith(".svg"):
                svg(s, t)
                counts["svg"] += 1
            elif n == "index.theme":
                with open(s) as f:
                    text = f.read()
                text = re.sub(r"(?m)^Name=.*$", "Name=SITE-9", text, count=1)
                text = re.sub(r"(?m)^Comment=.*$", "Comment=Chicago95 remapped to the SITE-9 tokens", text, count=1)
                with open(t, "w") as f:
                    f.write(text)
            elif n == "icon-theme.cache":
                continue  # rebuilt below
            else:
                shutil.copy2(s, t)
                counts["copy"] += 1
    if os.path.isfile(os.path.join(a.out, "index.theme")):
        subprocess.run(["gtk-update-icon-cache", "-f", "-q", a.out], check=False)
    print(a.out, counts)


if __name__ == "__main__":
    main()
