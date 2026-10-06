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

## 3. Design language: Half-Life / Black Mesa

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

- **Family confirmed by the user 2026-10-06.** They want it a bit bolder
  (MS-DOS / terminal blocky feel); size and weight are still open — see
  `PHASES.md` Phase 1 plan review.
- **Exact family name:** `DepartureMono Nerd Font` (no space). Use that
  in CSS; the spaced name only works through fontconfig fuzzy matching.
- **Pixel grid:** 550 units per em, 50 units per pixel, so the font is
  drawn on an **11px grid**. It renders pixel-crisp only at multiples of
  11px (11, 22, …). Other sizes (e.g. the current 13px) give uneven
  strokes. Pick sizes on the grid unless a deliberate exception is
  decided and recorded here.
- **Weight:** only a Regular style is known to ship (UNIT-1 confirming
  with `fc-list`). Any bolder look has to be produced another way —
  options under test in `PHASES.md`.

### Locked module framing & state color (decided Phase 1 — 2026-09-21)

First on-screen pass read as a generic dark-mode bar with one green accent,
not Half-Life/SCP — traced to missing module separation and no
state-driven color use. Direction chosen: primarily bracketed-HUD framing
+ HEV-style state color, with SCP report influence kept to labeling only
(not structural — the module boxes already provide separation a hairline
treatment would have given).

- **Framing:** every module (workspace group, clock, VOL, NET, PWR) gets
  its own thin `--border` box, small gap between boxes so they read as
  discrete panel segments rather than one continuous strip. Workspace
  numbers become individually boxed tabs, not plain numbers with a
  highlight.
- **State color:** values default to `--text` (label in `--text-dim`,
  uppercase, e.g. `PWR:`), box border/value shifts to `--warning` or
  `--critical` when the module is in a flagged state, `--accent` marks
  the active workspace. Suggested starting thresholds (adjustable once
  seen live): PWR `--warning` <30%, `--critical` <15%; NET `--critical`
  on disconnect. Not yet confirmed on-screen.
- **Labels:** `FIELD: value` formatting inside each box — uppercase
  dimmed label, value in state color — carries the SCP report influence
  without adding separate hairline dividers.
- Outer bar getting a top/bottom hairline rule (echoing a report-page
  header) is a nice-to-have, not required.

Status: built and deployed 2026-09-21 (see `PHASES.md` Log). Still needs
the user's on-screen confirm. Note: the approved content-density
direction swaps full-rectangle boxes for **corner-tick framing** — that
change is being scoped in the combined plan (`PHASES.md` "Next up for
UNIT-1"), so the full-box treatment above is current-but-provisional.

### Icon direction (decided Phase 1 — 2026-10-06)

HUD/gauge-style glyphs for the VOL/NET/PWR modules: boxy, segmented or
bracket-like forms that lean into the HEV HUD — **not** the default
rounded, Font-Awesome-style icon-font look. Chosen over minimal outline
glyphs and over going icon-less.

- Icons and the segmented value bars (content-density pass) are **one
  visual system**: same blocky, geometric register. Don't pick them
  independently.
- What the font actually has (checked 2026-10-06 with `fc-query` and
  `pango-view` renders): all Box Drawing (128/128) and Block Elements
  (32/32) characters, all Nerd Font MD and FA icons, progress-bar glyphs
  U+EE00–EE0B. **Not** in the font: `▮ ▯ ▰ ▱ ■ □` — don't use them,
  they'd only render via a fallback font. Block and box characters
  render pixel-sharp at 11px; Nerd Font icons render soft-edged and
  slightly small next to the pixel text.
- Watch emoji-default codepoints (e.g. `⚡` U+26A1): Pango can draw them
  from a color emoji font. Pin them with U+FE0E or avoid them.
- Exact glyphs are not chosen yet. Candidates must be confirmed present
  in the installed Departure Mono Nerd Font build (check the font
  itself, not a generic Nerd Fonts cheat-sheet — coverage varies by
  patch set) and proposed as options, not picked.
- If a good glyph only exists via a fallback font, that's a design
  question to raise, not something to quietly wire in.

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
  it on name recognition. Family confirmed 2026-10-06; size and weight
  pending. Sizes on the 11px grid (see above).

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
- Launcher: fuzzel
- Notifications: mako
- Idle/lock: hypridle + hyprlock
- Wallpaper: hyprpaper
- Screenshot: grim + slurp + swappy (bound to Print)
- Terminal: foot
- Polkit agent: hyprpolkitagent

## 5. What's already built

- **waybar** (`waybar/.config/waybar/`, stowed live with `stow -t ~`):
  workspaces, clock, pulseaudio (+ click-to-reveal volume slider),
  network, battery, tray. Phase 1 restyle is deployed — locked palette,
  Departure Mono, per-module boxes, `FIELD: value` labels, state colors.
  Not yet confirmed on-screen by the user, module icons still blank, and
  the content-density rework is still to come. Phase 1 stays open. See
  `PHASES.md`.
- **hypr** — not stowed from this repo yet. The only change so far is
  `scale = "1"`, made directly in the live `~/.config/hypr/hyprland.lua`
  (Phase 1 fix). The live file also has the stock `XF86AudioMute` →
  `wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle` bind (around line 308),
  which is where mute lives now. When `hypr` is first stowed, back up
  the live file and carry both over.
- Everything else starts from scratch.
