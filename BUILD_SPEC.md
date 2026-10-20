# SITE-9 — Build Spec

> Personal workstation configuration. Arch Linux / Hyprland.
> This is the source of truth for constraints and design decisions.
> Read this before touching styling on anything.
> Maintained by THE OVERSEER (since 2026-10-06). UNIT-1 reads, doesn't
> edit — see `AGENTS.md` "Docs ownership".

---

## 1. Hardware & platform

- Old laptop, Intel UHD integrated graphics (no dedicated GPU).
- Arch Linux, rolling release.
- Hyprland — **note:** the compositor's own config moved to Lua in v0.55
  (`~/.config/hypr/hyprland.lua`). `hypridle.conf`, `hyprlock.conf`, and
  `hyprpaper.conf` have **not** moved — they're still plain hyprlang syntax.
  Don't assume this list stays accurate — confirm the running version with
  `hyprctl version` at the start of each phase, since this API is still new
  and moves fast.

**UNIT-1: verify and fill in below before Phase 1 is marked done.** Don't
guess these — pull them from the actual machine.
- CPU: Intel Core i7-8650U @ 1.90GHz (8 threads, Kaby Lake-R)
- Exact iGPU model (`lspci -k | grep -A2 VGA`): Intel UHD Graphics 620
  (Kaby Lake-R GT2, rev 07) — onboard, Dell device 081b
- RAM: 15Gi total
- Screen resolution / refresh rate: 1920x1080 @ 60.05Hz (AU Optronics
  eDP-1, 15.6" panel — 290x170mm), 48.04Hz mode also available
- Arch kernel version (`uname -a`): 6.18.52-1-lts
- Hyprland version (`hyprctl version`): 0.56.2
- Display scale: **1x (native)** — locked 2026-09-21. `scale = "auto"` in
  `hyprland.lua` was defaulting to a fractional 1.5, conflicting with §2's
  integer-only rule; changed to `scale = "1"`, confirmed via `hyprctl
  monitors` (`1920x1080@60Hz`, `scale: 1`). See `PHASES.md` Phase 1 log.

## 2. Non-negotiable performance constraints

These override aesthetic preference every time. If a design idea conflicts
with one of these, the design idea loses.

- No blur, no drop shadows, no glassmorphism.
- No fractional scaling — integer scale only.
- `vfr = true` (variable frame rate) stays on everywhere it's supported.
- Animations: short (fast/snappy), simple curves only. Prefer linear or a
  single built-in easing over custom multi-keyframe curves.
- Nothing that renders continuously while idle (e.g. animated borders,
  looping background effects, animated wallpapers/video wallpapers).

**GTK theme defaults count.** Adwaita (GTK's default theme) adds its own
box-shadows and outlines to some widgets — e.g. a 1px shadow line on
hovered buttons, a blue focus outline on sliders. Those are drop
shadows / off-palette decoration by this spec: override them
(`box-shadow: none`, `outline: none`, explicit borders) wherever they
show up. Also found (2026-10-18): Adwaita gives every `button` a 1px
white `text-shadow` and tooltips a black one (clear with
`text-shadow: none`), and buttons a `transition: all 200ms
cubic-bezier(…)` fade — a custom easing curve, against the motion rule
in §3 (clear with `transition: none`).

**No `text-shadow` of any kind.** The double-strike weight exception
(`text-shadow: 1px 0 0 currentColor`, approved 2026-10-06) was
**retired 2026-10-18** with the move to regular weight (§3). Any blur,
any `box-shadow`, any `text-shadow` stays banned.

## 3. Design language: Half-Life VOX console

**Direction (user, 2026-10-09):** one look, everywhere — the
[suchipi/half-life-vox-console](https://github.com/suchipi/half-life-vox-console)
style (its `index.css` is in project context). Valve-era olive panels,
two-tone bevelled edges, blocky buttons, monospace text. **The SCP
report aesthetic and the HEV/HUD look are dropped** — one theme only, so
nothing reads inconsistent. Animations come later (Phase 4), in the same
style.

What defines it (from the reference CSS):
- Mid-tone olive surfaces, no near-black: a raised panel tone and a
  darker recessed field tone.
- **Bevels from plain per-side borders**: raised = light top/left, dark
  bottom/right; recessed (fields, pressed buttons) = reversed. No
  `box-shadow`, no gradient, radius 0 — §2-clean as it stands.
- Buttons and tags are raised blocks; text fields, lists and output
  areas are recessed.
- Off-white text; pure white for the selected/active item and titles.
  Selection highlights are flat background swaps, nothing glowing.

**Rule that still holds: palette, accent and fonts are NOT decided by
the agent** — they're personal choices, made by asking the user. Propose
2–3 concrete options and ask; record the pick here once made.

### Locked tokens (user, 2026-10-18 — on UNIT-1's renders)

Taken from the reference CSS, checked pixel-exact on the renders.
Contrast is against `--field`, where most text sits.

| Token | Value | Use | Contrast on `--field` |
|---|---|---|---|
| `--panel` | `#445435` | raised surfaces: bar background, buttons, `SITE-9`, selected list row | — |
| `--field` | `#303f25` | recessed surfaces: modules, lists, menus, pressed buttons | — |
| `--bevel-light` | `#667359` | light edge (raised top/left, recessed bottom/right) | — |
| `--bevel-dark` | `#1f2719` | dark edge; gauge troughs, unlit NET steps; flat border of single-color tools | — |
| `--text` | `#cbcfc8` | normal text (the reference's 75% white, flattened) | 7.1:1 |
| `--text-bright` | `#ffffff` | active/selected item, titles, typed-letter matches | 11.3:1 |
| `--text-dim` | `#8f9a85` | placeholders, and disabled controls in apps — **otherwise not on `--panel`** (2.8:1; disabled text may sit there, user 2026-10-18) | 3.8:1 |
| `--warning` | `#e6a84f` | flagged state | 5.4:1 |
| `--critical` | `#ff7a5c` | flagged state | 4.4:1 |

Warning/critical were brightened from the HUD-era `#c98a3c` / `#b8452e`
(user, 2026-10-18): the old red was 2.1:1 on `--field`, too hard to
read (`NET: OFFLINE`).

Single-color-border tools (fuzzel, mako) can't bevel; they get a flat
`--bevel-dark` edge. Hyprland window borders and kitty splits are flat
too, but show focus: active `--bevel-light`, inactive `--bevel-dark`.

### Locked look rules (user, 2026-10-09 and 2026-10-18)

- **Bevels 1px**, radius 0, no shadow, no gradient.
- **No accent color, no corner ticks.** Bevels do the framing;
  pressed-in + `--text-bright` marks "active".
- **Flagged states are text color only**, one color per readout: label,
  icon, gauge fill and value all turn `--warning` / `--critical`
  together. Backgrounds and bevels don't change.
- **Lists and menus** (picker, tooltips): `--field` background,
  selected row `--panel` with `--text-bright`, matched letters
  `--text-bright`.
- **Font: DepartureMono Nerd Font, 11px, regular weight, everywhere**
  (user, 2026-10-18). Double-strike is retired: only waybar could draw
  it (fuzzel, mako, kitty and GTK apps can't), so it would have meant
  two weights on screen; it also clogged the `W` in `PWR` and left a
  bright 1px column after every gauge. Regular matches the reference.

### Locked bar (waybar)

- **Layout A** (user, 2026-10-09; confirmed on renders 2026-10-18): bar
  background `--panel`, 1px `--bevel-dark` bottom edge (the bar is
  raised and sits flush at the top, so only its dark edge shows).
  Every module is a recessed field — the clock included; the tray
  is one field around all its icons.
- **Workspace tabs** are raised buttons with `--text` (not dim — dim is
  unreadable on `--panel`). The active tab is pressed in: recessed
  bevel, `--field` background, `--text-bright`.
- **Tab hover changes nothing** — default set by THE OVERSEER
  (2026-10-18), not asked; the user can change it after seeing the bar
  live. Adwaita's hover decoration stays cleared (§2).
- **Tab switches are instant** — no fade (`transition: none` clears
  Adwaita's 200ms eased fade; THE OVERSEER, 2026-10-18, applying the
  §3 motion rule).
- **`SITE-9`**: the machine's name, a raised block with `--text-bright`.
- **Layout (L2, trimmed 2026-10-18):** left — `SITE-9`, workspaces.
  Center — clock. Right — VOL, NET, PWR, tray. **CPU, RAM and MET
  (uptime) are off the bar** (user, 2026-10-18) — they move to the
  SITE-9 settings panel as "system diagnostics" (Phase 6). Their old
  spec: MET was uptime as `T+DDD:HH:MM`, every 60s; CPU/RAM were DOS
  gauges with no icon.
- **Tray:** icons 14px, keep their app colors. Hidden when empty.
- **Same inner padding in every field** (~7px each side, as NET and PWR
  have). VOL measured ~15px each side on `2.0-bar-trimmed-x3.png` —
  likely padding on both the drawer group `#volume` and `#pulseaudio`
  inside it (user, 2026-10-18; fix rides along in round #11). The
  wider gap before a 1-digit VOL value is the fixed-width number, by
  spec.
- **Height: 30px**, set explicitly (natural height is 24px).
- **Readouts:** icon, label, gauge, value — `◄ VOL: ██████████  60%`,
  `▂▄▆█ NET: 82%`, `⏻ PWR: ██████████  18%`.
  `PWR:` becomes `CHG:` while charging (no lightning glyph). Muted:
  `◄ VOL: MUTE` in `--text`, no gauge. Ethernet: `NET: LINK`, no steps.
  Percentages fixed-width (fmt `{x:>3}`).
- **Gauges (VOL, PWR):** DOS fill, 10 cells of `█`, lit cells
  in the readout's color, unlit cells `█` in `--bevel-dark`. NET steps
  `▂▄▆█`: lit in the readout's color, unlit in `--bevel-dark`. No NET
  gauge.
- **Thresholds:** PWR `--warning` <30%, `--critical` <15% (waybar's ≤
  values: `"warning": 29`, `"critical": 14`); NET `--critical` on
  disconnect (`NET: OFFLINE`).
- Hex colors inside pango spans or non-CSS files get a comment naming
  the token they mirror.

### Locked volume slider (decided Phase 1.2)

- Kept as a drawer: click VOL reveals `pulseaudio/slider`; it sits
  inside the VOL field.
- Horizontal gauge, **80×4px**: trough `--bevel-dark`, fill `--text`,
  no knob. Adwaita decoration removed on scale, trough, highlight and
  knob (`border`, `outline`, `box-shadow`, `background-image`). (The
  scale's border used to draw the tick frame; with ticks gone it has no
  job.)
- Mute empties the gauge (`zero-on-mute`, default). Mute itself is the
  `XF86AudioMute` key.
- **Scroll on VOL: 5% per step**, same as the media keys. Touchpad
  swipes on the open slider are uneven (waybar truncation bug, left as
  is — `PHASES.md`).

### Locked network picker (decided Phase 1.1, updated 2026-10-18)

- Click NET → the SITE-9 script `waybar/.config/waybar/scripts/net-menu`
  (`nmcli` + fuzzel). **Networks only** — the other network actions
  move to a future SITE-9 settings panel. No blank rows. Runs only when
  clicked; nothing left running.
- Top-right under the bar, 8px margins.
- **Opens instantly from NetworkManager's cached list** (`--rescan no`).
  **Refresh:** F5 in the menu (fuzzel `custom-1`, exit code 10 → the
  script restarts with `--refresh`, which rescans) or right-click NET
  (`--rescan yes`). A refresh normally takes ~1 s; one run took 12 s
  (NM's scan wait, likely from back-to-back test scans) — **left as is**
  (user, 2026-10-18). **After a successful connect the script starts a
  background rescan** (`setsid -f nmcli device wifi rescan`, all output
  to `/dev/null`) so the next open isn't short (user, 2026-10-18).
- fuzzel runs with `--keyboard-focus on-demand` (exit on focus loss is
  fuzzel's default).
- The script's lock is released before connecting to a saved or open
  network, so NET stays clickable during a connect; the new-network
  path holds it through the password prompt.
- **Closes** on: Esc, clicking NET again (toggle, tracks its own fuzzel
  only), clicking another window, or the pointer passing over a window
  (`follow_mouse = 1` moves keyboard focus there).
- **Pointer hand-back:** after fuzzel appears, the script moves the
  pointer to where it already is, so the bar gets it back and a second
  click on NET closes the menu. Only on the first menu of a NET click —
  not on the F5 restart and not on the password prompt (a row clicked
  with the mouse can leave the pointer over a window, and the nudge
  would then close the prompt; tested, 2026-10-18).
- **NET has no tooltip** (user, 2026-10-18 — it covered the menu).
- Row: `▂▄▆█  NAME  SEC`, padded columns, open networks show `OPEN`,
  names over ~24 chars cut with `…`. Connected network first, tagged
  **`[ACTIVE]`** (re-asked 2026-10-18: fuzzel can't dim part of a row,
  so "dim `connected`" wasn't possible; user kept `[ACTIVE]`).
- Wrong password: prompt reopens with placeholder `WRONG PASSPHRASE`,
  the failed profile is deleted; Esc cancels. **The password never goes
  on a command line or to disk in plain text** — it goes in through
  `passwd-file /dev/fd/3` (§6).
- **fuzzel colors (user, 2026-10-18 — mirrors the reference's drop-down
  list):** background `--field`; text, input and prompt `--text`;
  selected row `--panel` with `--text-bright`; match and
  selection-match `--text-bright`; placeholder and counter
  `--text-dim`; 1px flat `--bevel-dark` border; radius 0, selection
  radius 0; DepartureMono Nerd Font 11px, regular.
- Super+R stays on hyprlauncher until Phase 3.

### Locked terminal: kitty (Phase 2.1 — user, 2026-10-18; built round #10, `b3011ea`)

Picked on UNIT-1's render `2.1-kitty-field-P2-x3.png`:
- **Background `--field`**, text `--text`.
- **ANSI palette P2** — the classic DOS/VGA 16 colors, lightened only
  as far as needed to read on olive (bright green, yellow and cyan stay
  true DOS; bright black held ~3:1 so it stays darker than white).
  Each hex has a comment in `kitty.conf`:
  normal 0 `#000000` · 1 `#da9191` · 2 `#36bc36` · 3 `#cd9b69` ·
  4 `#9e9edf` · 5 `#d88ad8` · 6 `#24b6b6` · 7 `#aaaaaa`;
  bright 8 `#8a8a8a` · 9 `#ff7c7c` · 10 `#55ff55` · 11 `#ffff55` ·
  12 `#9b9bff` · 13 `#ff61ff` · 14 `#55ffff` · 15 `#ffffff`.
  `url_color` `#9b9bff` (P2 bright blue).
- **Cursor:** block in `--text`, `cursor_text_color background`,
  **no blinking** (user, 2026-10-18).
- **Selection: S1** — `--panel` + `--text-bright`, same as menus (user,
  2026-10-18).
- **Pane edges:** each pane is a recessed box inside the F3 frame
  (below): 1px, `--bevel-dark` top/left, `--bevel-light` bottom/right,
  the same in every pane (static). Focus is shown by Hyprland's window
  border, not by kitty. Bell border `--warning`. (Until round #11:
  split borders active `--bevel-light` / inactive `--bevel-dark` with
  `draw_minimal_borders yes`, which the margin now overrides.)
- **Padding 4px.** Font DepartureMono Nerd Font **`font_size 8.25`**
  (= 11px at kitty's 96 DPI, scale 1).
- `shell_integration no-cursor` (keeps the block cursor at the prompt),
  `url_style straight`.
- **Tab bar: T3** (user, 2026-10-18, picked from three renders) — on
  top, `tab_bar_style custom` with a small commented `tab_bar.py`.
  - The whole strip is `--panel`, margins included
    (`tab_bar_margin_width 3`, `tab_bar_margin_height 3 3`, margin color
    `--panel`) — no dark area after the last tab.
  - Each tab reads `▏ N:TITLE ▕` (upper-case title, regular weight).
    kitty draws the side edges itself, 1px each.
  - Bottom edge: a colored straight underline (SGR `4:1` + `58`),
    lowered with `modify_font underline_position 2px`.
  - Inactive tab: `--panel`, `--text`, light left edge, dark right and
    bottom edges. Active tab: `--field`, `--text-bright`, edges
    reversed (pressed in).
  - **No top edge** — kitty has no overline. Accepted with the pick.
  - Side effects, accepted with the pick: the side edges reach 1px
    below the bottom edge (kitty clamps the underline inside the cell),
    and every underline in the terminal (e.g. URL hover) sits 2px lower.
  - The strip is 14px tall (one text row), about half the height of
    waybar's buttons. Noted, not changed.
  - **A config reload (ctrl+shift+F5) doesn't apply tab-bar changes**;
    only a newly started kitty shows them.
- **Window frame: F3** (user, 2026-10-18 — picked on screen; built
  round #11, `8027ba9`). Like the VOX console: an **8px `--panel` frame
  around a recessed `--field` box**, bevelled like a pressed workspace
  tab (user: "top/left dark, right/bottom light"). Each split pane gets
  its own frame and box.
  - kitty: `window_margin_width 6`, `window_border_width 1px`,
    `draw_window_borders_for_single_window yes`; kitty's leftover
    pixels add 0–6px to the frame on some edges (cell rounding).
  - `kitty/.config/kitty/bevel.py` (a kitty watcher) recolors the
    border sides and paints the blank areas `--panel`. It wraps
    kitty's internal `kitty.borders.set_borders_rects` and falls back
    to kitty's own drawing on any error — **recheck after every kitty
    update** (internal API, may change).
  - Tab strip only with 2+ tabs (`tab_bar_min_tabs` stays 2; user
    declined the always-on strip).
  - Rejected: F2 (thick Hyprland border + kitty line — the line floats
    0–6px inside the frame) and F1 (impossible: kitty paints margins in
    the window's own background, §6).

### Locked window borders: Hyprland (Phase 2.6 — built round #10, `7ff55e8`)

- **No gradient** (user, 2026-10-18: Hyprland's default two-color
  gradient border was on every window).
- **Flat 1px border: active `--bevel-light`, inactive `--bevel-dark`**
  (user, 2026-10-18 — same as kitty's splits). Rounding 0, shadow off,
  blur off (§2/§3). Set as plain `"rgb(…)"` strings.
- **Grouped windows** (`group.col.*`, incl. locked) use the same two
  colors (round #11, `b2c32e8`). The **groupbar** (title strip of a
  window group) still has Hyprland's defaults — rounding 1,
  translucent off-palette colors, default font — against §2/§3; being
  decided in round #12 (theme it / turn it off).
- **On-screen color shift.** Hyprland draws its own colors a few values
  off: active `#667259` (set `#667359`), inactive `#242b1f` (set
  `#1f2719`); app surfaces are exact. It's an sRGB → gamma 2.2
  conversion on Hyprland-drawn colors only (§6). No CM setting fixes
  borders without shifting every app (tested round #11). Being decided
  in round #12: **pre-compensated hexes** `#667458` / `#192212` (exact
  on screen, commented as compensations, recheck on Hyprland updates)
  or accept the shift. Whatever is picked applies to every color
  Hyprland draws itself (borders, groupbar, background color).
- **Gaps and animations stay at Hyprland's stock values for now**
  (gaps `gaps_in 5` / `gaps_out 20`: ask later; animations: Phase 4 —
  current values recorded in `PHASES.md` Phase 4).

### Locked app theme: GTK3 (Phase 2.2 — user, 2026-10-18: "all leans")

- **G1: SITE-9's own GTK3 theme, written from the §3 tokens** — not a
  recolor of an existing theme (Adwaita-dark + overrides loses to
  Adwaita's selectors, §6; Chicago95's bevels are 2px with grey image
  assets). GTK4/libadwaita: none installed; covered when an app needs
  it.
- Widgets follow the look rules above: buttons, tabs and toolbars
  raised; entries, lists, views and menus recessed; active/pressed =
  recessed + `--text-bright`; selected rows `--panel` + `--text-bright`;
  tooltips like waybar's; scrollbars like the reference (raised `--panel`
  thumb, `--field` track, 12px).
- Hard rules inside the theme (§2): no `box-shadow`, `text-shadow`,
  `-gtk-icon-shadow`, gradients (`background-image: none`), blur or
  transitions; radius 0; 1px bevels; no off-palette outlines.
- Built round #11 (`gtk/` package: theme in
  `.local/share/themes/SITE-9/gtk-3.0/`, `settings.ini`).
- **User picks (round #11):** no title-bar buttons (decoration layout
  `:`); **check boxes and radio buttons both square** (recessed box,
  `--text-bright` mark; radio = filled square); **keyboard focus = 1px
  dotted `--text` box** inside the focused widget; **no text-cursor
  blink**; **disabled text `--text-dim`** (the one place it may sit on
  `--panel`).
- Choices UNIT-1 made, confirmed or changed in round #12: links
  `--text-bright` underlined; `.dim-label` in `--text` (dim not on
  panel); entries show no focus box (the caret marks focus); spinner is
  a still icon until Phase 4; no scrollbar arrows; menubar hover =
  pressed in. Placeholders `--text-dim` (GTK's named color
  `placeholder_text_color`).
- Settings (gsettings + `settings.ini`): `gtk-theme 'SITE-9'`,
  `color-scheme 'prefer-dark'`, font `DepartureMono Nerd Font 8.25`
  (= 11px, measured), `cursor-blink false`, `overlay-scrolling false`,
  `wm.preferences button-layout ':'`. Old values in `PHASES.md`
  round #11.
- **`xdg-desktop-portal-gtk` installed** — the Settings portal answers
  (waybar: "Discovered appearance 'dark'") and Firefox's file chooser
  is the themed GTK one.
- Known leftovers: Adwaita's symbolic icons are soft (2.5); GTK3
  `inset`/`outset`/`groove`/`ridge` frame styles shade colors (seen in
  the widget factory only).

### Locked Qt theme: Dolphin (Phase 2.3 — user, 2026-10-18: "all leans")

- **Q1: Kvantum** with a SITE-9 Kvantum theme (SVG + `.kvconfig`) from
  the §3 tokens — it can draw 1px two-tone bevels. Same widget rules
  as GTK above. (Not Q2 qt6ct + Fusion + stylesheet, not Q3
  kdeglobals colors on Breeze shapes.) Built round #11 (`kvantum/`
  package; SVG generated by `tools/make-svg.py`). Splitter 4px
  `--panel`; translucency, blur, shadows and state animations off.
- Selected with **`QT_STYLE_OVERRIDE=kvantum`** (documented upstream;
  upstream prefers a config tool like qt6ct — being confirmed in round
  #12) and **`QT_QPA_PLATFORMTHEME=gtk3`** (gives Qt the GTK font and
  file dialogs), both set in `hyprland.lua`.
- **Dolphin colors** come from a named KDE color scheme `SITE-9`
  (`kde/` package: `kdeglobals` + `SITE-9.colors`), selected in
  `dolphinrc` (`ColorScheme=SITE-9`; old value BreezeDark, backup
  `~/.config/dolphinrc.pre-site9.bak`). Sampled: view `--field`, frame
  `--bevel-dark` top/left, places `--panel`, selected tile `--panel` +
  white, no Breeze blue. KDE fades the places headers ("Places",
  "Devices") to `#959d8d` itself — no key reaches it; accepted.
- **Not covered:** hyprpolkitagent's password window — it's drawn by
  hyprtoolkit (Hyprland's own toolkit: rounded, dark grey, own
  animations), not Qt widgets. Being decided in round #12.

### Wallpaper (Phase 2.7 — pulled forward, built in round #12)

- User (2026-10-18): wants a wallpaper that matches, and **Hyprland's
  splash quotes and default wallpaper gone**. Picked **W1** (a SITE-9
  wallpaper made from the tokens) and handed the design to THE
  OVERSEER: "gritty, raw feel of Half-Life … go wild", with two
  suggestions — the nickname **`andr1cs`** and a **BMRF logo**. The
  user still picks the final version from UNIT-1's full-screen renders.
- **Concept — "facility wall"** (THE OVERSEER, mockup shown in chat
  2026-10-18): the desktop is a riveted wall inside SITE-9.
  - **Palette: tokens only.** Every pixel is one of the §3 tokens; grit
    and shading come from **ordered (Bayer) dithering** between them —
    the 1998 software-renderer look, no blends, no gradients.
  - **Wall:** `--field` base; large panels (240×180, an 8×6 grid) with
    1px recessed seams (dark line, light line beside it) and 2×2 rivets
    near each corner (light pixel top-left, dark bottom-right). A few
    panels a shade lighter (dithered toward `--panel`) for variety.
  - **Grime:** dithered `--bevel-dark` soot heavier toward the bottom and
    left edge, streaks running down from seams, sparse 1px
    `--bevel-light` scratches. All from a fixed random seed, so the
    image is reproducible.
  - **Stencil:** huge `SITE-9` in DepartureMono at a multiple of 11px
    (~264px), painted in `--bevel-light`, worn away in noisy patches
    (paint showing the wall through), with a stencil bridge cut through
    the middle of every letter. Painted before the seams, so seams run
    over it.
  - **Pipe:** a bevelled `--panel` pipe running under the bar with dark
    brackets — it shows in the 20px top gap above every window.
  - **Hazard band:** 45° `--warning` / `--bevel-dark` stripes along the
    bottom edge, worn — shows in the 20px bottom gap.
  - **Signage:** small painted text top-left in `--text-dim`:
    `◄ TEST CHAMBERS   LEVEL 3 // SECTOR C`.
  - **Placard** (bottom-right, a raised VOX panel with four screw
    heads): logo slot, `SITE-9` (`--text-bright`) / `RESEARCH
    FACILITY`, a seam, `OPERATOR ..... ANDR1CS`, `CLEARANCE .... LEVEL
    3`, a barcode strip and two unlit-looking status lamps
    (`--warning`, `--critical` — static).
  - **Logo:** the user supplies their own logo file, kept **outside the
    repo** (e.g. `~/.local/share/site-9/logo.png`). The script
    recolors it to the tokens with the same dither and wear, and
    places it in the placard slot; without the file the slot shows a
    plain recessed square.
  - **Variants to render:** V1 everything above; V2 calmer (no big
    stencil, lighter grime).
- **Built by a script, not by hand:** `wallpaper/tools/make-wallpaper.py`
  (or similar) in the repo, seeded, drawing at 1×, text with
  antialiasing off, output an indexed PNG holding only token colors.
  The finished PNG is written **outside the repo**
  (`~/.local/share/site-9/wallpaper.png`) because it may contain the
  logo; only the script is committed.
- Static only (§2); shown by the wallpaper tool picked in round #12.

### Typography & glyph findings (still valid)

- **Exact family name:** `DepartureMono Nerd Font` (no space). The
  spaced name only works through fontconfig fuzzy matching.
  Package: `otf-departure-mono-nerd` (AUR, Nerd Fonts patch v3.4.0).
- **Pixel grid:** 550 units per em, 50 per pixel → an **11px grid**.
  Crisp only at multiples of 11px (11, 22, …). Pick sizes on the grid.
- **Antialiasing off for DepartureMono, in every app** (user,
  2026-10-18; `fontconfig/` package, round #11 `aa3918f`): a fontconfig
  rule matching only DepartureMono (other fonts stay antialiased).
  Reason: Qt drew it half a pixel off horizontally (2-column strokes);
  hinting didn't help, antialias off did. Effects: Nerd icons (`◄ ⏻`)
  and `▂▄▆` are now hard-edged; kitty's text pixels didn't change.
- Only Regular is installed (Nerd Font, Mono and Propo variants).
  Synthetic bold smears (fails the pixel-crisp standard). Double-strike
  was tried and retired (see Locked look rules); in GTK3 its doubled
  copy also ignores pango span colors.
- What the font has: all Box Drawing and Block Elements, all Nerd Font
  MD and FA icons, progress-bar glyphs U+EE00–EE0B (one outlined
  continuous bar). **Not** in the font: `▮ ▯ ▰ ▱ ■ □`.
- Crispness at 11px (measured before antialiasing was turned off —
  soft edges below are now hard): text glyphs fully crisp. `█` is the sharpest bar
  glyph, with a faint ≤10% font-level fringe on its outer edges (left
  as is). `⏻` and `▂▄▆` have soft edges. `▌`, `▏`–`▉` and `┃` land on
  half pixels (soft). `░` is a soft dot texture at every size. Nerd
  icons render soft and slightly small next to the pixel text.
  Letter-spacing tweaks push glyphs onto fractional pixels — avoid.
- Emoji-default codepoints (e.g. `⚡` U+26A1) can come from a color
  emoji font; pin with U+FE0E or avoid. None installed as of
  2026-10-06.
- New glyphs must be confirmed present in the installed font itself and
  proposed as options, not picked. A glyph only available via a
  fallback font is a design question to raise.

### Retired (kept for reference)

- **HUD palette** (2026-09-20 → 2026-10-09): `--bg #15140f`,
  `--border #3a3626`, `--text #d6d0bd`, `--text-dim #8f8a76`,
  `--accent #5fae5a`. Gone from waybar and `fuzzel.ini` since round #8.
- **Corner ticks** (2026-10-06 → 2026-10-09): 9-slice `border-image`
  from an 11×11 SVG, `border: 1px solid transparent`,
  `border-image-slice: 5`, `border-image-width: 5px`, recolored with
  `-gtk-recolor(url("…-symbolic.svg"), success <hex>)`. +0px height.
  Proven to work; dropped with the HUD look.
- **Double-strike weight** (2026-10-06 → 2026-10-18):
  `text-shadow: 1px 0 0 currentColor`. See Locked look rules.
- **SCP influence**: now content only — the `FIELD:` labels, `SITE-9`
  and (until 2026-10-18) MET stayed as content, styled VOX; MET
  moves to the settings panel.

### What IS fixed regardless

**Shape language**
- Border radius: 0px. No soft rounded corners anywhere.
- Borders: thin (1px), hard. No soft shadows, ever. No gradients.

**Typography**
- Monospace, everywhere, no exceptions — a stated requirement, not a
  default. DepartureMono Nerd Font 11px regular (above). Verify actual
  rendering on this screen before finalizing any new use.

**Motion**
- Short, linear/snap transitions. No easing flourishes, no bounce, no
  multi-stage animations — abrupt and mechanical, not smooth.

### Sound (deferred, not in scope yet)
User wants to add sound later (UI feedback sounds, alerts). Don't build
anything that makes that awkward to bolt on later, but don't implement it
now — no audio dependencies, no hooks, until it's an actual phase.

## 4. Stack (current, confirm nothing here has gone stale)

- Compositor: Hyprland 0.56.2 (re-checked 2026-10-18). Started by hand,
  **not through uwsm**, so systemd's `graphical-session.target` is
  never active (§6).
- Bar: waybar — installed as **`aur/waybar-git`**, not `extra/waybar`.
  The fix for Hyprland's Lua dispatch (Waybar PR #5013) isn't in a
  tagged release yet: latest tag is still 0.15.0 (checked 2026-10-06).
  Recheck at each phase start; switch back to `extra/waybar` once a
  tagged release includes the fix. Background in `PHASES.md` Log
  (2026-09-21).
- Launcher: **hyprlauncher** 0.1.6 (Hyprland's first-party launcher,
  bound to Super+R in `hyprland.lua`). **fuzzel is installed** (round
  #7, from `extra`; exact version to be reported in round #8) and used
  **for the network picker only**; Super+R stays on hyprlauncher until
  Phase 3 decides the launcher. wofi 1.5.3 is also installed
  (maintenance status not checked).
  networkmanager-dmenu was installed in round #7, replaced by the
  SITE-9 `net-menu` script and **uninstalled** (`pacman -Q`: not found,
  2026-10-18).
- Notifications: **mako 1.11.0 — installed and running, no config**
  (found 2026-10-09). **libnotify isn't installed**, so there's no
  `notify-send`. Apps that talk to the notification service directly
  still show up: kitty does — Claude Code's "waiting for your input"
  notice appears through it (seen 2026-10-18). Unstyled, mako uses its
  upstream defaults (blue `#285577` background, white text, 2px
  `#4C7899` border) — off-palette; Phase 3 styles it. The network
  picker sends no notifications.
- Idle/lock: hypridle + hyprlock — **planned, not installed**.
- Wallpaper: none set — the screen shows Hyprland's default wallpaper
  and splash quotes (to be removed, round #12). hyprpaper: not checked
  yet (round #12 checks it against Hyprland's own `background_color`).
- Screenshot: grim + slurp + swappy (bound to Print) — grim is in use;
  slurp/swappy not checked.
- Terminal: **kitty 0.49.2** — kept (user, 2026-10-18; foot is no
  longer planned). Tabs and splits in use. SITE-9 config since round
  #10 (§5).
- File manager: **Dolphin 26.08.2 — Qt6/KDE**, so GTK theming doesn't
  reach it. No Qt theming set up (no qt6ct, Kvantum, breeze style,
  kdeglobals or `QT_*` variables). Available, maintained: kvantum
  1.1.8 (`extra`), qt6ct 0.11 (`extra`), breeze 6.8.0 (not installed).
  **kvantum 1.1.8-1 installed** (round #11) — §3 "Locked Qt theme".
  qt6ct not installed. Installed Qt platform-theme plugins: gtk3,
  xdgdesktopportal. plasma-integration not installed (so `kdeglobals`
  fonts don't apply; the gtk3 platform theme supplies the font).
- GTK: **GTK3 only — no GTK4, no libadwaita installed** (2026-10-18).
  GTK3 apps: Firefox, swappy, wofi, polkit-gnome, rustdesk-bin, waybar.
  **SITE-9 GTK3 theme live since round #11** (§3). Before that:
  `gtk-theme 'Adwaita'`, `color-scheme 'default'`, font Adwaita Sans
  11, cursor-blink true, overlay-scrolling true, button-layout
  `appmenu:close`. **gtk3-demos 1:3.24.52-2** installed as the test
  bench (`gtk3-widget-factory`).
- Browser: **Firefox 158** — uses its own built-in dark theme
  (`firefox-compact-dark`), not the system theme; a GTK theme only
  reaches its file and print dialogs.
- Portals: `xdg-desktop-portal` + `-hyprland` + **`-gtk` 1.15.3-1
  (installed round #11)** — Settings (dark-mode signal) and FileChooser
  now answer.
- Display manager: **sddm 0.21.0 is installed** (Phase 5's gate).
- Polkit agent: **hyprpolkitagent 0.2.0 — autostarted since round #10**
  (user's pick, 2026-10-18), launched directly from `hyprland.lua`'s
  autostart, not through its systemd unit (the unit waits for
  `graphical-session.target`, §6). Logged "registered polkit agent for
  session 2". Its password window is **hyprtoolkit**, not Qt widgets —
  it ignores Kvantum and the GTK theme (round #11). It reads
  `~/.config/hypr/hyprtoolkit.conf` (colors, two rounding sizes, fonts,
  icon theme; no bevels). Round #12 decides.
  **polkit-gnome** (installed, unused): GNOME no longer develops it and
  Fedora dropped it in F41 — treat as deprecated, don't use. Maintained
  alternatives: mate-polkit (GTK3), lxqt-policykit (Qt), polkit-kde-agent
  (KDE).
- Network: **NetworkManager 1.58.1** (wpa_supplicant backend), `nmcli`
  and `nmtui` present; iwd not installed, systemd-networkd disabled.

**Tool freedom (user, 2026-10-18):** SITE-9 isn't tied to waybar or
Hyprland — any package or service that's current, maintained and good
for the job is fine, as long as the Half-Life VOX theme carries on.
Don't switch working tools without a reason and the user's OK; do
check current options whenever a phase needs a new tool (e.g. the
settings panel and sidebar, which waybar can't build).

**Open stack question:** launcher — keep hyprlauncher on Super+R or move
it to fuzzel (already installed, already VOX-colored)? Phase 3 at the
latest. The user decides; don't install a planned tool or remove a
live one without asking.

## 5. What's already built

- **waybar** (`waybar/.config/waybar/`, stowed live with `stow -t ~`,
  restow with `-R` when files are added or removed). **VOX look as of
  round #8 (`105c8fb`, 2026-10-18)** — everything in §3 "Locked bar"
  and "Locked volume slider": layout A and L2, 30px, regular weight,
  tokens as hyphenated `@define-color`s, gauges and NET steps with
  `--bevel-dark` troughs, VOL field on `#volume` (the drawer group) so
  the open slider sits inside it, VOX tooltips. Phase 1 closed on it.
  - `scripts/net-menu` — the network picker (§3, §6).
  - CPU, RAM and MET removed in round #10 (`f96c6a8`); the `{x:>3}`
    width-spec comment now sits on VOL (VOL, NET and PWR use it).
- **fuzzel** (`fuzzel/.config/fuzzel/fuzzel.ini`, stowed): VOX colors
  (all 12 color keys; `message` → `--text`), radius 0, DepartureMono
  11px, `[key-bindings] custom-1=F5`.
- **kitty** (`kitty/.config/kitty/`, stowed, round #10 `b3011ea`):
  `kitty.conf` + `tab_bar.py` — everything in §3 "Locked terminal".
  Live dir was empty, nothing backed up.
- **hypr** (`hypr/.config/hypr/hyprland.lua`, **stowed since round #10**,
  `4472245`). The pre-stow live file is backed up at
  `~/.config/hypr/hyprland.lua.pre-stow.bak` (outside the repo). Still
  mostly Hyprland's stock example config, plus:
  - `scale = "1"` and the stock `XF86AudioMute` → `wpctl set-mute
    @DEFAULT_AUDIO_SINK@ toggle` bind (`locked = true, repeating =
    true`) — carried over unchanged; that bind is where mute lives.
  - Autostart (`91773c0`): hyprpolkitagent only. The stray `nm-applet`
    line and the terminal autostart are gone (user, 2026-10-18).
  - Flat 1px borders, rounding 0, shadow and blur off (`7ff55e8`, §3).
  - Gaps and animations untouched (stock values).
- **gtk** (`gtk/`, stowed `--no-folding`, round #11): SITE-9 GTK3 theme
  (`.local/share/themes/SITE-9/gtk-3.0/`) + `.config/gtk-3.0/settings.ini`.
  `.gitignore` had `*.local`, which also matched `.local/` folders —
  `!.local` added (`6d23a95`). Commit `d56061c`'s message claims the
  theme files but only `settings.ini` landed; `6d23a95` adds them.
- **kvantum** (`kvantum/.config/Kvantum/`, stowed `--no-folding`):
  `SITE-9/SITE-9.kvconfig`, `SITE-9/SITE-9.svg` (generated by
  `tools/make-svg.py`), `kvantum.kvconfig`.
- **kde** (`kde/`): `kdeglobals` (colors + fonts) and `SITE-9.colors`
  (a symlink to it). Selected in `~/.config/dolphinrc`, which isn't in
  the repo.
- **fontconfig** (`fontconfig/`, stowed `--no-folding`): DepartureMono
  without antialiasing (§3 Typography).
- **hypr** additions in round #11: group border colors; `QT_STYLE_OVERRIDE`
  and `QT_QPA_PLATFORMTHEME` env vars.
- **waybar** in round #11: VOL padding from `#volume` only (`3991e27`);
  the GTK theme's scale-knob block/margin cleared on the VOL slider
  (`6bc75c7`).
- Everything else starts from scratch.

## 6. Verified tooling facts

Behavior checked against the actual installed versions — not training
data. Recheck if the package version changes. Newest first.

**Round #11 findings (UNIT-1, 2026-10-18):**
- **Hyprland color management vs its own colors** (sampled: inactive /
  active border, kitty field, waybar panel/dark/field/light):
  - baseline, monitor `sdr_eotf = "srgb"` or `"gamma22"`, and
    `render.cm_enabled = false` (reload only): no change —
    borders `#242b1f` / `#667259`, apps exact.
  - `render.cm_sdr_eotf = "srgb"` or `"default"`: same as baseline.
  - `render.cm_sdr_eotf = "gamma22"` or `"auto"`: borders exact, **every
    app shifted** (kitty `303f25`→`2c3d20`, waybar `445435`→`425332`,
    `1f2719`→`192212`, `667359`→`667458`).
  - Baseline CM with border hexes **`#667458` / `#192212`**: borders
    and apps exact.
  - So THE OVERSEER's sRGB → gamma 2.2 reading of the shift holds, but
    the per-monitor `sdr_eotf` knob doesn't reach Hyprland-drawn colors.
    Accepted values: monitor `sdr_eotf`; `render.cm_sdr_eotf`
    srgb/gamma22/auto/default.
- **kitty 0.49.2 internals (source):** margins and blank areas are
  painted in the **window's own background** (the shader's DEFAULT_BG
  slot follows the window bg, even after OSC 11) — so a margin can't
  differ from the text area without patching. `draw_window_borders_for_single_window`
  exists (inactive color when the OS window is unfocused). kitty's
  leftover pixels sit outside its border box. A watcher can wrap
  `kitty.borders.set_borders_rects`; border rects with `border_type < 0`
  are top/left; slot 3 carries its own RGB.
- **Hyprland window rules** set via `hl.dsp.exec_cmd` accept
  `border_size` and `border_color` (one color = active only;
  `"rgb(a) rgb(b)"` sets both).
- **Hyprland groups:** `group.col.border_{active,inactive,locked_active,locked_inactive}`
  are `string|HL.Gradient`; defaults were translucent gradients
  (`66ffff00`, `66777700`, `66775500`, `66ff5500`). Groupbar defaults:
  enabled, rounding 1, gradients false, gradient_rounding 2,
  round_only_edges true, font_family empty, font_size 8, height 14,
  indicator_height 3, col.active `66ffff00`, inactive `66777700`,
  locked `66ff5500` / `66775500`, text white, blur false.
- **GTK3:** the theme loads in `gtk3-widget-factory` with no CSS
  warnings; font `8.25` = 11px (7px advance, two-color text); the
  placeholder color is the named color `placeholder_text_color`; at 0%
  volume Adwaita's 2px fill stub is gone (the gauge reads empty). The
  file chooser runs as class `xdg-desktop-portal-gtk`.
- **Kvantum 1.1.8:** no docs in the Arch package; upstream V1.1.8
  `INSTALL.md` / Theme-Config read. `QT_STYLE_OVERRIDE` is documented;
  upstream prefers a Qt config tool (qt6ct).
- **Dolphin (KF6) outside Plasma ignores `kdeglobals` colors**: with no
  scheme set it follows the dark-mode signal to Breeze/BreezeDark, and
  its own `dolphinrc` had `ColorScheme=BreezeDark`. A named scheme file
  (`SITE-9.colors`) fixes it.
- **Qt draws DepartureMono half a pixel off horizontally** (2 columns
  per stroke). `hintstyle full` and gsettings `font-hinting full` don't
  help; `antialias=false` does. fontconfig's `50-user.conf` includes
  `$XDG_CONFIG_HOME/fontconfig/conf.d`.
- **hyprpolkitagent 0.2.0 = hyprtoolkit 0.6** (own renderer). Config:
  `~/.config/hypr/hyprtoolkit.conf`; keys seen: background, base,
  alternate_base, text, bright_text, accent, accent_secondary,
  rounding_large, rounding_small, font_family, font_family_monospace,
  h1_size–h3_size, small_font_size, icon_theme. Has opacity/geometry
  animations.
- **Session env:** env vars set in `hyprland.lua` don't reach
  D-Bus/systemd-activated apps by themselves; UNIT-1 pushed the QT_*
  vars into the activation environment by hand for this session only.
- **Test input:** Hyprland's `send_shortcut` works for sending keys to
  test windows. Never to the user's own windows — Space in Firefox's
  file dialog confirmed it and opened a file in the user's browser tab
  (round #11 mishap; `AGENTS.md` rule).

**Round #10 findings (UNIT-1, 2026-10-18; math by THE OVERSEER):**
- **Versions:** kitty 0.49.2, Hyprland 0.56.2, hyprpolkitagent 0.2.0.
- **kitty tab bar:** every key used is in the installed `conf.html` —
  `tab_bar_style custom` (loads `draw_tab` from `tab_bar.py` in the
  config dir), `tab_bar_margin_width`, `tab_bar_margin_height`,
  `tab_bar_margin_color`, `modify_font underline_position`,
  `url_style straight`, `selection_*`. `tab_bar.py` can call
  `screen.apply_sgr(…)`, which is how the colored underline (SGR
  `4:1;58…`) is drawn. kitty has **no overline**. The underline is
  clamped inside the cell, so 2px and 3px positions look the same.
  `modify_font underline_position` moves **every** underline. A config
  reload doesn't rebuild the tab bar — only a new kitty does. kitty's
  only stderr line is the known missing-portal message.
- **Hyprland `general.col.*_border`** accepts `string|HL.Gradient`
  (`hl.meta.lua`) — a plain `"rgb(…)"` string gives a flat color.
  `hyprctl getoption` after reload: border_size 1, active `ff667359`,
  inactive `ff1f2719`, rounding 0, shadow false, blur false;
  `decoration.glow.enabled` was already false. `hyprctl configerrors`
  empty. `group.col.*` unset → Hyprland's default group colors.
- **Hyprland border color shift:** with color management on
  (`render.cm_enabled true`, monitor preset `srgb`), Hyprland draws its
  own border colors slightly off — sampled active `#667259` (set
  `#667359`), inactive `#242b1f` (set `#1f2719`). App surfaces (kitty)
  come out exact. Setting `sdr_min_luminance = 0` changed nothing
  (reverted). **Cause (THE OVERSEER's arithmetic):** every sampled
  channel equals the set value decoded with the piecewise sRGB curve
  and re-encoded with gamma 2.2 — e.g. `0x1f`→`0x24`, `0x27`→`0x2b`,
  `0x19`→`0x1f`, `0x73`→`0x72`; the dark end shifts most. The current
  wiki lists a per-monitor `sdr_eotf` (`default` / `gamma22` / `srgb`;
  `default` follows `render:cm_sdr_eotf`). **Tested round #11: it
  doesn't reach Hyprland-drawn colors** (see round #11 findings).
- **hyprpolkitagent's systemd user unit doesn't start here:** it waits
  for `graphical-session.target`, which stays inactive because
  Hyprland isn't launched through uwsm. Starting the binary directly
  from the autostart works.
- **waybar** after the trim: log clean, bar 1920×30.

**Round #9 findings (UNIT-1, 2026-10-18):**
- **kitty 0.49.2** (options checked in the installed
  `/usr/share/doc/kitty/html/conf.html`): at scale 1 kitty uses 96 DPI
  (measured) — `font_size 8.25` gives an exact 11px em and 7×14 px
  cells; text rows contain only exact palette colors (no blends). Nerd
  icons (◄ ⏻) stay slightly soft. kitty's own box/block drawing and the
  font's glyphs (`symbol_map U+2500-U+259F`) are pixel-identical —
  default kept. Shell integration switches the cursor to a thin bar at
  the prompt unless `shell_integration no-cursor`. `tab_separator`
  doesn't take `{fmt…}` codes (prints them); `tab_title_template`
  does. Session-file keywords `focus_matching_window` and `focus_tab`
  work.
- **GTK3** picks up a theme from `$XDG_DATA_HOME/themes` via
  `GTK_THEME` (scratch-only proofs possible). An Adwaita-dark base with
  plain overrides loses: Adwaita's more specific selectors
  (`window.background`, `button.flat`, button radius) win, so buttons
  stayed rounded — a from-scratch theme avoids the fight.
- **Hyprland:** floating windows show a rounded corner and the default
  gradient border (seen live; fixed in 2.6, round #10).
- The live `hyprland.lua` also autostarted `$terminal` (besides the
  stray `nm-applet` line) — both dropped in round #10.

**Round #8 findings (UNIT-1, 2026-10-18):**
- **Versions:** fuzzel 1.15.0-1, waybar-git 0.15.0.r1019.g3672eee-1,
  gtk3 3.24.52-2.
- **GTK3 `@define-color`** accepts hyphenated names (`@bevel-light`
  renders `#667359`).
- **GTK3 tooltip node** is `tooltip` (and `tooltip label`) — waybar's
  `waybar-styles(5)` doesn't name it; confirmed in Adwaita's CSS inside
  the installed libgtk. Adwaita gives it `text-shadow: 0 1px black`,
  radius 5px, white text and an rgba(0,0,0,.8) background.
- **Adwaita `button`** (gresource in `/usr/lib/libgtk-3.so.0`):
  `text-shadow: 0 1px rgba(255,255,255,0.77)` and
  `transition: all 200ms cubic-bezier(0.25,0.46,0.45,0.94)`. The old
  double-strike rule had been hiding the text-shadow.
- **A drawer group's CSS node** (`#volume` for `group/volume`) can carry
  a module's field, so the revealed slider sits inside the frame.
- **`nmcli device wifi rescan`** (1.58.1): returns in ~0.02 s, rc 0
  (the man page doesn't say). Requests 15–24 s after a scan are held
  and run late, not dropped (seen via the device's `LastScan` D-Bus
  property); one 40 s after a scan ran in 1.8 s. It can refuse with
  "Scanning not allowed at this time". Detached with `setsid -f …
  </dev/null >/dev/null 2>&1`, nothing is left running (pgrep).
- **fuzzel `--search=TEXT`** pre-fills the filter — handy for test
  screenshots.
- `--rescan yes` once took 12.3 s (NM's scan wait).

**Round #7 findings (UNIT-1, 2026-10-18):**
- **Pointer focus on new layers (Hyprland 0.56.2):** when fuzzel maps,
  Hyprland sends it `wl_pointer.enter` even though the pointer is
  outside it (logged at (167, −23), above its surface, pointer still on
  NET). Waybar gets `leave`, so the cursor turns into fuzzel's arrow and
  the next click goes to fuzzel. **Fix:** once `hyprctl -j layers` shows
  fuzzel's pid, `hyprctl dispatch 'hl.dsp.cursor.move(hl.get_cursor_pos())'`
  (checked in `hl.meta.lua`: `HL.DspCursorNamespace.move`,
  `hl.get_cursor_pos(): HL.Vec2`) → waybar gets `enter` and the hand
  cursor back; fuzzel keeps keyboard focus.
- **`follow_mouse = 1`:** the pointer passing over a window moves
  keyboard focus to it, so fuzzel (exit on keyboard-focus loss) closes.
  That's also why the pointer nudge is only safe when the pointer is
  known to be on the bar.
- **A non-exclusive scratch waybar** (`"layer": "overlay"`,
  `"exclusive": false`) is placed below the live bar's reserved zone
  (y=30), not over it.
- **Waybar's `"name"` key** renames the CSS window node, so
  `window#waybar` rules stop matching. Don't use it.
- **GTK3 honours per-side `border-*-color`** on waybar's nodes
  (pixel-sampled): raised top/left `#667359`, bottom/right `#1f2719`;
  recessed reversed. The corner pixel where a light side meets a dark
  side is blended (`#3a4630`, GTK antialiasing) — accepted.
- **nmcli (NetworkManager 1.58.1):**
  - `nmcli device wifi list` rescans by default if the AP list is over
    30 s old (`nmcli(1)`); that scan hung ~30 s twice. `--rescan no`
    takes 0.04 s; `--rescan yes` ~1 s when it doesn't hang.
  - Right after a reconnect the cached list can be thin (1 AP instead
    of 10).
  - `nmcli connection up uuid … passwd-file /dev/fd/3` takes the
    password from a file descriptor — nothing in argv (checked with a
    watcher logging every nmcli argv).
  - Wrong password → `Error: Connection activation failed: Secrets were
    required, but not provided`.
  - A profile created by the picker matches a hand-made one except
    runtime seen-bssids and `auth-alg` left at its default (open).
- **fuzzel:** in dmenu mode, `custom-1`…`custom-19` key bindings exit
  with codes 10…28; no default binding uses F-keys;
  `fuzzel --check-config` validates the file. In `[colors]`, `match` and
  `selection-match` are text colors — there's no match background
  (THE OVERSEER, Arch `fuzzel.ini(5)`, 2026-10-18).

**Machine (2026-10-09):**
- `man` isn't installed (no man-db). Read man pages with
  `zcat /usr/share/man/man<N>/<page>.<N>.gz`.
- `pacman -F` (file database) isn't synced — needs `sudo pacman -Fy`
  before use. Use `pacman -Ql` on installed packages instead.

**Hyprland 0.56.2 (Lua config):**
- `hyprctl dispatch` takes a Lua dispatcher expression with a table
  argument, e.g. `hyprctl dispatch 'hl.dsp.cursor.move({ x = 135, y =
  18 })'` — not positional args.
- Dispatcher/API stubs for checking names: `/usr/share/hypr/stubs/hl.meta.lua`.
- **`hl.dsp.exec_cmd(cmd, { rules })` works through `hyprctl dispatch`**
  and applies window rules to what it launches, no config edit needed.
  Tested 2026-10-09: `hyprctl dispatch 'hl.dsp.exec_cmd("kitty --class X
  …", { float = true, size = "720 480", move = "monitor_w-728 44" })'`
  → floating kitty at 1192,44, 720×480. `move` accepts `monitor_w`
  expressions.
- Window rules can't move a **layer surface** (launchers, bars) — only
  the app's own anchor/margin options can.

**Network & menus (2026-10-09):**
- **networkmanager-dmenu** (tried in round #7, uninstalled
  2026-10-18): no option to hide its action rows or the blank,
  clickable separator rows — why it was replaced by `net-menu`. Its
  source notes are in git history if ever needed.
- **fuzzel, observed 2026-10-09:** default width is 30 characters (rows
  get cut off). With the default `keyboard-focus=exclusive`, clicking
  another window **doesn't** close it; `keyboard-focus=on-demand` +
  `exit-on-keyboard-focus-loss` (default yes) is the documented way to
  close on focus loss. Click-away works in the built picker; which mode
  `net-menu` uses is to be reported in round #8.
- **NetworkManager permissions** (`nmcli general permissions`):
  network-control, wifi.scan and settings.modify.own are `yes` for the
  user, so any picker can scan and connect **without a polkit agent**.
- `extra/network-manager-applet` 1.36.0 does SNI/tray via `--indicator`,
  but depends on Canonical's **libappindicator** (unmaintained upstream,
  not the maintained libayatana-appindicator) — treat as deprecated,
  don't use.
- `extra/fuzzel` 1.15.0 (upstream man page, checked before install):
  `anchor=top-right` with `x-margin`/`y-margin` places it under the
  bar (built and seen; which edge `y-margin` counts from wasn't
  reported). Defaults are off-spec: **Solarized
  light colors** (background `fdf6e3`) and **`border-radius` 10** —
  rounded, breaks §3. Any use must override radius (0) and colors.
  Default layer `overlay`. No text-shadow, so no double-strike weight.
- **hyprlauncher 0.1.6 `-m` / `--dmenu`** (checked live 2026-10-09):
  opens a 400×260 layer surface centred on screen (760,410) through the
  already-running daemon. No position or password flags; config keys
  are only `ui:window_size`, `general:grab_focus` and finder settings.
  Times out with no pick → exits 124 and closes cleanly. **Unconfirmed:**
  that a picked line comes back on stdout (no way to send keys to a
  layer surface from UNIT-1's side).
- **pinentry 1.3.3:** `pinentry-gtk` and `pinentry-qt` link cleanly;
  `pinentry-gnome3` is missing a library — don't use it.
- **wofi 1.5.3** is installed; networkmanager-dmenu supports it natively
  (`-P` masks the passphrase) and it can anchor top-right. Upstream
  maintenance not checked.

**waybar-git 3672eee0** (source + installed `waybar.5`, 2026-10-06/09):
- **fmt width specs** (`{usage:>3}` etc.) work on cpu, memory,
  pulseaudio, network and battery values — all integers in the source.
  `min-length` pads the whole label instead (moves icons and bars).
- **`pulseaudio/slider` with `"orientation": "vertical"`** renders
  bottom-up (inverted). Unstyled, its trough gets Adwaita's light
  `#ccc6c1` border and the highlight a blue `#185fb4` outline.
- **Workspace buttons on hover** get Adwaita's box-shadow (a 1px light
  line along the top edge) unless overridden — fixed with
  `box-shadow: none` on `#workspaces button:hover` (cf4319a).
- **Natural bar height** (no `height` key, 11px text + corner ticks):
  **24px**, with no slider or with a horizontal 4px slider trough. The
  old vertical 24px trough was what forced 36px. A drawer's hidden
  slider still counts toward the bar's height.
- **`pulseaudio` scroll:** scrolling on the module changes volume
  natively; `scroll-step` defaults to 1.0 (%). `reverse-scrolling` and
  `smooth-scrolling-threshold` exist for touchpads. (Media keys use 5%.)
- **`pulseaudio/slider` `zero-on-mute`** defaults to true — mute empties
  the gauge.
- **`memory` supports `{icon}`** with `format-icons` even though the man
  page's replacement list doesn't mention it (memory/common.cpp).
- **Battery `format-<status>`:** the status is lowercased, so
  `format-charging` is valid. A charging battery at 100% reports
  "Full" and falls back to `format-full` / `format`.
- **`network` `{icon}`** is indexed by signal strength.
- **`custom/` `exec` runs via `sh`**, so shell syntax works but quoting
  in JSONC needs escaping (the MET `awk` round-trips correctly).
- **Tray with no items is hidden** — its frame only shows when an app
  has a tray icon.
- **`format-icons` also accepts threshold objects** in waybar-git
  (ALabel.cpp:222), but it's undocumented in the man page — don't use
  it until it's documented in a tagged release.
- **Text-shadow placement** (history — double-strike is retired):
  applying it on `window#waybar label` covered bar text and left
  tooltips alone.
- **Group orientation** defaults to `"orthogonal"`, which makes a group
  *vertical* on a horizontal bar. Every group must set
  `"orientation": "horizontal"` (or `"inherit"`).
- **Group CSS name** is the part after `group/` — `group/net` is styled
  as `#net`. Groups can nest.
- **Drawer packing:** in a drawer group only the first module (the
  leader) is visible; every later module goes into the revealer and is
  hidden until revealed.
- **Clicks:** a module only takes button presses if it has an
  `on-click*` key (or the code forces clicks on). `custom/` modules
  default to not taking clicks, so a static label with no `on-click`
  passes clicks through to its group. A leader with *any* `on-click*`
  bound swallows the drawer's reveal click (2026-09-21 finding).
- **State classes** (`.warning`, `.critical`, `.disconnected`, …) are
  set on the module's own widget. GTK3 CSS has no parent selector, so a
  group's frame or a sibling module can't react to them.
- **`always-visible-class`** needs a CSS class on the module; a static
  `custom/` module can only get a class from JSON output, i.e. an
  `exec`. Not useful for static labels.
- **`format-icons` level indexing:** with N entries, the index is the
  level scaled to N, capped at N−1. Prebuilt bar strings use N entries
  where entry i lights i+1 cells. Pango markup inside icon strings is
  passed through.
- **`custom/` with `"interval": "once"` and no `exec`** draws once and
  never starts a process.
- **GTK3 `text-shadow`** (history): paints the shadow pass first, then
  the real text on top, and the shadow ignores pango span colors.
