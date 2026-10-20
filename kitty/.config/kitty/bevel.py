# kitty/.config/kitty/bevel.py — loaded by `watcher bevel.py` (kitty.conf).
# SITE-9 window frame (BUILD_SPEC.md §3 "Locked terminal: kitty", F3):
# an 8px --panel frame around each pane, and a recessed 1px bevel around
# the text box — top/left --bevel-dark, bottom/right --bevel-light, like
# the bar's pressed workspace tab.
#
# kitty has no setting for this: it draws each border side as its own
# rect but gives all four one color, and paints margins in the window
# background. This wraps kitty's hand-off of those rects to the GPU
# (kitty.borders.set_borders_rects, an internal, checked on kitty 0.49.2)
# and recolors them. Runs only when kitty redraws its borders (resize,
# split, focus) — nothing continuous. On any error it passes kitty's own
# rects through unchanged and prints one line to kitty's stderr.
import sys

import kitty.borders as kb
from kitty.borders import BorderColor

PANEL = 0x445435  # --panel

_orig = kb.set_borders_rects
_warned = False


def _minus(r, b):
    """Parts of rect r outside box b (up to four rects)."""
    l, t, rr, bb = r.left, r.top, r.right, r.bottom
    if b[2] <= l or b[0] >= rr or b[3] <= t or b[1] >= bb:
        return [r]
    out = []
    if t < b[1]:
        out.append(r._replace(bottom=b[1]))
    if b[3] < bb:
        out.append(r._replace(top=b[3]))
    mt, mb = max(t, b[1]), min(bb, b[3])
    if l < b[0]:
        out.append(r._replace(top=mt, bottom=mb, right=b[0]))
    if b[2] < rr:
        out.append(r._replace(top=mt, bottom=mb, left=b[2]))
    return out


def _recolor(r, boxes):
    c = int(r.color) & 0xff
    if c == BorderColor.default_bg:
        # A blank rect runs from the window edge to the cells. Outside the
        # pane's border box it is margin (or kitty's spare pixels): paint
        # that --panel (slot 3 takes its RGB from the rect, border.slang).
        # Inside the box it is padding: keep the window background.
        outside = [r]
        for b in boxes:
            outside = [p for o in outside for p in _minus(o, b)]
        panel = [o._replace(color=(PANEL << 8) | BorderColor.window_bg) for o in outside]
        return [r] + panel
    if c in (BorderColor.active, BorderColor.inactive):
        # add_borders(): top/left sides carry -window_id, bottom/right +id.
        # inactive = --bevel-dark, active = --bevel-light (kitty.conf).
        side = BorderColor.inactive if r.border_type < 0 else BorderColor.active
        return [r._replace(color=side)]
    return [r]


def _set_borders_rects(os_window_id, tab_id, rects):
    # One box per pane, from its four border sides; blank rects inside a
    # box are the pane's padding and keep the window background.
    global _warned
    try:
        new = _bevel(rects)
    except Exception as e:
        new = rects  # kitty internals changed: fall back to its own borders
        if not _warned:  # once per kitty process, so a broken update shows
            _warned = True
            print(f"bevel.py: fallback to kitty's own borders ({type(e).__name__}: {e})",
                  file=sys.stderr, flush=True)
    _orig(os_window_id, tab_id, new)


def _bevel(rects):
    boxes = {}
    for r in rects:
        if (int(r.color) & 0xff) in (BorderColor.active, BorderColor.inactive, BorderColor.bell):
            b = boxes.setdefault(abs(r.border_type), [r.left, r.top, r.right, r.bottom])
            b[0], b[1] = min(b[0], r.left), min(b[1], r.top)
            b[2], b[3] = max(b[2], r.right), max(b[3], r.bottom)
    boxes = list(boxes.values())
    return [x for r in rects for x in _recolor(r, boxes)]


kb.set_borders_rects = _set_borders_rects
