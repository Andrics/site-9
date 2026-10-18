#!/usr/bin/env python3
"""Writes ../SITE-9.svg, the SITE-9 Kvantum theme's elements.

Run from this folder:  python3 make-svg.py

Kvantum draws a widget from named SVG elements: an interior
("<element>-<state>") stretched to the widget, and eight frame pieces
("<element>-<state>-top", "-topleft", ...) stretched along its edges at
the frame sizes set in SITE-9.kvconfig (all 1px here). So a bevel is just
1-unit rects in two colors. States: normal, focused (= hover), pressed,
toggled, disabled. Hover changes nothing (BUILD_SPEC.md §3), so
"focused" is always drawn like "normal".

Tokens: BUILD_SPEC.md §3 "Locked tokens".
"""

PANEL = "#445435"        # --panel: raised surfaces
FIELD = "#303f25"        # --field: recessed surfaces
LIGHT = "#667359"        # --bevel-light
DARK = "#1f2719"         # --bevel-dark
TEXT = "#cbcfc8"         # --text
BRIGHT = "#ffffff"       # --text-bright
DIM = "#8f9a85"          # --text-dim (disabled)

STATES = ["normal", "focused", "pressed", "toggled", "disabled"]
out = []
y_cursor = [0]  # elements are laid out in a column so none overlap


def place(h):
    y = y_cursor[0]
    y_cursor[0] += h + 4
    return y


def rect(id_, x, y, w, h, fill, opacity=1):
    op = "" if opacity == 1 else f' fill-opacity="{opacity}"'
    idattr = f' id="{id_}"' if id_ else ""
    out.append(f'<rect{idattr} x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{op}/>')


# Bevel colors per side: (top, left, bottom, right). Corners: top-left
# takes the top/left color, bottom-right the bottom/right color; the two
# mixed corners take the right edge (top-right) and left edge
# (bottom-left) color, as kitty's bevel.py does.
RAISED = (LIGHT, LIGHT, DARK, DARK)
SUNKEN = (DARK, DARK, LIGHT, LIGHT)


def framed(name, state, interior, bevel):
    """Interior + 8 one-unit frame pieces for one element state."""
    y = place(10)
    base = f"{name}-{state}"
    if interior is None:
        rect(base, 20, y, 8, 8, "#000000", 0)       # present but empty
    else:
        rect(base, 20, y, 8, 8, interior)
    if bevel is None:
        top = left = bottom = right = None
    else:
        top, left, bottom, right = bevel
    sides = {
        "top": (0, y, 8, 1, top), "bottom": (0, y + 9, 8, 1, bottom),
        "left": (10, y, 1, 8, left), "right": (12, y, 1, 8, right),
        "topleft": (14, y, 1, 1, top), "topright": (15, y, 1, 1, right),
        "bottomleft": (16, y, 1, 1, left), "bottomright": (17, y, 1, 1, bottom),
    }
    for side, (x, yy, w, h, color) in sides.items():
        if color is None:
            rect(f"{base}-{side}", x, yy, w, h, "#000000", 0)
        else:
            rect(f"{base}-{side}", x, yy, w, h, color)


def element(name, normal, pressed, disabled=None):
    """normal/pressed: (interior, bevel). focused = normal, toggled =
    pressed, disabled = normal unless given."""
    disabled = disabled or normal
    for state, spec in (("normal", normal), ("focused", normal), ("pressed", pressed),
                        ("toggled", pressed), ("disabled", disabled)):
        framed(name, state, *spec)


# --- Raised blocks; pressed/toggled = recessed --field ----------------
element("button", (PANEL, RAISED), (FIELD, SUNKEN))
element("tab", (PANEL, RAISED), (FIELD, SUNKEN))
element("scrollbarslider", (PANEL, RAISED), (PANEL, RAISED))
element("slidercursor", (PANEL, RAISED), (PANEL, RAISED))
element("tooltip", (FIELD, RAISED), (FIELD, RAISED))
element("tabframe", (PANEL, RAISED), (PANEL, RAISED))
element("dock", (PANEL, None), (PANEL, None))
element("toolbar", (PANEL, None), (PANEL, None))
element("splitter", (PANEL, None), (PANEL, None))
element("menubar", (PANEL, None), (PANEL, None))

# Tool buttons: flat until pressed or toggled (like GTK's flat buttons).
element("toolbutton", (None, None), (FIELD, SUNKEN))

# --- Recessed fields ---------------------------------------------------
element("lineedit", (FIELD, SUNKEN), (FIELD, SUNKEN))
element("spin", (FIELD, SUNKEN), (FIELD, SUNKEN))
element("common", (FIELD, SUNKEN), (FIELD, SUNKEN))
element("group", (None, SUNKEN), (None, SUNKEN))
element("menu", (FIELD, SUNKEN), (FIELD, SUNKEN))
element("progress", (FIELD, SUNKEN), (FIELD, SUNKEN))
element("slider", (FIELD, SUNKEN), (FIELD, SUNKEN))
element("scrollgroove", (FIELD, None), (FIELD, None))
element("progress-pattern", (TEXT, None), (TEXT, None))

# --- Rows: nothing until selected / highlighted ------------------------
# Item views: selected = --panel (toggled/pressed); hover draws nothing.
element("itemview", (None, None), (PANEL, None))
# Menu items: the highlighted row is --panel ("focused" here IS the
# keyboard/pointer highlight, so it can't be blank).
for state, fill in (("normal", None), ("focused", PANEL), ("pressed", PANEL),
                    ("toggled", PANEL), ("disabled", None)):
    framed("menuitem", state, fill, None)
# Menubar items: pressed in while their menu is open.
for state, spec in (("normal", (None, None)), ("focused", (FIELD, SUNKEN)),
                    ("pressed", (FIELD, SUNKEN)), ("toggled", (FIELD, SUNKEN)),
                    ("disabled", (None, None))):
    framed("menubaritem", state, *spec)


# --- Focus: 1px dotted --text box (pick c) ------------------------------
# Kvantum tiles the frame pieces at frame.patternsize (2), so a 2-unit
# piece with one lit unit gives a dotted line.
for side, (w, h) in {"top": (2, 1), "bottom": (2, 1), "left": (1, 2), "right": (1, 2)}.items():
    y = place(2)
    out.append(f'<g id="focus-{side}">')
    rect(None, 30, y, w, h, "#000000", 0)
    rect(None, 30, y, 1, 1, TEXT)
    out.append("</g>")
for corner in ("topleft", "topright", "bottomleft", "bottomright"):
    rect(f"focus-{corner}", 40, place(1), 1, 1, TEXT)
rect("focus", 44, place(2), 2, 2, "#000000", 0)


# --- Pixel art ----------------------------------------------------------
def pixels(id_, rows, color, box=None):
    """Group of 1-unit rects for '#' cells, inside a transparent box that
    fixes the element's size (Kvantum scales the element's bounds)."""
    h, w = len(rows), len(rows[0])
    bw, bh = box or (w, h)
    y0 = place(bh)
    ox, oy = (bw - w) // 2, (bh - h) // 2
    out.append(f'<g id="{id_}">')
    rect(None, 60, y0, bw, bh, "#000000", 0)
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                rect(None, 60 + ox + c, y0 + oy + r, 1, 1, color)
    out.append("</g>")


ARROW_DOWN = ["#######", ".#####.", "..###..", "...#..."]
ARROWS = {
    "down": ARROW_DOWN,
    "up": ARROW_DOWN[::-1],
    "right": ["".join(ARROW_DOWN[r][c] for r in range(4)) for c in range(7)],
    "left": ["".join(ARROW_DOWN[r][c] for r in range(3, -1, -1)) for c in range(7)],
    "plus": ["...#...", "...#...", "...#...", "#######", "...#...", "...#...", "...#..."],
    "minus": ["#######"],
}
for name, art in ARROWS.items():
    for state in STATES:
        color = {"pressed": BRIGHT, "toggled": BRIGHT, "disabled": DIM}.get(state, TEXT)
        pixels(f"arrow-{name}-{state}", art, color, box=(9, 9))

CLOSE = ["#.....#", ".#...#.", "..#.#..", "...#...", "..#.#..", ".#...#.", "#.....#"]
for state in STATES:
    pixels(f"tab-close-{state}", CLOSE, DIM if state == "disabled" else TEXT, box=(9, 9))

# Check boxes and radio buttons (pick b): both square, a recessed 13px
# box; tick / 5px square / tristate bar in --text-bright.
TICK = ["......#", ".....##", "#...###", "##.###.", "#####..", ".###...", "..#...."]
SQUARE = ["#####"] * 5
BAR = ["#######"] * 2


def box(id_, mark, mark_color):
    y0 = place(13)
    out.append(f'<g id="{id_}">')
    rect(None, 80, y0, 13, 13, FIELD)
    rect(None, 80, y0, 13, 1, DARK)          # top
    rect(None, 80, y0, 1, 13, DARK)          # left
    rect(None, 80, y0 + 12, 13, 1, LIGHT)    # bottom
    rect(None, 92, y0, 1, 13, LIGHT)         # right
    if mark:
        h, w = len(mark), len(mark[0])
        ox, oy = (13 - w) // 2, (13 - h) // 2
        for r, row in enumerate(mark):
            for c, ch in enumerate(row):
                if ch == "#":
                    rect(None, 80 + ox + c, y0 + oy + r, 1, 1, mark_color)
    out.append("</g>")


for state in STATES:
    mark_color = DIM if state == "disabled" else BRIGHT
    box(f"checkbox-{state}", None, None)
    box(f"checkbox-checked-{state}", TICK, mark_color)
    box(f"checkbox-tristate-{state}", BAR, mark_color)
    box(f"radio-{state}", None, None)
    box(f"radio-checked-{state}", SQUARE, mark_color)

# Elements that must exist but draw nothing (otherwise Kvantum falls back
# to its default theme's art): grips, handles, glows, shadows.
for empty in ["splitter-grip-normal", "splitter-grip-focused", "splitter-grip-pressed",
              "splitter-grip-toggled", "splitter-grip-disabled", "toolbar-handle",
              "header-separator", "sizegrip-normal", "sizegrip-focused", "sizegrip-pressed",
              "sizegrip-toggled", "sizegrip-disabled", "button-default-indicator",
              "grip-normal", "grip-focused", "grip-pressed", "grip-toggled", "grip-disabled",
              "tab-tear", "slider-tick-normal", "slider-tick-disabled"]:
    rect(empty, 100, place(2), 2, 2, "#000000", 0)

height = y_cursor[0]
svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
       f'<!-- SITE-9 Kvantum theme. Generated by tools/make-svg.py — edit that, not this. -->\n'
       f'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="{height}" '
       f'viewBox="0 0 120 {height}" shape-rendering="crispEdges">\n'
       + "\n".join(out) + "\n</svg>\n")
open("../SITE-9.svg", "w").write(svg)
print(f"wrote ../SITE-9.svg ({len(out)} nodes)")
