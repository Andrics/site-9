#!/usr/bin/env python3
# Writes the theme's pixel-art PNGs (no dependencies). Run from this folder:
#   python3 make-assets.py
# check.png: 11x11, the classic 7x7 tick in --text-bright (#ffffff),
# centred, transparent around it — exactly the check box's content size,
# so GTK draws it 1:1 (no scaling blur).
import struct, zlib

TICK = [
    "......#",
    ".....##",
    "#...###",
    "##.###.",
    "#####..",
    ".###...",
    "..#....",
]

def png(path, rows, rgb=(0xff, 0xff, 0xff)):
    h, w = len(rows), len(rows[0])
    raw = b"".join(b"\0" + b"".join(bytes(rgb) + (b"\xff" if c == "#" else b"\0") if c == "#" else b"\0\0\0\0" for c in r) for r in rows)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    open(path, "wb").write(data)

pad = 2
rows = ["." * 11] * pad + ["." * pad + r + "." * pad for r in TICK] + ["." * 11] * pad
png("../gtk-3.0/assets/check.png", rows)
