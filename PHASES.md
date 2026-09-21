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
| 6 | Sidebar | Not started |

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
- Font: Departure Mono Nerd Font (2026-09-21) — swapped from JetBrains
  Mono Nerd Font per Overseer direction. Installed from AUR
  (`otf-departure-mono-nerd`). Not yet confirmed on-screen.
- Bar shape: full-width, flush to the screen edge, no floating rounded
  pill — reads more like an institutional control panel.
- Module framing & state color (2026-09-21): bracketed-HUD boxes per
  module + HEV-style state coloring, SCP influence via `FIELD: value`
  labeling only. Full detail in `BUILD_SPEC.md` §3. Not yet implemented
  or seen live — see Still open.
- Applied to waybar (`waybar/.config/waybar/`) — needs to be seen live on
  the actual screen and confirmed before calling this phase done.
- Module framing & state-color pass (2026-09-21): built and deployed,
  per plan reviewed and approved by THE OVERSEER. See Log for detail.
- Volume dropdown/slider (2026-09-21): built and deployed. Right-click
  mute now works (moved off the leader's default on-click). Left-click
  reveal still doesn't fire — see Still open, this isn't resolved yet.

**Still open:**
- Volume slider reveal still doesn't fire on left-click (2026-09-21,
  live-tested by user). Right-click mute works now, so moving mute off
  the default `on-click` helped, but didn't fully fix it. Likely cause,
  per waybar's own `click-to-reveal` docs ("grouped modules may still
  process their own on-click events"): the leader module may swallow
  *all* button-press events once *any* `on-click-*` is bound to it,
  regardless of which button — not just the one it's bound to. Next
  test: remove `on-click-right` (mute) from the `pulseaudio` leader
  entirely and see if left-click reveal starts working; if it does,
  mute needs to live somewhere that isn't the leader's own on-click
  (the slider module itself, a keybind, etc.) rather than back on the
  group.
- On-screen confirm of the new framing/color AND the palette/font-at-
  bar-scale check (now Departure Mono, see above) — do both together,
  this is the real gate before Phase 1 closes. Not yet done.
- Bar height auto-bumped 30px → 32px (2026-09-21) when the volume
  slider was added — waybar expanded it to fit the 20px trough plus
  border/margin, not something explicitly requested. Cosmetic (2px),
  but flagging rather than absorbing silently; revisit if it reads as
  off once seen live.
- Module icons (VOL/NET/PWR) discovered blank (2026-09-21) — empty
  `format-icons`/missing glyphs since the initial baseline commit, not
  something recent edits caused. `BUILD_SPEC.md`'s "icons + short
  HUD-style text labels" decision isn't actually built yet. Iconography
  is an ask-first item per `AGENTS.md` — needs the user/Overseer to pick
  actual glyphs before this gets filled in.
- Workspace click-to-switch diagnosed dead (2026-09-21): upstream
  Waybar/Hyprland Lua-dispatch incompatibility, not a config bug. Fix
  exists (`aur/waybar-git`) but means swapping the installed `waybar`
  package from `extra` to an AUR git build — needs a go/no-go decision,
  not something to do unprompted. See Log for full detail.

**Resolved:**
- Fractional-scale conflict (scale was 1.5, `BUILD_SPEC.md` §2 requires
  integer only): user fixed directly, `scale = "auto"` → `scale = "1"`
  in `~/.config/hypr/hyprland.lua`, confirmed live via `hyprctl monitors`
  (`1920x1080@60Hz`, `scale: 1`).

## Phase 2 — System theme
Not scoped. Once Phase 1's palette is locked, ask what "system theme"
should actually cover before proposing anything — don't assume GTK/icon
theme scope carries over automatically.

**Reference found for the terminal (2026-09-21):**
[suchipi/half-life-vox-console](https://github.com/suchipi/half-life-vox-console)
— a real Black Mesa VOX announcer web console, source added to project
context (`index.css`, `App.js`, etc.), actual CSS reviewed, not just
screenshots. Key technique: two-tone beveled borders (light top/left +
dark bottom/right = raised, reversed = recessed), built from plain
`border-*-color` — no `box-shadow`, no gradient anywhere in the file, so
it's naturally compatible with §2's no-blur/no-shadow rule without
adaptation. Also present: monospace throughout, zero `border-radius`
anywhere, a single-hue olive-green tonal palette (mid-tone bg, no black —
different structure from SITE-9's near-black `--bg` + selective `--accent`),
and substring-match highlighting via a plain `mark` background, no
special effects.

Two open questions for when Phase 2 actually starts, not now:
- Bring the beveled-border technique in as a new element for the
  terminal specifically (distinguishing "terminal" from "HUD" within the
  same family), or keep it on the flat uniform-border look already built
  for waybar?
- The reference sits on a mid-tone olive background throughout, no
  black — keep the terminal on SITE-9's locked near-black `--bg`
  structure, or let it run a different, lighter tonal register since
  it's a distinct surface from the HUD bar?

Not scoped further than this — still gated behind Phase 1 closing first.

## Phase 3 — Shell polish
Not scoped.

## Phase 4 — Motion
Not scoped. `BUILD_SPEC.md` §2 performance constraints still govern
whatever gets decided here.

## Phase 5 — Login screen
Gated: confirm a display manager is actually installed/wanted before
scoping this at all — user may be starting Hyprland by hand from a TTY.

## Phase 6 — Sidebar
Not scoped. Ask what "sidebar" should actually cover — content, trigger,
placement, all of it — before proposing anything; don't assume it carries
over from waybar's decisions.

## Log

_(newest first, short entries)_

- 2026-09-21 — **Volume slider reveal: right-click mute confirmed fixed,
  left-click reveal still broken.** User tested live after the
  mute-to-right-click change below: right-click mutes correctly now,
  but left-clicking VOL shows no dropdown at all — the "fixed" framing
  in the entry below was premature. Re-diagnosed against waybar's own
  `click-to-reveal` man page note ("grouped modules may still process
  their own on-click events") — the leader having *any* `on-click-*`
  bound, not just the one matching the button actually pressed, may be
  enough to stop the group's reveal handler from ever seeing the click.
  Next test logged under Phase 1 "Still open": drop `on-click-right`
  from the leader entirely and see if reveal starts working; if so,
  mute needs to live somewhere other than the leader's own on-click.
- 2026-09-21 — **Volume slider click conflict: fixed.** User rebooted,
  tested the build, and reported clicking VOL just toggled mute — no
  slider appeared. Root cause: `pulseaudio`'s own `"on-click": "wpctl
  set-mute ..."` was still bound on the group leader, and it swallows
  the click before the group's `click-to-reveal` gets a chance — the
  waybar man page had actually warned about this ("grouped modules may
  still process their own on-click events") when this was researched
  for the original plan, and it should have been caught then instead of
  only surfacing after a live test. Fix: moved mute to `on-click-right`
  (documented, valid option for the pulseaudio module), leaving
  left-click free to trigger the reveal. Left-click now reveals the
  slider, right-click mutes. Restarted waybar, no errors. Still can't
  verify the reveal itself renders correctly (no synthetic-input tool
  here) — needs the user's own click to confirm.
- 2026-09-21 — **Volume dropdown/slider built and deployed.** Plan
  reviewed and approved by THE OVERSEER (confirmed a second time after
  the thread moved on before the first go-ahead got acted on). Verified
  syntax against the installed waybar's own man pages
  (`waybar-pulseaudio-slider.5`, group/drawer section of `waybar.5`)
  rather than assuming. `group/volume` wraps the existing `pulseaudio`
  module (leader, stays always visible) with `pulseaudio/slider`,
  revealed via `click-to-reveal`. `orientation: "horizontal"` set
  explicitly on the group — groups default to stacking vertically
  regardless of bar position, which would've broken the 30px bar.
  150ms reveal, drag handle hidden (`opacity: 0`), trough → `--border`,
  highlight → `--accent`, 0px radius throughout, matching the shared
  module-box framing. Restarted waybar, no errors, **but**: it logged
  `Requested height: 30 is less than the minimum height: 32 required by
  the modules` and auto-bumped the bar to 32px — see Phase 1 "Still
  open." Screenshot taken (see below) — shows the collapsed default
  state only; the slider reveal itself needs the user's own click to
  confirm, no synthetic-input tool available here to trigger it.
- 2026-09-21 — **Screenshot method corrected: cropped + upscaled, not
  full-desktop.** Overseer flagged the earlier full-screen `grim`
  capture as unusable for design review (bar reduced to a thin sliver).
  No `slurp` available in this context (needs interactive mouse drag,
  which isn't something this agent can drive) — used the bar's known
  fixed geometry instead (`grim -g "0,0 1920x32"`), then upscaled 3x
  with `ffmpeg`'s nearest-neighbor filter (`flags=neighbor`) to keep the
  pixel font crisp rather than blurring it, producing a large enough
  image to actually check font weight, module boxes, and the icon gap.
- 2026-09-21 — **Terminal reference found and logged: half-life-vox-console.**
  User found an existing Black Mesa VOX web console project and added its
  source to project context. Reviewed the actual `index.css`/`App.js`,
  not just the screenshot. Notable: it already respects §2's no-blur/
  no-shadow rule throughout (its 3D look comes entirely from two-tone
  border coloring, not shadows), so nothing to fight there. Logged under
  Phase 2 with two open questions (bevel technique scope, background
  tone) for whenever that phase actually starts. Phase 1 is still open —
  this is reference capture, not a green light to build Phase 2.
- 2026-09-21 — **Workspace click diagnosed: upstream Waybar/Hyprland
  incompatibility, not a config bug.** Overseer asked to verify
  `"on-click": "activate"` is present (it is) and, if still dead, check
  `waybar --version` against known regressions. Root cause: installed
  `waybar` (`extra`, 0.15.0-3) still sends Hyprland's old text-based
  dispatch commands (`dispatch workspace N`); Hyprland 0.54+ (this
  machine runs 0.56.2, Lua config) replaced that socket protocol with a
  Lua-based one, so old-style dispatches are silently invalid and clicks
  do nothing. Fixed upstream in Waybar PR #5013 (merged to `main`,
  routes through the new `hl.dsp` Lua API) but **no official Waybar
  release has shipped since**, so `extra/waybar` doesn't have the fix.
  `aur/waybar-git` (currently `0.15.0.r822.g4e76d73-1`) does, since it
  tracks git HEAD, but it **conflicts with and replaces** the `extra`
  `waybar` package. Not installed — this is a package-source swap
  (stable repo → AUR git build), which needs a decision, not something
  to do silently. Left as-is pending that call.
- 2026-09-21 — **Font swapped to Departure Mono Nerd Font; discovered
  the module icons have never actually rendered.** Built and installed
  `otf-departure-mono-nerd` (AUR, not `[extra]` as expected — verified
  with `pacman -Ss`/`yay -Ss`, package matches the version the Overseer
  named). Swapped `font-family` in `style.css`, restarted waybar, no
  errors. Screenshot showed VOL/NET/PWR with no icon glyph at all before
  the label — traced with `od -c` to the actual config bytes (not a
  rendering/font issue): pulseaudio/battery's `format-icons` arrays are
  literally `["", "", ""]` (empty strings) and network's format strings
  have a bare space where an icon glyph should be. Confirmed via
  `git show` on the initial commit that this has been true since the
  very first baseline — not something this session's edits caused.
  Leaving as-is: `BUILD_SPEC.md`/`AGENTS.md` both call out iconography
  as a personal-taste, ask-first decision, not something to fill in
  unprompted. `BUILD_SPEC.md` §3 updated with the new font. Screenshot
  taken for the Overseer; on-screen confirm still pending (see Phase 1
  "Still open").
- 2026-09-21 — **Module framing & state-color pass built and deployed.**
  Plan reviewed and approved by THE OVERSEER. Changes to
  `waybar/.config/waybar/{config.jsonc,style.css}`:
  - Every module now has a persistent `--border` box: workspace numbers
    are individually boxed tabs (was only on hover/active before), clock
    got a box too (no `TIME:` label — a clock doesn't need
    disambiguating the way VOL/NET/PWR do).
  - `FIELD: value` labeling added to pulseaudio/network/battery formats.
    The dimmed uppercase label is a pango `<span color='...'>` hardcoded
    directly in the format string, with a comment above each occurrence
    noting which `style.css` token the hex mirrors (`--text-dim` for the
    normal case, `--critical` for network's disconnected label) — GTK
    CSS can't reach inside a pango span, so this is the only way to
    color the label independent of the module's state-driven text
    color, and it needs a comment so the two don't silently drift apart.
  - Added the two state-color CSS rules the spec called for but that
    weren't actually written yet: `#network.disconnected` (critical) and
    `#pulseaudio.muted` (dim, distinct from warning/critical — a one-
    liner since the format-muted variant was already there).
  - Deployed live: `killall waybar` + relaunch, confirmed via its log
    it's reading the symlinked config/style with no errors.
  - Not yet on-screen confirmed by the user — see Phase 1 "Still open."
- 2026-09-21 — **Module framing & state-color direction decided.**
  Response to the on-screen check below: user picked a mix leaning
  bracketed-HUD + HEV combat-glow, SCP kept to label styling only.
  Locked in `BUILD_SPEC.md` §3. Not yet built — needs a UNIT-1 plan
  (CSS + threshold wiring) reviewed before execution, then on-screen
  confirm together with the original palette/font check.
- 2026-09-21 — **On-screen check: restyle doesn't read as Half-Life/SCP
  yet.** First live look at the deployed bar (scale 1x, correct symlink).
  Palette is visibly applied (green accent on active workspace) but the
  overall bar reads as an ordinary dark-mode status bar, not Black Mesa/
  SCP. Identified two gaps: (1) no visible module borders/dividers,
  which `BUILD_SPEC.md` §3 already requires regardless of palette — a
  spec gap, not an open style question; (2) accent color only used on
  one element, no state-based color logic on the HUD values. Phase 1
  stays "In progress." Style direction for the framing/color fix is
  being decided with the user before this goes back to UNIT-1 as a new
  scoped plan.
- 2026-09-21 — **Correction: `vfr` doesn't belong in waybar's config.**
  Two entries below describe adding `"vfr": true` to
  `waybar/.config/waybar/config.jsonc` as resolving the §2 vfr constraint —
  that's wrong. Waybar has no `vfr` config key (its top-level options are
  things like `layer`, `position`, `modules-*`, `margin`, `spacing`); the
  line is silently ignored and does nothing. `vfr` is a **Hyprland**
  setting, under `misc { vfr = true }` in `hyprland.lua`, where it already
  defaults to `true`. **Done 2026-09-21:** removed the line from waybar's
  `config.jsonc`. When Phase 4 populates `hyprland.lua`, set
  `misc { vfr = true }` there explicitly (documents the already-locked
  constraint — not a behavior change, since it's on by default).
- 2026-09-21 — **Phase 1 restyle actually deployed live** (it wasn't
  before — see below). Backed up the pre-existing
  `~/.config/waybar/{config.jsonc,style.css}` to `*.pre-stow.bak`, then
  `stow waybar`. First attempt used the default target and silently
  linked to `~/Development/.config` instead of `~/.config`, because this
  repo lives at `~/Development/site-9`, not `~/site-9` as the README's
  quickstart example assumes — parent-dir-as-target only works from the
  latter. Corrected with `stow -t ~ waybar`; symlinks now land correctly
  in `~/.config/waybar/`. **Note for next stow invocation (hypr package,
  etc.): use `stow -t ~ <package>` from this repo's actual location, not
  bare `stow <package>`.** Restarted waybar to load the new config —
  confirmed via its log it's reading from the symlinked path, no errors.
  Also confirmed user's own fix for the scale-1.5 blocker is live
  (`hyprctl monitors` shows `scale: 1`). Phase 1's restyle (palette,
  shape, `VOL`/`NET`/`PWR` labels, `vfr: true`) is now genuinely visible
  on-screen for the first time — before this, the repo had the new
  styling but the live bar was still running the old placeholder config
  since it was never stowed.
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
