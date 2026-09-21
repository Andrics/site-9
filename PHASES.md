# SITE-9 — Phases

One file. UNIT-1 and the Project agent (THE OVERSEER) both read and update
this directly — don't split status/tasks back out into separate files.

## How this actually works

Nothing below is a finished spec. Design decisions here are personal, not
generic best-practice — so the agent's job at each phase is to **ask what's
wanted**, then build it, not to build from an assumed answer. If a phase
below has blanks or open questions, that's intentional: they get filled in
through conversation, not pre-decided.

Beyond asking, non-trivial work also goes through a **plan → review → go**
loop before execution — see the Workflow section in `AGENTS.md`. UNIT-1
proposes a plan, the user relays it to the Project chat for review, and
work only starts once that review comes back with a go-ahead.

## Status

| # | Phase | Status |
|---|-------|--------|
| 0 | Waybar — functional baseline (modules/layout) | Done |
| 1 | Waybar — Half-Life / Black Mesa restyle | In progress |
| 2 | System theme (GTK/icons/cursor/terminal/file manager) | Not started |
| 3 | Shell polish (fuzzel/mako/hyprlock) | Not started |
| 4 | Motion (Hyprland animations/window rules) | Not started |
| 5 | Login screen (optional — gated on whether a display manager exists) | Not started |

## Phase 1 — Waybar restyle

Goal: match the **Half-Life / Black Mesa** direction (see `BUILD_SPEC.md`
§3) — replacing the old placeholder "generic dark minimal" styling, not
just building on top of it.

**Decided so far:**
- Color direction: fusion — HEV-style green as primary accent, Black Mesa
  institutional olive/tan as the structural base. Full palette locked in
  `BUILD_SPEC.md` §3.
- Corners/borders: fully sharp, 0px radius, hard 1px borders throughout.
- Module display: icons + short HUD-style text labels (e.g. `VOL 45%`,
  `NET 82%`, `PWR 100%`), not icon-only.
- Font: JetBrains Mono Nerd Font (already installed) — open to swapping
  for something grittier (Departure Mono) later if it doesn't read well
  at bar scale.
- Bar shape: full-width, flush to the screen edge, no floating rounded
  pill — reads more like an institutional control panel.
- Applied to waybar (`waybar/.config/waybar/`) — needs to be seen live on
  the actual screen and confirmed before calling this phase done.

**Still open:**
- **Blocker found 2026-09-21:** live monitor is running at scale 1.5
  (fractional) — conflicts with `BUILD_SPEC.md` §2's integer-scale-only
  rule. User decided: switch to scale 1 (native 1920x1080). Not yet
  applied — the live `~/.config/hypr/hyprland.lua` that sets this isn't
  part of this repo yet (hypr/ package hasn't started, per "one phase at
  a time"). One-line change needed there: `scale = "auto"` →
  `scale = 1` in the `hl.monitor({...})` block, then `hyprctl reload`.
  User needs to apply this (edit denied to UNIT-1 as an out-of-repo
  system-file change) before the items below can be checked at final
  scale.
- Confirm the palette actually looks right on-screen (colors read
  differently on the real display than in a spec doc) — do this *after*
  scale is fixed to 1x, not before.
- Font rendering check at bar-scale text size — same, after scale fix.

## Phase 2 — System theme
Not scoped. Once Phase 1's palette is locked, ask what "system theme"
should actually cover before proposing anything — don't assume GTK/icon
theme scope carries over automatically.

## Phase 3 — Shell polish
Not scoped.

## Phase 4 — Motion
Not scoped. `BUILD_SPEC.md` §2 performance constraints still govern
whatever gets decided here.

## Phase 5 — Login screen
Gated: confirm a display manager is actually installed/wanted before
scoping this at all — user may be starting Hyprland by hand from a TTY.

## Log

_(newest first, short entries)_

- 2026-09-21 — Repo pushed to GitHub: `github.com/Andrics/site-9` (public).
  SSH key generated and added to the GitHub account; repo scanned for
  secrets before going public (clean — only `.gitignore` rules and the
  word "token" in a design-tokens table). `origin` remote set, both
  commits pushed, `main` tracks `origin/main`.
- 2026-09-21 — Repo git-initialized (was a plain directory until now,
  despite AGENTS.md/README assuming commit-as-you-go) and initial commit
  made capturing existing state. `BUILD_SPEC.md` §1 hardware section
  filled in with verified values (i7-8650U, UHD 620, 15Gi RAM,
  1920x1080@60Hz, kernel 6.18.52-1-lts, Hyprland 0.56.2). Added missing
  `"vfr": true` to waybar config (restates already-locked constraint).
  Found live scale=1.5 conflict with the integer-scale rule — user chose
  scale 1x; not yet applied, see Phase 1 "Still open."
- 2026-09-20 — Phase 1 palette/shape/font decided (see Phase 1 section
  above) and applied to waybar. Not yet confirmed live on-screen.
- 2026-09-20 — Consolidated `PHASES.md` + `phases/*.md` into this single
  file. Corrected direction: theme is Half-Life / Black Mesa, not generic
  dark minimal — `BUILD_SPEC.md` §3 updated to match, palette left open
  for Phase 1 questions rather than pre-decided.
