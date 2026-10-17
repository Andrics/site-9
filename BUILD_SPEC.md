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
show up.

**Exception — double-strike text weight (user-approved 2026-10-06).**
Exactly `text-shadow: 1px 0 0 currentColor` is allowed: zero blur, 1px
horizontal offset, same color as the text. It renders as a 1px-wider
stroke (the font has no bold), not as a shadow, and it's static with
negligible cost. Allowed for font weight only. Any other `text-shadow`,
any blur, any offset in another direction or color, and any
`box-shadow` stay banned.

## 3. Design language: Half-Life / Black Mesa

> **Under revision (user, 2026-10-09): the VOX console look everywhere.**
> The user wants the visual style of
> [suchipi/half-life-vox-console](https://github.com/suchipi/half-life-vox-console)
> (Valve-VGUI olive panels, two-tone bevels) applied system-wide, not
> just the terminal — the current HUD look "isn't doing it". Options
> and picks are in `PHASES.md` → "Design pivot". **Until picks are
> locked, everything below stands** and nothing gets restyled. Behavior
> rules (picker, slider, layout, MET, thresholds) are unaffected.

Primary references — go look at both before making style calls:
- **Black Mesa Research Facility** (Half-Life) — 1990s institutional-
  industrial: keycard/badge systems, stenciled warning labels, hazard
  tape, beige/olive-drab hardware, monochrome CRT terminal readouts, the
  HEV suit's amber HUD.
- **SCP Foundation report aesthetic** — typewriter/monospace text,
  redacted black bars, clinical bureaucratic document tone, site/unit
  numbering, classification-stamp styling.

Net result: serious, raw, work-focused. Nothing soft, nothing playful,
nothing decorative for its own sake.

**Palette, exact shade of the accent color, and specific fonts are NOT
decided here** — they're personal choices, made by asking the user, not
assumed by the agent. See `PHASES.md` Phase 1 for the open questions and
where decisions get recorded once made. Don't invent a palette and present
it as done — propose 2–3 concrete options and ask which lands.

### Locked palette (decided Phase 1 — 2026-09-20)

Fusion direction: HEV-style green as the primary signal color, Black Mesa
institutional olive/tan as the structural base.

| Token | Value | Use |
|---|---|---|
| `--bg` | `#15140f` | main background, warm near-black |
| `--border` | `#3a3626` | structural borders, module dividers |
| `--text` | `#d6d0bd` | primary text |
| `--text-dim` | `#8f8a76` | inactive/secondary text |
| `--accent` | `#5fae5a` | primary accent (HUD green) |
| `--warning` | `#c98a3c` | warning state |
| `--critical` | `#b8452e` | critical state |

Font: Departure Mono Nerd Font (`otf-departure-mono-nerd`, AUR — not
`[extra]`, Nerd Fonts patch v3.4.0) — swapped 2026-09-21 from JetBrains
Mono Nerd Font per Overseer direction, applied to waybar. Carry this font
into every later phase rather than re-deciding per app.

- **Family confirmed by the user 2026-10-06**, with an ask for a bolder,
  MS-DOS / terminal blocky feel — met by the 11px + double-strike lock
  below. Live on the bar since 2026-10-09.
- **Exact family name:** `DepartureMono Nerd Font` (no space). Use that
  in CSS; the spaced name only works through fontconfig fuzzy matching.
- **Pixel grid:** 550 units per em, 50 units per pixel, so the font is
  drawn on an **11px grid**. It renders pixel-crisp only at multiples of
  11px (11, 22, …). Other sizes (e.g. the current 13px) give uneven
  strokes. Pick sizes on the grid unless a deliberate exception is
  decided and recorded here.
- **Locked 2026-10-06: 11px, double-strike weight** (`text-shadow: 1px
  0 0 currentColor`, the §2 exception). Crisp 2px strokes, the
  MS-DOS/terminal blocky look the user asked for.
- **Weight background:** only Regular is installed (confirmed with `fc-list`
  2026-10-06: Regular in the Nerd Font, Nerd Font Mono, and Nerd Font
  Propo variants). Tested ways to look bolder, at 11px:
  - Synthetic bold (`font-weight: bold`): bolder but smeared, with gray
    fringe pixels. Fails the pixel-crisp standard.
  - Double-strike (`text-shadow: 1px 0 0 currentColor`): crisp 2px
    strokes, no layout change. **But in GTK3 the doubled copy is always
    drawn in the widget's CSS color and ignores pango span colors**, so
    anything colored by a span (the dim `FIELD:` labels, dim bar parts)
    gets a bright extra column. Also uses the `text-shadow` property,
    which §2 rules out unless an exception is decided.
  - 22px: an exact 2× of 11px — bigger, not bolder.
  Weight decision is in `PHASES.md` (Phase 1 plan review).

### Locked module framing & state color (decided Phase 1 — 2026-09-21)

First on-screen pass read as a generic dark-mode bar with one green accent,
not Half-Life/SCP — traced to missing module separation and no
state-driven color use. Direction chosen: primarily bracketed-HUD framing
+ HEV-style state color, with SCP report influence kept to labeling only
(not structural — the module boxes already provide separation a hairline
treatment would have given).

- **Framing:** every module gets its own frame, small gap between frames
  so they read as discrete panel segments rather than one continuous
  strip. **Frame style updated 2026-10-06: corner ticks** (5px L-shaped
  ticks at each corner, technique below) instead of full rectangles.
  **Workspace tabs get corner ticks too** (user, 2026-10-09): each
  number is its own ticked tab; the active tab's ticks and number are
  `--accent`.
- **State color (updated 2026-10-06):** each readout is one color — label,
  icon, bar fill, value, and frame ticks all default to `--text`/
  `--border` and the **whole readout** shifts to `--warning` or
  `--critical` when the module is in a flagged state (HEV-style: the
  entire reading turns amber/red). `--accent` marks the active
  workspace. Thresholds (adjustable once seen live): PWR `--warning`
  <30%, `--critical` <15% — in waybar's ≤ terms, `"warning": 29`,
  `"critical": 14`; NET `--critical` on disconnect.
- **Fixed-width values:** percentages are padded to a fixed width so a
  readout doesn't shift sideways when a value crosses 9→10 or 99→100.
- **Labels (updated 2026-10-06):** `FIELD: value` formatting, uppercase
  label — **same color as its value**, no separate dim color. Replaces
  the original dim-label rule: with the double-strike weight, GTK3 draws
  the doubled stroke in the module color and ignores span colors, so
  dim labels would come out two-tone (see Weight above). The SCP report
  influence is carried by the `FIELD:` format, the `SITE-9` tag, and the
  mission clock.
- Outer bar getting a top/bottom hairline rule (echoing a report-page
  header) is a nice-to-have, not required.

Status: full-box version built 2026-09-21; corner ticks and one-color
readouts built and live since 2026-10-09.

**Corner ticks — proven feasible (probe, 2026-10-06):** 9-slice
`border-image` from an 11×11 SVG with 1px L-shaped corners and
transparent edges: `border: 1px solid transparent`,
`border-image-slice: 5`, `border-image-width: 5px`,
`border-image-repeat: stretch`. Ticks measured 5px long, 1px thick,
exact color, and add **0px** to the bar height. State colors via one
SVG named `*-symbolic.svg` and `-gtk-recolor(url("…"), success <hex>)`
(amber swap tested). Fallback if recoloring ever breaks: one plain SVG
per state with the color hard-coded. Relies on gdk-pixbuf's SVG loader
(present: glycin-svg 2.1.5 with librsvg 2.62.4). Static, nothing
animated — §2-clean.

### Icon direction (decided Phase 1 — 2026-10-06)

HUD/gauge-style glyphs for the VOL/NET/PWR modules: boxy, segmented or
bracket-like forms that lean into the HEV HUD — **not** the default
rounded, Font-Awesome-style icon-font look. Chosen over minimal outline
glyphs and over going icon-less.

- Icons and the value bars (content-density pass) are **one
  visual system**: same blocky, geometric register. Don't pick them
  independently.
- What the font actually has (checked 2026-10-06 with `fc-query` and
  `pango-view` renders): all Box Drawing (128/128) and Block Elements
  (32/32) characters, all Nerd Font MD and FA icons, progress-bar glyphs
  U+EE00–EE0B. **Not** in the font: `▮ ▯ ▰ ▱ ■ □` — don't use them,
  they'd only render via a fallback font. Nerd Font icons render
  soft-edged and slightly small next to the pixel text.
- **Crispness at 11px (measured 2026-10-06 by counting partial
  pixels):** `█` (full block) is the sharpest bar glyph, but not
  perfectly crisp: the font's own `█` has a faint ≤10% fringe on its
  outer edges (top/bottom ~8–10%, left ~6%; confirmed in a bare
  `pango-view` render, so it's the font, not waybar). Left as-is
  (THE OVERSEER, 2026-10-09 — barely visible at 1x; the user can reopen
  it, the alternative being antialiasing off for this font). Text glyphs measure fully crisp
  (0 partial pixels). `⏻` and the `▂▄▆` steps have soft edges. `▌`, the other partial blocks `▏`–`▉`, and `┃` land on half
  pixels and come out soft-edged (`▌` is 3.5px wide). `░` is a soft dot
  texture at every size tested (11/22/33px). Letter-spacing tweaks push
  glyphs onto fractional pixels — avoid them.
- Watch emoji-default codepoints (e.g. `⚡` U+26A1): Pango can draw them
  from a color emoji font. Pin them with U+FE0E or avoid them. (No color
  emoji font is installed as of 2026-10-06, so `⚡` currently renders as
  Departure's own small, thin text glyph.)
- **Locked 2026-10-06 (user's picks):**
  - VOL: `◄` U+25C4, static. PWR: `⏻` U+23FB. NET: signal steps
    `▂▄▆█` (U+2582/2584/2586/2588), lit steps in the module color,
    unlit in `--border`. NET gets no separate bar.
  - Bars (VOL, PWR, CPU, RAM): **DOS fill** — 10 cells of `█`, lit
    cells in the module color, empty cells `█` in `--border` (dark
    trough). Not `▌` segments (soft at 11px) and not `░` (soft, and
    busy under double-strike). Accepted side effect: one 1px column in
    the module color right after the bar's end (double-strike
    overhang).
  - Charging: the `PWR:` label becomes `CHG:` while charging. No
    lightning glyph.
  - Readout order: icon, label, bar, value — e.g. `◄ VOL: ██████████
    60%`, `▂▄▆█ NET: 82%`, `⏻ PWR: ██████████ 18%`.
- New glyphs later must still be confirmed present in the installed
  font (check the font itself, not a cheat-sheet) and proposed as
  options, not picked.
- If a good glyph only exists via a fallback font, that's a design
  question to raise, not something to quietly wire in.

### Locked bar layout & content (decided Phase 1 — 2026-10-06)

- **Layout (L2):** left — `SITE-9` tag, workspaces. Center — clock,
  mission clock. Right — CPU, RAM, VOL, NET, PWR, tray.
- **Mission clock (MET):** system uptime as `T+DDD:HH:MM`, updated every
  60s. No seconds (they'd sit stale between updates).
- **Tray:** one frame around the whole tray, icons at 14px. Tray icons
  keep their app colors.
- **Height: 30px**, set explicitly (user, 2026-10-09 — back to the
  original spec). The earlier 36px came only from the vertical slider
  trough; the bar's natural height is 24px, and 30 gives the frames a
  gap from the bar edge.
- **Active workspace tab** stays `--accent` (ticks and number) while
  hovered (2026-10-09).

### Locked volume slider (decided Phase 1.2 — 2026-10-09)

- Kept as a drawer: click VOL reveals `pulseaudio/slider`.
- **Horizontal gauge, 80×4px** trough in `--border`, fill in **`--text`
  cream** (one-color readout — VOL is cream everywhere), no knob, inside
  the existing tick frame. Adwaita decoration removed: trough,
  highlight and knob get `border: none`, `outline: none`,
  `box-shadow: none`, `background-image: none`. The scale itself
  (`#pulseaudio-slider`) **keeps its border — that border draws the tick
  frame** — and only clears outline, box-shadow and background-image
  (corrected 2026-10-09; the first brief wrongly said border too).
- Mute empties the gauge (`zero-on-mute`, default). Mute itself stays
  on the `XF86AudioMute` key.
- **Scroll on VOL: 5% per step**, same as the media keys.

### Locked network picker (decided Phase 1.1 — 2026-10-09)

- Click NET → a **SITE-9 script** (`nmcli` + **fuzzel**) — replaces
  networkmanager-dmenu (user, 2026-10-09: the menu shows **networks
  only**; its other actions move to a SITE-9 system settings panel,
  built later). List under the bar, top-right, 8px margins; masked
  passphrase via fuzzel's password mode.
- **No blank or non-network rows** — every row is a network.
- **Closes when you click away** (another window) and when NET is
  clicked again (toggle). Esc closes too.
- Row format: `▂▄▆█  NAME  SEC`, bars first, columns padded so they line
  up; connected network listed first and tagged `[ACTIVE]`. Menu width
  fits the rows; long names truncated with `…` so the bars are never
  cut off.
- Signal as **`▂▄▆█`**, matching NET — not the Nerd wifi glyphs.
- Wrong passphrase: the prompt reopens with the placeholder
  `WRONG PASSPHRASE`; Esc cancels and the failed profile is deleted.
- The passphrase never goes on a command line (argv) or to disk in
  plain text.
- **fuzzel stopgap styling** (until Phase 3 refines the same file):
  locked tokens only — DepartureMono Nerd Font 11px, background `--bg`,
  text `--text`, 1px `--border` border, radius 0, selected row
  `--border` background with `--text`, match highlight `--accent`,
  placeholder/counter `--text-dim`. Light weight (fuzzel has no
  double-strike) — a Phase 3 question.
- Super+R stays on hyprlauncher until Phase 3; fuzzel is installed for
  the picker only for now.

### What IS fixed regardless of which palette gets picked

**Shape language**
- Border radius: 0px, or at most 1–2px if 0 looks visually broken
  somewhere. No soft rounded corners anywhere.
- Borders: thin (1px), hard, high-contrast. No soft shadows, ever.
- No gradients.

**Typography**
- Monospace, everywhere, no exceptions — this is a stated requirement,
  not a default. Font: Departure Mono Nerd Font (see §3 locked palette) —
  whatever's picked, verify actual glyph rendering at bar-scale text size
  looks right on this specific screen before finalizing, don't just trust
  it on name recognition. Locked: 11px with double-strike weight (§3
  font notes above). Sizes on the 11px grid.

**Motion**
- Short, linear/snap transitions. No easing flourishes, no bounce, no
  multi-stage animations. Motion should feel abrupt and mechanical, not
  smooth — consistent with "raw, no soft edges."

### Sound (deferred, not in scope yet)
User wants to add sound later (UI feedback sounds, alerts). Don't build
anything that makes that awkward to bolt on later, but don't implement it
now — no audio dependencies, no hooks, until it's an actual phase.

## 4. Stack (current, confirm nothing here has gone stale)

- Compositor: Hyprland
- Bar: waybar — installed as **`aur/waybar-git`**, not `extra/waybar`.
  The fix for Hyprland's Lua dispatch (Waybar PR #5013) isn't in a
  tagged release yet: latest tag is still 0.15.0 (checked 2026-10-06).
  Recheck at each phase start; switch back to `extra/waybar` once a
  tagged release includes the fix. Background in `PHASES.md` Log
  (2026-09-21).
- Launcher: fuzzel — **planned, not installed** (2026-10-09). Live now:
  **hyprlauncher** 0.1.6 (Hyprland's first-party launcher, bound to
  Super+R in `hyprland.lua`); wofi 1.5.3 is also installed (maintenance
  status not checked). **fuzzel is being installed in round #7 for the
  network picker only** (user, 2026-10-09); Super+R stays on
  hyprlauncher until Phase 3 decides the launcher.
- Notifications: **mako 1.11.0 — installed and running, no config**
  (found 2026-10-09). **libnotify isn't installed**, so there's no
  `notify-send` and apps that use it (e.g. networkmanager-dmenu's
  connect/fail notices) stay silent. Unstyled, mako uses its upstream
  defaults (blue `#285577` background, white text, 2px `#4C7899`
  border) — off-palette; Phase 3 styles it.
- Idle/lock: hypridle + hyprlock — **planned, not installed**.
- Wallpaper: hyprpaper — not checked yet.
- Screenshot: grim + slurp + swappy (bound to Print) — grim is in use;
  slurp/swappy not checked.
- Terminal: foot — **planned, not installed**. Live now: **kitty**.
- Polkit agent: hyprpolkitagent 0.2.0 — **installed, not running**
  (polkit-gnome is installed too). Nothing needs one yet: NetworkManager
  lets the user scan and connect without it (§6). Start it once
  something does (Phase 3/4, when `hypr` is stowed).
- Network: **NetworkManager 1.58.1** (wpa_supplicant backend), `nmcli`
  and `nmtui` present; iwd not installed, systemd-networkd disabled.

**Open stack question (for whichever phase first needs it):** keep the
live tools (hyprlauncher, kitty) or switch to the planned ones (fuzzel,
foot)? The user decides; don't install a planned tool or remove a live
one without asking. The network picker (Phase 1.1) is the first thing
that touches this.

## 5. What's already built

- **waybar** (`waybar/.config/waybar/`, stowed live with `stow -t ~`,
  restow with `-R` when files are added): final Phase 1 pass deployed
  2026-10-09 — layout L2 (`SITE-9`, workspaces | clock, MET | CPU, RAM,
  VOL, NET, PWR, tray), 11px double-strike, corner ticks
  (`frame/tick-symbolic.svg`), one-color state readouts, S1 icons,
  DOS-fill bars, 36px. Seen live by the user. Fix pass done 2026-10-09:
  ticked workspace tabs, thresholds 29/14, fixed-width percentages.
  Remaining Phase 1 work (1.1 network picker, 1.2 volume slider) is in
  `PHASES.md`.
- **hypr** — not stowed from this repo yet. The only change so far is
  `scale = "1"`, made directly in the live `~/.config/hypr/hyprland.lua`
  (Phase 1 fix); otherwise it's Hyprland's stock example config. It
  includes the stock `XF86AudioMute` → `wpctl set-mute
  @DEFAULT_AUDIO_SINK@ toggle` bind (around line 308, `locked = true,
  repeating = true`), which is where mute lives now. When `hypr` is first stowed, back up
  the live file and carry both over.
  - **Stray autostart:** `hyprland.lua:55` starts `nm-applet`, which
    isn't installed (and is rejected — §6), so it fails silently at
    every login. Drop that line when `hypr` is stowed.
- Everything else starts from scratch.

## 6. Verified tooling facts

Behavior checked against the actual installed versions — not training
data. Recheck if the package version changes. Newest first.

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
- **networkmanager-dmenu has no option to hide its action rows**
  (Disable WiFi, Launch Connection Manager, …) or the blank separator
  rows between sections — not in the README's config table (UNIT-1 to
  confirm in the installed source). In fuzzel the blank rows are
  clickable. It also prints 4 `GLib-GObject-CRITICAL` lines per launch
  (works anyway), and "Launch Connection Manager" runs `xterm -e nmtui`
  unless `[editor] terminal` is set (xterm isn't installed). Being
  replaced by a SITE-9 script (§3).
- **fuzzel, observed 2026-10-09:** default width is 30 characters (rows
  get cut off). With the default `keyboard-focus=exclusive`, clicking
  another window **doesn't** close it; `keyboard-focus=on-demand` +
  `exit-on-keyboard-focus-loss` (default yes) is the documented way to
  close on focus loss — to be checked on this machine.
- **NetworkManager permissions** (`nmcli general permissions`):
  network-control, wifi.scan and settings.modify.own are `yes` for the
  user, so any picker can scan and connect **without a polkit agent**.
- `extra/networkmanager-dmenu` 2.6.3, not installed (upstream
  latest 2.7.2; **2.7.2-1 is in `extra-testing`**, built 2026-09-29, so
  it reaches `extra` through normal updates — no AUR build needed).
  `-git` on AUR is maintained by upstream. Read in the v2.6.3 source
  (recheck after the 2.7.x upgrade):
  - Strips `-d`, `-dmenu` and `--dmenu` from `dmenu_command`, then adds
    its own flags for launchers it knows.
  - Knows fuzzel: adds `--dmenu --placeholder <prompt>`, and with
    `[dmenu_passphrase] obscure = True` adds `--password` (masked
    passphrase).
  - Launchers it doesn't know (e.g. hyprlauncher) get no prompt text and
    no masking — only a `pinentry` program can hide the passphrase.
  - Config keys (upstream README): `wifi_chars` (4 characters, used by
    `{bars}` in `format`), `wifi_icons` (used by `{icon}`), `format`,
    `compact`, `pinentry`. Default icons are Nerd wifi glyphs
    (󰤯󰤟󰤢󰤥󰤨), present in DepartureMono Nerd Font.
  - Uses `notify-send` for connect/fail notices if libnotify is present;
    with no notification daemon running they don't show.
- `extra/network-manager-applet` 1.36.0 does SNI/tray via `--indicator`,
  but depends on Canonical's **libappindicator** (unmaintained upstream,
  not the maintained libayatana-appindicator) — treat as deprecated,
  don't use.
- `extra/fuzzel` 1.15.0 (upstream man page; not installed yet):
  `anchor=top-right` with `x-margin`/`y-margin` can place it under the
  bar — whether `y-margin` counts from the bar's edge or the screen's is
  **unchecked on this machine**. Defaults are off-spec: **Solarized
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
- **Text-shadow placement:** applying it on `window#waybar label`
  covers bar text and leaves tooltips alone.
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
- **GTK3 `text-shadow`** paints the shadow pass first, then the real
  text on top, and the shadow ignores pango span colors (see §3,
  Weight).
