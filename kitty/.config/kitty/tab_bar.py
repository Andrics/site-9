# kitty/.config/kitty/tab_bar.py
# SITE-9 tabs as VOX buttons, like waybar's workspace tabs
# (BUILD_SPEC.md §3). kitty calls draw_tab once per tab when the bar
# changes; nothing here redraws on a timer.
#
# kitty's tab bar is one text row, so the edges are glyphs kitty draws
# itself, 1px each: ▏ left edge, ▕ right edge, and a colored underline
# as the bottom edge (kitty has no overline, so there is no top edge).
from kitty.tab_bar import as_rgb, draw_title

PANEL = 0x445435        # --panel: raised tab, strip
FIELD = 0x303f25        # --field: pressed (active) tab
BEVEL_LIGHT = 0x667359  # --bevel-light
BEVEL_DARK = 0x1f2719   # --bevel-dark
TEXT = 0xcbcfc8         # --text
TEXT_BRIGHT = 0xffffff  # --text-bright


def underline(color):
    # SGR 4:1 = straight underline, 58 = its color.
    r, g, b = color >> 16, (color >> 8) & 0xFF, color & 0xFF
    return f'4:1;58:2::{r}:{g}:{b}'


def draw_tab(draw_data, screen, tab, before, max_tab_length, index, is_last, extra_data):
    active = tab.is_active
    # Raised: light top/left, dark bottom/right. Pressed: reversed.
    light, dark = (BEVEL_DARK, BEVEL_LIGHT) if active else (BEVEL_LIGHT, BEVEL_DARK)

    screen.cursor.bold = screen.cursor.italic = False
    screen.cursor.bg = as_rgb(FIELD if active else PANEL)
    screen.apply_sgr(underline(dark))

    screen.cursor.fg = as_rgb(light)
    screen.draw('▏')
    screen.cursor.fg = as_rgb(TEXT_BRIGHT if active else TEXT)
    screen.draw(' ')
    draw_title(draw_data, screen, tab, index, max_tab_length)
    # Too long for its share of the bar: cut it with an ellipsis,
    # leaving room for the trailing space and the right edge.
    limit = before + max_tab_length - 2
    if screen.cursor.x > limit:
        screen.cursor.x = limit - 1
        screen.draw('…')
    screen.draw(' ')
    screen.cursor.fg = as_rgb(dark)
    screen.draw('▕')
    end = screen.cursor.x

    # One cell of bare strip between tabs (bg 0 = tab_bar_background).
    screen.apply_sgr('24')
    screen.cursor.bg = screen.cursor.fg = 0
    if not is_last:
        screen.draw(' ')
    return end
