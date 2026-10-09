# SITE-9 — Phases

One file — don't split status/tasks back out into separate files.

**Maintained by THE OVERSEER** (since 2026-10-06). UNIT-1 reads this but
doesn't edit it: it reports work in a "Report for THE OVERSEER" block
(see `AGENTS.md`), the user relays that to the Project chat, and THE
OVERSEER folds it in here and hands back an updated file for the user to
drop into the repo. Log entries before 2026-10-06 were written by both
agents directly.

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

**Two sub-phases per round (from 2026-10-09).** Phases are split into
numbered sub-phases (`1.1`, `1.2`, `2.1`, …), and every round — plan,
build, test or fix — covers the next two together. Checks a plan needs
go inside the plan, not in a round of their own. Full rule in
`AGENTS.md` → Batching.

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

## Next up for UNIT-1

_Written by THE OVERSEER; replaced whenever there's a new task._

**Round (2026-10-09, #7): sub-phases 1.1 + 1.2 — one plan. Plus a
trivial fix and a push.**

**Do now (no plan needed):**
- **Tab hover line:** add `box-shadow: none` to the workspace button
  hover rule (Adwaita's hover shadow — a §2 violation, see `BUILD_SPEC.md`
  §2 "GTK theme defaults count"). One commit.
- **Push:** nothing has been pushed since 2026-09-21. Push everything to
  `origin/main` once `git status` is clean, and report the hash.

**Then write ONE plan covering both sub-phases** (Phase 1 → "Still
open" has the background). Present design choices as options; the user
picks when THE OVERSEER reviews the plan. Fold any checks into the plan.

- **1.1 Network picker** — click NET → a list of available networks;
  pick one to connect, prompt for the passphrase if needed. Plan these
  options concretely (packages, config, keybinds/on-click, how the menu
  is positioned and styled for now):
  - N1a: `extra/networkmanager-dmenu` through **fuzzel** (needs fuzzel
    installed — it's the planned launcher, but not on the machine).
  - N1b: `networkmanager-dmenu` through **hyprlauncher `--dmenu`**
    (already installed). Check on the machine: does `--dmenu` work, can
    it mask a passphrase (or does it need pinentry), can it be placed
    top-right under the bar.
  - N3: click NET opens `nmtui` in a floating **kitty** window (no new
    packages).
  - N2 (`nm-applet`) is out — deprecated dependency (`BUILD_SPEC.md` §6).
  NET has no drawer, so `on-click` on the network module is safe.
- **1.2 Volume slider** — currently vertical by config (`orientation:
  vertical`, 14×24px trough), Adwaita border + blue outline, fill
  ~2px at 12%. Plan both options:
  - V1: fix it — horizontal, a long thin trough in the palette, fill in
    the module's color, no knob, Adwaita border/outline overridden.
    Give the size and what it does to bar height (could the bar drop
    back toward 30px?).
  - V2: drop the slider — volume by scrolling on VOL (pulseaudio's
    native scroll), click stays free for something else or nothing.
    Say what happens to `group/volume`, and the bar height.

Screenshots for anything you render go in `~/Pictures/site-9-phase1/`
(`AGENTS.md`). End with the report block, including the pushed hash.

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
  (`otf-departure-mono-nerd` 3.4.0-1). **Family confirmed by the user
  2026-10-06** ("I like this font"), with one ask: a bit bolder, for an
  MS-DOS / terminal blocky feel. Size and weight still open (choices F
  and W in the plan review). Exact family name and the 11px pixel grid
  are recorded in `BUILD_SPEC.md` §3.
- Bar shape: full-width, flush to the screen edge, no floating rounded
  pill — reads more like an institutional control panel.
- Module framing & state color (2026-09-21): bracketed-HUD boxes per
  module + HEV-style state coloring, SCP influence via `FIELD: value`
  labeling only. Full detail in `BUILD_SPEC.md` §3. Built and deployed
  the same day (see below); corner-tick framing may replace the full
  boxes (plan review).
- Applied to waybar (`waybar/.config/waybar/`) — needs to be seen live on
  the actual screen and confirmed before calling this phase done.
- Module framing & state-color pass (2026-09-21): built and deployed,
  per plan reviewed and approved by THE OVERSEER. See Log for detail.
- Volume dropdown/slider (2026-09-21): built and deployed. Reveal
  confirmed working (see Log) — user screenshotted it live. Mute is no
  longer on the bar; it's the `XF86AudioMute` key (see Mute location).
  Slider gauge enlarged (14px/24px) per user feedback that it was too
  small to see.
- Workspace click-to-switch (2026-09-21): package swapped
  `extra/waybar` → `aur/waybar-git` (0.15.0.r1019.g3672eee-1, includes
  the Lua-dispatch fix) per Overseer go-ahead. Installed, waybar
  restarted on the new binary, no errors. **Confirmed working by the
  user 2026-10-06** — clicking a tab switches workspaces.
- Mute location (2026-09-21, decided by THE OVERSEER): moves to a
  Hyprland keybind (`XF86AudioMute` → `wpctl set-mute @DEFAULT_AUDIO_SINK@
  toggle` or equivalent), not back onto waybar. Reasoning: real mute is
  a separate boolean from volume level — drag-to-zero loses "restore to
  previous volume" on unmute, and `pulseaudio/slider`'s documented
  config (`min`/`max`/`orientation`/`expand`) shows no `on-click`
  option, so binding it there isn't confirmed possible. A dedicated key
  is also the more standard pattern (status widget for glanceable
  state + fine adjustment, discrete toggle lives at the compositor
  level) and sidesteps the group/leader click-conflict entirely.
  **Already in place:** the live `~/.config/hypr/hyprland.lua` has the
  stock bind (around line 308) `XF86AudioMute` → `wpctl set-mute
  @DEFAULT_AUDIO_SINK@ toggle`, `locked = true, repeating = true`.
  Nothing to add. (UNIT-1 recorded this in
  commit f78a3e7; the 2026-10-06 doc sync dropped it, restored here.)
  Carry the bind over when `hypr` is first stowed. The stale
  "diagnostic test / restore mute" comment in `config.jsonc` gets
  removed in the combined build.
- Content-density direction approved (2026-09-21) — user reacted
  positively to all of the Overseer's brainstormed additions from the
  "too simple" feedback round: more modules (CPU/RAM/uptime formatted
  as a mission clock, a static `SITE-9` tag), segmented value bars
  (block-character gauges next to the percentage — note the `▮▯` used
  as the example then aren't in Departure Mono, see plan review),
  corner-tick framing instead of full-rectangle module boxes, and
  boxing the tray icons for consistency. Approved in direction. Now
  being scoped together with the icon glyphs — see Combined pass below.
- Icon direction (2026-10-06, user's pick): HUD/gauge-style glyphs for
  VOL/NET/PWR — boxy, segmented/bracket forms, not the default rounded
  icon-font look. Chosen over minimal outline glyphs and icon-less.
  Full detail in `BUILD_SPEC.md` §3. Exact glyphs not chosen yet.
- Combined pass (2026-10-06, THE OVERSEER): icon glyphs, the
  content-density rework, and the bar-height drift get scoped as **one**
  UNIT-1 plan instead of separate passes. Same modules, same blocky
  glyph vocabulary — planning them apart risks two visual systems on one
  bar. This replaces the earlier "wait until the open items clear"
  sequencing; only glyph *locking* waits on the font confirm. Brief is
  in "Next up for UNIT-1" above.
- Keep `waybar-git` (2026-10-06 check): latest tagged Waybar release is
  still 0.15.0, without the PR #5013 Lua-dispatch fix. Recheck at each
  phase start; return to `extra/waybar` once a tagged release has it.
  Recorded in `BUILD_SPEC.md` §4.
- **Combined plan review (2026-10-06, THE OVERSEER).** Verdict: the
  plan is **approved in structure** — nothing in it breaks §2 or the
  design language, the build method (prebuilt bar strings in
  `format-icons`, no polling scripts, `interval: "once"` for the static
  tag) is the right one, and skipping waybar-git's undocumented new
  option is correct. **Build is not a go yet:** it waits on the user's
  choices below and on the tests in "Next up for UNIT-1". Review notes
  that bind the build:
  - Nerd Font icons render soft-edged and smaller next to the pixel text
    (UNIT-1's renders). That works against the blocky direction, so
    S2/S3 start at a disadvantage.
  - `⚡` (S1 charging) has emoji-by-default presentation — must be
    pinned to the text glyph or replaced (test #4).
  - Empty-segment color is a hardcoded hex inside a pango span, same as
    the dimmed labels: each one needs the same comment naming the
    `style.css` token it mirrors.
  - CSS `font-family` changes to the exact family name
    `DepartureMono Nerd Font` (it currently relies on fontconfig
    fuzzy-matching the spaced name).
  - Bar strings use N entries (entry i lights i+1 segments), so 0% still
    shows one lit segment. Accepted: mute, disconnect, and low battery
    already have their own states.

  Options as UNIT-1 planned them (glyphs verified present in the font):
  - **S1 all-native:** VOL `◄` U+25C4 static; NET `▂▄▆█`
    U+2582/84/86/88 lit by signal strength (no separate NET bar); PWR
    `⏻` U+23FB, plus `⚡` U+26A1 while charging; bars `▌` U+258C ×10,
    lit in the module's state color, empty in `--border`.
  - **S2 Nerd MD, level-stepped:** speaker with 3 levels + muted
    (U+F057F/F0580/F057E, F0581); stepped signal (U+F08BC–F08BF),
    disconnected U+F0318; upright battery in 10% steps (U+F007A–F0082,
    F0079), charging U+F0084; bars `┃`/`│` ×10.
  - **S3 mixed:** VOL `◄`; NET as S2; PWR sideways battery outline, 5
    steps (U+F244–F240); bars `█`/`░` ×5 (reads as a solid fill, and
    `░` in `--border` nearly disappears).
  - Layout **L2:** left `SITE-9` · workspaces | center clock · MET |
    right CPU RAM VOL NET PWR tray. (L1/L3 move SITE-9/MET elsewhere —
    see UNIT-1's plan.)
  - MET (mission clock): `custom/met`, interval 60, `awk` on
    `/proc/uptime`, format `T+DDD:HH:MM`. CPU interval 10, RAM 30.
  - Framing: corner ticks via `border-image` 9-slice SVG with
    `border-image-width` separate from the 1px border, recolored per
    state with `-gtk-recolor`. Unproven — probe first. Fallbacks: (a)
    keep full boxes, (b) left/right borders only.
  - Tray: **T1** one box around the whole tray, `icon-size: 14`;
    **T2** a box per icon, `--warning` border on needs-attention. Tray
    icons are app-colored either way.
  - Height: **H1** back to ~30px by shrinking the slider; **H2** keep
    36px and the bigger slider the user asked for. 11px text rows come
    to ~28px; corner ticks add 0px.

  First renders reviewed 2026-10-06 (UNIT-1's `site9-mock-11px.png`,
  `site9-mock-13px.png`, `site9-glyphsheet-11px.png`, via the user):
  - S1 reads best: the `▌` segments and `▂▄▆█` NET steps are crisp, and
    the state colors work (PWR at 8% goes fully `--critical`, bar
    included).
  - S2's Nerd icons and thin `┃`/`│` bars look small and light — they
    undercut the blocky direction.
  - S3's `█`/`░` reads as a fill, not segments. That fails the
    segmented-bar idea but is the classic DOS installer look, which
    suits the user's new MS-DOS ask. Kept as a bar-style candidate
    alongside `▌` segments, with `░` in `--text-dim` so it stays
    visible (probe item 5).
  - `⚡` currently renders as the plain text glyph (no color emoji font
    in the way). The pin to U+FE0E still applies, in case one gets
    installed later.
  - The glyph sheet's alternate clock format `T+03:14:07` shows seconds;
    with a 60s interval that would sit stale for up to a minute. Keep
    seconds out unless the interval changes.
  - At the screenshot sizes, 13px reads heavier mainly because it's
    bigger. The uneven strokes UNIT-1 measured need the upscaled crops
    to judge.

  Test round reviewed 2026-10-06 (probe bar + pango renders,
  screenshots via the user). Findings that change the options:
  - Corner ticks work, crisp and recolorable, +0px height. Technique in
    `BUILD_SPEC.md` §3. Fallbacks (a)/(b) no longer needed unless the
    user prefers full boxes after seeing both side by side.
  - Weight: W1 smears (out). W3 is just bigger (out). W2 is crisp bold
    but its doubled copy ignores span colors, so dim labels and dim bar
    parts get a bright column. W2 variants: (a) accept that — not
    recommended, it reads as a glitch; (b) W2 only on elements with no
    dim spans (`SITE-9`, clock, MET, workspace tabs), data modules stay
    light; (c) drop dim labels, everything one color per module —
    changes the locked `FIELD: value` rule in `BUILD_SPEC.md` §3;
    (d) give each label its own static module so it can be dim *and*
    double-struck — keeps the locked rule, more config, feasibility
    desk-checked in "Next up".
  - `▌` segments are soft at 11px (3.5px wide); only `█` is crisp. That
    rules out S1's segment bars and favors the DOS fill. This replaces
    the approved "segmented value bars" idea with a fill bar — needs the
    user's OK. Empty part: `░` dither (soft texture, authentic DOS, gets
    brighter and busier under W2) or `█` in a dark tone (crisp trough).
  - `⚡` is small and thin next to the text. Charging options: keep
    `⚡︎`; Nerd bolt U+F0E7 (soft like the other Nerd icons); or text —
    the `PWR:` label swaps to `CHG:` while charging (battery's
    `format-charging`).
  - Probe height: 24px with ticks and 11px text but no slider. The live
    36px comes from the slider alone, so H1 could land well under 30px.

  W2-d desk check (2026-10-06, against waybar-git source at 3672eee0):
  - Label module + value module in a group, ticks on the group: works.
    **But the frame can no longer follow state** — `.warning` /
    `.critical` / `.disconnected` sit on the value module, and GTK3 CSS
    has no parent selector, so neither the group's frame nor the label
    can react. Lost: PWR frame going amber/red, NET label going red on
    disconnect. Value text and bar still recolor. Untested workaround:
    split ticks — label module draws the left ticks, value module the
    right ticks (recolored by state), so half the frame follows state.
  - Volume drawer: the label can't just be added to `group/volume` (it
    would become the leader, or be hidden in the drawer). Arrangement
    A: drawer = [`group/vol-head`, `pulseaudio/slider`], with vol-head
    = [`custom/vol-label`, `pulseaudio`] — click anywhere on label or
    value toggles the slider, same as today. Arrangement B: plain outer
    group = [label, `group/volume`] — label clicks do nothing. Neither
    has been run.
  - Icon order: with labels as separate modules, level-changing icons
    (NET steps) must sit after the label (`NET: ▂▄▆█ 82%`); static
    icons (`◄`, `⏻`) either go in the dim label module or move after
    the label too.
  - Cost: VOL/NET/PWR/CPU/RAM each gain a label module plus a group —
    all `"interval": "once"`, no exec, no runtime cost, but noticeably
    more config.
  - `█` trough under W2: confirmed by reasoning from the render order
    (shadow pass first, real text on top; the test-round pixels back it
    up). Exactly one bright 1px column at the bar's right end, full
    height, in the module's state color. The lit/trough boundary stays
    clean.

  THE OVERSEER's reading: W2-d keeps the dim labels but costs the
  state-colored frame — which is also a locked §3 rule — unless the
  untested split-tick workaround holds, and it roughly doubles the
  module count. Three clean paths:
  - **W0** — light weight, everything as locked, no exception, no new
    structure.
  - **W2-c** — bold everywhere; labels lose their separate dim color
    and take the module's color, so the *whole* readout (label, value,
    bar, frame) turns amber/red in a flagged state, HEV-style. One
    locked rule changes (dim labels); config stays simple; no drawer
    changes.
  - **W2-d + split ticks** — keeps dim labels and (half-)state-colored
    frames; needs drawer arrangement A and one more probe to prove the
    split ticks before building.

  **Choices made (user, 2026-10-06):** "W2-c, yes to exception, rest
  your leans." So: 11px; W2-c double-strike weight with labels in the
  module color; §2 exception granted (wording in `BUILD_SPEC.md` §2);
  DOS-fill `█` bars with a `█` `--border` trough, 10 cells; S1 icons
  (`◄` / `▂▄▆█` / `⏻`) without `▌` bars; `CHG:` label while charging;
  corner-tick framing; layout L2; MET `T+DDD:HH:MM`; tray T1; height H2
  (36px); no NET bar. All recorded as locked in `BUILD_SPEC.md` §2–§3.
  This replaces the earlier "segmented value bars" idea with a fill bar
  and the dim-label rule with one-color readouts.

**Still open — remaining sub-phases (earlier Phase 1 work predates
sub-phase numbering):**
- **1.1 Network picker** (user request 2026-10-09): click NET → a list
  of available networks to connect to — the user doesn't manage wifi
  from the terminal. Machine: NetworkManager 1.58.1, wlp2s0. Options
  (UNIT-1 plans them, user picks at review):
  - N1a `networkmanager-dmenu` via fuzzel — needs fuzzel installed
    (the planned launcher). THE OVERSEER's lean *if* the user is going
    with fuzzel as the launcher anyway.
  - N1b `networkmanager-dmenu` via hyprlauncher `--dmenu` — already
    installed; viability (passphrase masking, positioning) being
    checked in the plan. Lean *if* the user keeps hyprlauncher.
  - N3 `nmtui` in a floating kitty window — no new packages, but a
    terminal screen, not a list menu.
  - N2 `nm-applet` — **rejected**: depends on unmaintained Canonical
    libappindicator (no-deprecated rule).
  This forces the open launcher question (`BUILD_SPEC.md` §4): fuzzel
  vs hyprlauncher. Whichever menu is picked gets its real styling in
  Phase 3 and looks plain until then.
- **1.2 Volume slider** (known since 2026-09-21): diagnosed 2026-10-09 —
  vertical by config (`"orientation": "vertical"`, renders bottom-up),
  14×24px trough (16×26 rendered), Adwaita's light border and blue
  outline on it, fill only ~2px tall at 12%. Options: V1 fix it as a
  long thin horizontal gauge in the palette (THE OVERSEER's lean — the
  user asked for a slider); V2 drop it and scroll on VOL to change
  volume. Either way, check whether the bar can come back down toward
  30px.
- Phase 1 closes when 1.1 and 1.2 are built and the user confirms the
  whole bar on-screen.

**Resolved:**
- Fix pass (2026-10-09): 26db176 ticked workspace tabs (active =
  `--accent`), 3ad0eb1 battery thresholds 29/14, 49b5ab6 fixed-width
  percentages via fmt `{x:>3}`. Log clean, 1920×36. Approved on
  UNIT-1's report.
- Tab hover line (1px light line on hover): Adwaita's button-hover
  box-shadow, present since before the tabs changed. Counts as a drop
  shadow under §2 — removed in round #7 (`box-shadow: none`).
- Light 1px column after each DOS bar and after NET's steps: the
  double-strike overhang already accepted in `BUILD_SPEC.md` §3. Left
  as-is.
- Final Phase 1 build (2026-10-09): six steps committed (0f6fdc7,
  3276af9, eee67bf, bfecf46, c53a162) and deployed, reviewed and
  approved by THE OVERSEER. User saw it live; asked for tick framing on
  workspace tabs too.
- Module icons: no longer blank — S1 icons live.
- `█` fringe (≤10%, from the font): left as-is, see `BUILD_SPEC.md` §3.
- Undefined-by-spec defaults UNIT-1 picked, accepted: CPU/RAM have no
  icon; ethernet shows `NET: LINK` (no steps); muted shows
  `◄ VOL: MUTE` with no bar.
- All Phase 1 design choices (2026-10-06): font size/weight, §2
  double-strike exception, framing, bars, icons, charging, layout, MET,
  tray, height — see "Choices made" in the plan review.
- Bar height drift (30 → 36px): kept at 36px on purpose (H2), now set
  explicitly instead of auto-bumped.
- Workspace click-to-switch: works on `waybar-git`, confirmed by the
  user 2026-10-06.
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

- 2026-10-09 — **Fix pass reviewed: approved. New working rules: two
  sub-phases per round, push every round, screenshots in ~/Pictures.
  Handoff to a new Overseer chat.** UNIT-1 synced docs (61415e7) and
  shipped the fix pass (26db176, 3ad0eb1, 49b5ab6) — approved. Checks:
  NetworkManager 1.58.1 runs the network; `nm-applet` would pull in
  unmaintained libappindicator, so N2 is out; the slider is vertical by
  config, 14×24px, with Adwaita's border/outline. Found: `BUILD_SPEC.md`
  §4 didn't match the machine — fuzzel, foot, hypridle, hyprlock aren't
  installed; kitty and hyprlauncher are live (§4 corrected, launcher /
  terminal now an open stack question). Tab hover line traced to
  Adwaita's hover box-shadow — §2 now says GTK theme defaults count as
  shadows; fix rides along in the next round. User set new rules: (1)
  every round covers **two sub-phases** — plans, builds, tests and
  fixes alike — to cut round trips (`AGENTS.md` → Batching); remaining
  Phase 1 work renumbered as 1.1 network picker + 1.2 volume slider;
  (2) **push to GitHub every round** — nothing had been pushed since
  2026-09-21; (3) screenshots go in `~/Pictures/site-9-phase<N>/`, not
  `/tmp` (UNIT-1 had announced that folder but still used the
  scratchpad). This chat was handed off to a fresh Overseer chat; the
  docs are the full handoff.
- 2026-10-09 — **Final Phase 1 build reviewed: approved; fix pass
  briefed; network picker added.** UNIT-1 synced docs (9d84e94 —
  included `AGENTS.md`, correctly, since it was part of the same drop)
  and built all six steps, one commit each (0f6fdc7 font & weight,
  3276af9 corner ticks, eee67bf new modules + L2, bfecf46 icons & bars
  + `CHG:`, c53a162 tray/height/comment), restowed, restarted: log
  clean, 1920×36. Warning/critical/offline captured from a scratch copy
  — whole readout recolors as specced. Verdict: matches the spec;
  approved. Deviations found and settled: battery thresholds were
  25/10 in config vs 30/15 in spec (THE OVERSEER's brief said "keep
  existing" — ambiguous; spec wins, fix queued); `█` has a faint
  font-level fringe (left as-is, §3 corrected); percentage width jitter
  (fix queued). User saw it live: tabs should get corner ticks too;
  volume slider still opens as a small vertical bar (known, later); and
  asked for a network picker (click NET → list of networks). New §6
  facts recorded. Next: fix pass + backend and slider checks.
- 2026-10-06 — **All Phase 1 choices made; final build approved.** User:
  "W2-c, yes to exception, rest your leans." Locked in `BUILD_SPEC.md`:
  §2 gains a narrow exception for `text-shadow: 1px 0 0 currentColor`
  as double-strike weight only; §3 now records 11px + double-strike,
  corner-tick framing, one-color readouts (dim-label rule retired),
  S1 icons, DOS-fill bars with a `--border` trough, `CHG:` while
  charging, layout L2, MET format, tray, and 36px height. Build brief
  (6 steps, one commit each, restow for the new `frame/` dir) written
  into "Next up for UNIT-1". Open for the screenshot review: workspace
  tab framing.
- 2026-10-06 — **W2-d desk check reviewed; weight narrowed to three
  paths.** UNIT-1 synced docs (a235011; removed lines checked, nothing
  of its own dropped) and desk-checked W2-d against the waybar-git
  source — no probe, no machine changes. W2-d works structurally but
  loses state-colored frames (no parent selector in GTK3 CSS), needs a
  nested drawer arrangement, and adds a label module + group per
  readout. `█` trough under W2 confirmed: one 1px bright end column.
  Review and the three weight paths (W0 / W2-c / W2-d + split ticks)
  are in Phase 1's plan review; lean W2-c. Verified waybar behavior
  (group orientation default, drawer packing, click handling,
  `always-visible-class`) recorded in `BUILD_SPEC.md` §6. Next: user's
  choices. Project instructions also rewritten for the
  docs-ownership + relay + /clear workflow (text given to the user to
  paste into the Project).
- 2026-10-06 — **Test round reviewed: corner ticks proven, weight
  options narrowed, DOS fill favored; f78a3e7 recovered.** UNIT-1 synced
  docs (ba56d94; checked removed lines, nothing of its own dropped) and
  ran the round: weight W0–W3, corner-tick probe (second waybar from the
  scratchpad, bottom of screen, 90s auto-kill — exited cleanly, live bar
  untouched), DOS fill, `⚡` check. Results and the updated choice list
  are in Phase 1's plan review; the measured facts (crispness, W2's span
  color limit, tick technique, installed weights) are in `BUILD_SPEC.md`
  §3. Row E on the earlier glyph sheet was a test-script bug: the
  progress-bar glyphs U+EE00–EE0B are in the font and render as one
  outlined continuous bar, not segments. `git show f78a3e7`: everything
  survived except one Log entry (restored below, under 2026-09-21) and
  the bind's `locked = true, repeating = true` (now in `BUILD_SPEC.md`
  §5 and the Mute location bullet). Next: user's choices, plus a W2-d
  desk check by UNIT-1.
- 2026-10-06 — **Combined plan reviewed; workspace click confirmed; font
  family confirmed with a bolder ask; doc-sync slip found and fixed.**
  UNIT-1 synced the docs (commit 0608fc0) and delivered the combined
  plan without building. Review: approved in structure, build waits on
  user choices plus a test round (weight, corner-tick probe, `⚡`
  presentation) — full review under Phase 1 "Decided so far". UNIT-1
  found the sync had dropped commit f78a3e7: PHASES.md said the mute
  keybind wasn't built, but the stock `XF86AudioMute` bind is already
  live in `hyprland.lua`. Cause: THE OVERSEER edited from the Project's
  copy of PHASES.md, which predated f78a3e7. Mute fact restored; UNIT-1
  asked to report the rest of that commit; `AGENTS.md` sync rule now
  says to check removed lines too. UNIT-1 also found: `▮ ▯ ▰ ▱ ■ □`
  aren't in Departure Mono; the font is on an 11px pixel grid (13px is
  off-grid); exact family name is `DepartureMono Nerd Font` — all
  recorded in `BUILD_SPEC.md` §3. User confirmed workspace clicks work
  and that they like Departure Mono, but want it a tad bolder for an
  MS-DOS / terminal feel. THE OVERSEER checked: only one weight is
  known to ship, so the weight test covers synthetic bold, a
  double-strike via zero-blur `text-shadow` (flagged as needing an
  explicit §2 exception), and 22px as reference.

- 2026-10-06 — **New Overseer chat: icon direction decided, combined
  plan briefed, doc ownership moved to THE OVERSEER.** Picked up from
  the 2026-09-21 handoff. User chose HUD/gauge-style icon glyphs (over
  minimal outline or icon-less); recorded in `BUILD_SPEC.md` §3 as one
  visual system with the segmented value bars. THE OVERSEER folded the
  icon work, the content-density rework, and the bar-height drift into
  a single UNIT-1 plan — brief written into the new "Next up for
  UNIT-1" section. Workflow change: THE OVERSEER now maintains
  `BUILD_SPEC.md`, `PHASES.md`, and `AGENTS.md`; the user downloads and
  drops them into the repo; UNIT-1 stops editing docs and reports via a
  "Report for THE OVERSEER" block instead (rules in `AGENTS.md`). Also
  added the cropped/upscaled screenshot method to `AGENTS.md` as a
  standing rule. Checked Waybar releases: latest tag still 0.15.0, so
  `waybar-git` stays (now noted in `BUILD_SPEC.md` §4). Fixed stale
  `BUILD_SPEC.md` §5, which still described waybar as the unstyled
  placeholder and didn't note `hypr` is unstowed. No machine changes
  this session. Still pending from the user: workspace-click test and
  the font/framing on-screen confirm.

- 2026-09-21 — **Mute keybind: already satisfied, no build needed.**
  _(Restored 2026-10-06 from commit f78a3e7 after a doc sync dropped
  it. The relayed copy was partly cut off; gaps marked […].)_ Overseer
  relayed the mute-to-keybind decision as small enough to build without
  a separate plan. Checked the live `~/.config/hypr/hyprland.lua` first
  rather than assuming a blank slate — it's still Hyprland's unmodified
  stock example config, and the exact binding asked for
  (`XF86AudioMute` → `wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle`) is
  already in there from the template. Nothing to change. Left `hypr/`
  in this repo untouched […] Phase 4 work, not in scope while Phase 1
  is still open. Also relayed: workspace-click live test is on the user
  now that waybar-git is ins[talled …]; content-density plan stays
  deferred until the Phase 1 "Still open" items clear […].
- 2026-09-21 — **Session handoff: continuing in a new Overseer chat.**
  Wrap-up of this session: mute-location decided (Hyprland keybind, see
  Phase 1 "Decided so far"), content-density direction approved (same
  section), bar-height drift deferred into that future pass rather than
  tuned in isolation. Still open going in: workspace-click live test
  (package is swapped, unverified), the framing/font on-screen confirm,
  module icons, and the content-density plan itself once UNIT-1 scopes
  it. This file is the handoff — a fresh Overseer chat reads this plus
  `BUILD_SPEC.md`/`AGENTS.md` same as session one did, nothing here
  depends on this specific chat's history.
- 2026-09-21 — **Volume slider reveal: diagnostic test confirmed the
  hypothesis, reveal works.** Removed `on-click-right` (mute) from the
  `pulseaudio` leader entirely per Overseer's instruction. Restarted
  waybar, no errors. User tested live and screenshotted the revealed
  slider (small green gauge next to `VOL: 55%`) — reveal fires on
  left-click now. Confirms: the leader swallows the group's reveal
  click as long as it has *any* `on-click-*` handler bound, not just
  one matching the pressed button. Per Overseer's instruction this is a
  real design choice (where mute lives now), not just a bug fix —
  reported back rather than picking one unprompted. User also flagged
  the slider as too small to see; bumped the gauge from 6px/20px to
  14px/24px (trough/highlight `min-width`/`min-height`). Restarted
  again — bar height auto-grew further, 32px → 36px this time. Stopped
  there rather than pushing the size up again blind; flagged under
  Phase 1 "Still open" for a look before any further enlarging.
- 2026-09-21 — **Workspace click fixed: swapped to `aur/waybar-git`.**
  Overseer's call, documented in the prior entry: reversible, fixes
  real broken behavior (upstream Lua-dispatch incompatibility, not a
  config issue), only cost is manual rebuilds going forward instead of
  official releases. User ran `yay -S waybar-git` themselves (needed
  sudo for build deps this time, not just the final install, unlike the
  font package). Installed `waybar-git 0.15.0.r1019.g3672eee-1`
  (includes PR #5013's fix), conflict with `extra/waybar` resolved by
  replacing it as expected. Restarted waybar on the new binary, no
  errors, `waybar --version` confirms it's running the git build. Not
  yet click-tested live — this agent can't simulate a click to verify
  end-to-end, needs the user to actually try switching workspaces.
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
