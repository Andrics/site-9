# SITE-9 — Build Spec

> Personal workstation configuration. Arch Linux / Hyprland.
> This is the source of truth for constraints and design decisions.
> Read this before touching styling on anything.

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

Font: JetBrains Mono Nerd Font. Applied so far: waybar only — carry these
exact tokens into every later phase rather than re-deciding per app.

### What IS fixed regardless of which palette gets picked

**Shape language**
- Border radius: 0px, or at most 1–2px if 0 looks visually broken
  somewhere. No soft rounded corners anywhere.
- Borders: thin (1px), hard, high-contrast. No soft shadows, ever.
- No gradients.

**Typography**
- Monospace, everywhere, no exceptions — this is a stated requirement,
  not a default. Specific font is still an open question (Phase 1) — but
  whatever's picked, verify actual glyph rendering at bar-scale text size
  looks right on this specific screen before finalizing, don't just trust
  it on name recognition.

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
- Bar: waybar
- Launcher: fuzzel
- Notifications: mako
- Idle/lock: hypridle + hyprlock
- Wallpaper: hyprpaper
- Screenshot: grim + slurp + swappy (bound to Print)
- Terminal: foot
- Polkit agent: hyprpolkitagent

## 5. What's already built

- **waybar** — functional baseline exists (`waybar/.config/waybar/` in this
  repo): workspaces, clock, pulseaudio, network, battery, tray. Module
  *layout* is fine to keep. Styling is still the old generic dark-minimal
  placeholder and does **not** match the Half-Life/Black Mesa language yet
  — full restyle is Phase 1, currently in progress. See `PHASES.md`.
- Nothing else has been touched yet. Everything else starts from scratch.
