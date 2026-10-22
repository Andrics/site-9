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

**THE OVERSEER's working rules from the user (2026-10-09)** — on top of
the Project instructions, for every Overseer chat:
- End every reply with a short **"What to do"**: concise, easy,
  step-by-step actions for the user. It comes last, after /clear and
  the Relay.
- If a question's answer would drastically change the relay to UNIT-1,
  **ask it first, before drafting anything** (docs or relay).
- Explain things in plain words; the user isn't always familiar with
  the jargon (e.g. "passphrase" = WiFi password).

**Added 2026-10-18:**
- **Chat-size check, every reply:** estimate how much context the chat
  has built up and how fast each round is adding to it (screenshots
  and full doc rewrites are the big ones), and say whether the user
  should start a new Overseer chat in this Project. Every reply re-reads
  the whole chat, so a long one burns usage on every turn.
- **When recommending a switch,** include a short paste-ready prompt
  for the new OVERSEER that says where things were left off (the docs
  carry the details).

## Status

| # | Phase | Status |
|---|-------|--------|
| 0 | Waybar — functional baseline (modules/layout) | Done |
| 1 | Waybar — Half-Life VOX restyle (+ network picker) | Done (2026-10-18) |
| 2 | System theme (terminal, GTK apps, file manager, Firefox, cursor/icons, window borders/wallpaper) | In progress — all built (rounds #10–#12) except 2.4 Firefox, which is round #13 |
| 3 | Shell polish (fuzzel/mako/hyprlock) | Not started — next to scope (round #14) |
| 4 | Motion (Hyprland animations/window rules) | Not started |
| 5 | Login screen | Pulled forward — 5.1 SDDM theme in round #13 (scope: login screen only) |
| 6 | Sidebar (+ SITE-9 settings panel) | Not started |

## Next up for UNIT-1

_Written by THE OVERSEER; replaced whenever there's a new task._

**Round #13 build (2026-10-22): 2.4 Firefox + 5.1 login screen** (Phase 5
pulled forward — user asked; Phase 2 closes with 2.4). Spec:
`BUILD_SPEC.md` §3 (tokens, look rules, "Firefox", "Login screen"), §2.
Check every key, pref, QML type and package against the installed
files and the package database, not memory. One commit per step;
`git show --stat` after each. If a piece can't be done as written, stop
that piece, report options, carry on with the rest. `AGENTS.md` rules on
the user's windows, killing processes (new: check what a PID owns
first) and `sudo`/AUR commands (new: the user runs them) apply.

0. **Docs sync** — `git diff` (BUILD_SPEC, PHASES, AGENTS **and
   README**), read the removed lines, commit
   `docs: sync from Overseer (2026-10-22)`.

**Already answered — user, 2026-10-22: "all leans"** (don't re-ask):
- a. Login program: **SDDM (installed) + a SITE-9 SDDM theme** — not
  greetd + ReGreet.
- b. Look: **P1 "access terminal"** (`BUILD_SPEC.md` §3 "Login
  screen"); render P2 (DOS-style full-screen prompt) beside it, the
  user picks on screen.
- c. Phase 5 scope: **login screen only** for now (no boot menu or
  boot splash).
- d. Firefox: **userChrome.css** (+ userContent.css for new-tab and
  blank pages only); websites untouched. Not a theme manifest.
- e. Dolphin's faded hidden files: **accepted** as they are.

**Report gaps from round #12** (read-only, answer in the report):
- G1. Resend these four lines in full — they were cut off in the
  relay: the "socket-activated and …" line (polkit-agent-helper-1);
  the cursor package line ("ships Chicagoicago95_Emerald…"); the
  groupbar line ("…thin indicator … over"); the screenshots note on
  the V1/V2 renders ("These … band was removed").
- G2. hyprpaper: version, config format (still hyprlang?), memory use
  (RSS), idle CPU over ~60 s, and why it was picked over Hyprland's
  background color.
- G3. Why lxqt-policykit instead of mate-polkit (the lean)?
- G4. Is 32 one of Chicago95_Cursor_White's native sizes? List them.
- G5. The user's workspace-2 kitty closed during your tests. For each
  PID you killed, what was it (`args`)? Could one kitty process have
  served the user's window too (kitty can run several OS windows from
  one process — e.g. `--single-instance`, or a window opened from an
  existing kitty)? Check how your test kitties were started.
- G6. Where does the `dbus-update-activation-environment … --all`
  come from that makes R4 redundant? If it runs **after** the env
  lines, drop R4's line (ride-along commit); otherwise keep it.
- G7. The "a few pixels 1 off the tokens" (`e5a84f`, `cacfc7`): which
  surfaces exactly? Is the leftover root `polkit-agent-helper-1` gone?
- G8. Confirm the user removed polkit-gnome, hyprpolkitagent and
  hyprland-qt-support (`pacman -Q`), and lxqt-policykit still
  registers after that.

**2.4 — Firefox (userChrome.css):**
1. Checks: installed Firefox version; the pref
   `toolkit.legacyUserProfileCustomizations.stylesheets` exists and
   works in this version; the user's profile path; Firefox's own CSS
   for the parts we restyle (from `omni.ja` / `browser/omni.ja`, not
   memory — selectors change between versions). Note what Firefox
   draws with `box-shadow`, gradients, radius and transitions.
2. **Build and test in a scratch profile** (`firefox --new-instance
   --profile <scratch dir>` on a spare workspace) — **never restart or
   close the user's own Firefox**. The user restarts theirs when the
   pick is live.
3. Write `userChrome.css` from the tokens — small, commented, every
   hex naming its token:
   - Tab strip and toolbars `--panel`; tabs raised, **selected tab
     pressed in** (`--field`, `--text-bright`) like waybar's tabs;
     URL bar and search fields recessed `--field`; popups and menus
     like the picker (`--field`, selected row `--panel` +
     `--text-bright`, flat `--bevel-dark` edge).
   - 1px bevels, radius 0; **no `box-shadow`, gradients, blur or
     transitions/animations** anywhere in the chrome (§2/§3);
     DepartureMono Nerd Font 11px.
   - **userContent.css:** new-tab, home and blank pages in `--field`
     only. Websites stay as they are.
   - The pref goes in the profile's `user.js` (commented). Repo layout:
     a `firefox/` package plus a short install step that links
     `chrome/` and `user.js` into the profile (the profile dir name is
     random, so stow alone can't target it) — propose the exact method
     in the report if stow can't do it.
4. Render on screen (scratch profile), **user picks**: Firefox
   density **normal vs compact** (check how compact mode is enabled
   in this version) and anything you had to choose that §3 doesn't
   cover.
5. Put the pick in the user's profile (back up the profile's
   `prefs.js`/`user.js` first); tell the user to restart Firefox
   themselves.

**5.1 — Login screen (SDDM theme):**
6. Checks: `systemctl is-enabled sddm` / `status`, what shows at boot
   (journal), `/etc/sddm.conf` and `/etc/sddm.conf.d/*`, current
   theme, greeter binary (`sddm-greeter-qt6`?), display server for the
   greeter (X11 or Wayland) and whether `xorg-server` is installed,
   which session file starts Hyprland (`/usr/share/wayland-sessions/`).
   **`BUILD_SPEC.md` §4 says Hyprland is "started by hand" — correct
   it if SDDM starts it.** Also: the theme API available (QML imports
   SDDM provides, `metadata.desktop` `QtVersion=6`), and how the
   `sddm` user's fonts render — **our antialias-off fontconfig rule is
   per-user and won't reach the greeter**; report options (QML text
   render settings, or a system-wide copy of the rule — ask before
   writing anything under `/etc`). If SDDM isn't what's on screen at
   boot, stop the switch-on part (step 9) and report.
7. Write the theme in the repo (`sddm/site-9/`: `Main.qml`,
   `metadata.desktop`, `theme.conf`): P1 per §3. Every color a token,
   1px bevels as separate edge rectangles, radius 0, **no
   animations/transitions**, static text cursor (no blink), clock
   `HH:MM` updated once a minute. Background: the facility wall
   **without the placard** — add a flag to `make-wallpaper.py` (e.g.
   `--no-placard`); the PNG goes into the installed theme dir only,
   **never into the repo** (it contains the logo).
8. **Preview without logging out:** `sddm-greeter-qt6 --test-mode
   --theme <repo theme dir>` (check the flag) as a floating window on
   a spare workspace. Render **P1 and P2**, plus P1's states: normal,
   `ACCESS DENIED`, `CAPS LOCK ON` (fake the states in test mode if
   needed). **User picks on screen** (also: password mask character,
   whether to show the session selector).
9. **Switch-on, only after the preview passes:** give the user the
   exact `sudo` commands to run **in their own terminal** — copy the
   theme to `/usr/share/sddm/themes/site-9/` and write
   `/etc/sddm.conf.d/site-9.conf` (`[Theme] Current=site-9`, plus
   `CursorTheme=Chicago95_Cursor_White`, `CursorSize=32` if the keys
   exist in 0.21.0). Back up any existing SDDM config first. Preview
   once more from the installed path. **Don't log out or restart
   SDDM** — the user checks it at their next reboot. Put the recovery
   steps in your report (text login on Ctrl+Alt+F2 → remove the conf
   file → `sudo systemctl restart sddm`).

**Test:** Firefox chrome pixels on token values, no shadow / radius /
fade anywhere (hover a tab, open a menu); scratch profile removed after;
SDDM preview pixels on token values (no 1-off — no Hyprland CM in the
greeter), DepartureMono crisp, nothing animating while idle;
`hyprctl configerrors` empty; waybar log clean, 1920×30.

**Screenshots:** `~/Pictures/site-9-phase2/2.4-firefox-<option>-x3.png`
(tab strip + URL bar crop), `2.4-firefox-menu-x3.png`;
`~/Pictures/site-9-phase5/5.1-login-P1-x1.png`, `5.1-login-P2-x1.png`,
`5.1-login-panel-x3.png`, `5.1-login-denied-x3.png`,
`5.1-login-caps-x3.png`.

**Then** push to `origin/main` and report (pushed hash, screenshot
paths, G1–G8, the picks, the exact switch-on commands given to the
user).

**Next round (#14), for planning only:** Phase 3 (shell polish: mako,
hyprlock, launcher) once the user scopes it — hyprlock should match
the login panel. Phase 4 (motion) after.

## Phase 1 — Waybar restyle

Goal: the bar (and its network picker) in the **Half-Life VOX console**
look (`BUILD_SPEC.md` §3) — replacing the old placeholder styling and,
since 2026-10-09, the HUD-era restyle too.

**Current look:** the VOX re-skin locked 2026-10-18 — `BUILD_SPEC.md`
§3 is the source of truth. Much of "Decided so far" below is HUD-era
history (green accent, corner ticks, double-strike), kept for the
reasoning behind it; where it disagrees with §3, §3 wins.

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

**Closed 2026-10-18** on the user's on-screen look at round #8 ("Much
better"). Carried forward:
- **The user wants to change some things later** — not listed yet.
  Ask when they're ready; they'd be a later round, not a reopening.
- **SITE-9 system settings panel** → moved to **Phase 6** (user,
  2026-10-18), with the sidebar: both need the same new widget tool.
- **Tab hover:** "no change" is THE OVERSEER's default, not asked —
  the user can change it.
- **Slow refresh** (right-click NET / F5, one 12 s run): left as is
  (user, 2026-10-18).

**Resolved:**
- **Round #8 (1.3 waybar + 1.4 picker VOX re-skin) — built, tested,
  pushed (`105c8fb`, 2026-10-18).** Approved by THE OVERSEER. Commits:
  a28bb36 docs sync; 28a012a double-strike dropped + Adwaita button
  text-shadow cleared; 4d78610 corner ticks and `frame/` removed;
  971e739 VOX tokens (`@define-color`); c423a8d VOX surfaces; d45826a
  troughs/unlit steps `--bevel-dark`, muted VOL `--text`; 332aa63 VOL
  field on the drawer group (slider inside it); fd6dbbd VOX tooltips;
  d35be18 fuzzel VOX colors; 410fcf9 pointer hand-back only on the
  first menu of a NET click; 105c8fb background rescan after connect.
  Tests: bar 1920×30, log clean, bevels pixel-exact, no bright column,
  flagged states as specced, slider inside the field (user saw it
  live), picker opens in 97 ms 8px under the bar, matches white, toggle
  works, F5 keeps the menu open with the pointer anywhere, reconnect →
  full list (user). Ride-along for round #9: Adwaita's 200ms eased fade
  on tabs → `transition: none` (THE OVERSEER, applying §3 motion).
- **Round #7 (1.1 picker + 1.2 volume) — built, tested, pushed
  (`b4352b8`, 2026-10-18).** Approved by THE OVERSEER. Commits from
  `cf4319a`: 90ef4f3 / eb72659 / 55d5ef3 / 42b792b docs syncs (removed
  lines checked each time); c854b79 volume gauge 80×4 cream, Adwaita
  cleared, 5% scroll; b6925bc height 30; 63ece26 active tab keeps
  accent on hover (moot under VOX); 5b8ca6b stopgap `fuzzel.ini`;
  1f1d77e / 61ea7f8 networkmanager-dmenu (then replaced); 2876cec
  `net-menu` script behind NET; 088cf43 networkmanager-dmenu removed
  (also uninstalled); c341142 pointer hand-back after fuzzel opens,
  menu 2 chars wider (`[ACTIVE]` was cut off); b4352b8 instant open
  from NM's cache, F5 / right-click rescan, NET tooltip off. Results:
  - Cursor/second-click bug: traced with `WAYLAND_DEBUG` to Hyprland
    giving the new fuzzel layer pointer focus; fixed with a
    zero-distance pointer move (`BUILD_SPEC.md` §6).
  - Passphrase test (a), run by the user 2026-10-18: wrong password →
    `WRONG PASSPHRASE` re-prompt, failed profile deleted; right password
    connected; one TransworldNet profile left; the password never
    appeared in any argv (watcher log). No popups from the picker.
  - Slow open traced to nmcli's 30 s auto-rescan (hung ~30 s twice);
    fixed by opening from the cache. Cache can be thin right after a
    reconnect → background rescan after connect added in round #8.
  - Scratch renders of layouts A/B × double-strike/regular
    (`1-pivot-*-x3.png`); live bar untouched. Ignore the two old
    `1.1-net-menu-alt-*` files in `~/Pictures/site-9-phase1/`.
- **Design picks for the VOX re-skin (user, 2026-10-18): "all leans".**
  Regular weight everywhere (double-strike and its §2 exception
  retired); render details kept (inactive tabs `--text`, `SITE-9`
  raised + white, 1px bevels, dark bar bottom edge); warning/critical
  brightened to `#e6a84f` / `#ff7a5c` (old red was 2.1:1 on the field);
  rest of the token table locked as proposed; picker keeps `[ACTIVE]`;
  fuzzel colors mirror the reference's drop-down list; background
  rescan after connect. Earlier: layout A, SCP leftovers kept as
  content, no accent, no corner ticks (2026-10-09). All in
  `BUILD_SPEC.md` §3.
- **User picks during round #7 (2026-10-09/18):** picker lists networks
  only, closes on click-away, NET toggle; passphrase test (a); notices
  silent until Phase 3 (option (a)); touchpad slider bug left as is
  (waybar's `pulseaudio_slider.cpp:50` truncates instead of rounding —
  a one-line upstream fix if ever wanted; no issue filed); instant open
  + both refresh triggers; NET tooltip off.
- **Round #7 plan review and pivot options (2026-10-09):** the long
  option lists (N1a/N1b/N3, V1/V2, bar heights, pivot A/B, accent,
  ticks, notices) are settled; full text in git history (docs as of
  `42b792b`).
- Fix pass (2026-10-09): 26db176 ticked workspace tabs (active =
  `--accent`), 3ad0eb1 battery thresholds 29/14, 49b5ab6 fixed-width
  percentages via fmt `{x:>3}`. Log clean, 1920×36. Approved on
  UNIT-1's report.
- Tab hover line (1px light line on hover): Adwaita's button-hover
  box-shadow, present since before the tabs changed. Counts as a drop
  shadow under §2 — removed in cf4319a (`box-shadow: none` on
  `#workspaces button:hover`), confirmed on a 3x crop.
- Push: cf4319a on `origin/main` (2026-10-09, 27 commits, first push
  since 2026-09-21; diff checked for secrets/personal data first).
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

Goal: the rest of the desktop in the same VOX look and tokens
(`BUILD_SPEC.md` §3).

**Scope (user, 2026-10-18):** all of it — terminal, normal app windows
(GTK), file manager, Firefox, mouse cursor, icon theme, Hyprland window
borders, wallpaper. **Terminal first.** Apps the user uses now: the
file manager, the terminal, Firefox; an editor, music and chat apps
come later (theme them when they arrive). Terminal stays **kitty**.

**Sub-phases:**
- **2.1 Terminal** — kitty: colors, font on the 11px grid, padding.
  Built round #10; F3 window frame in round #11.
- **2.2 GTK app theme** — buttons, menus, dialogs for GTK3 (and GTK4 /
  libadwaita as far as it goes). Built round #11.
- **2.3 File manager** — whichever the user uses; app-specific bits on
  top of 2.2. Dolphin via Kvantum, built round #11; polkit window open.
- **2.4 Firefox** — browser UI. userChrome.css (user, 2026-10-22);
  round #13.
- **2.5 Cursor + icon theme.** Built round #12: SITE-9 icons (C2),
  Chicago95_Cursor_White 32px.
- **2.6 Hyprland window borders** — pulled forward to round #10 (user
  dislikes the gradient border on every window) and built there, with
  `hypr` stowed. Color shift fixed with pre-compensated hexes (round
  #12).
- **2.7 Wallpaper** — pulled forward to round #12 (user asked, with the
  splash quotes removed), paired with 2.5. Built: V1 without the hazard
  band, shown by hyprpaper.

**Round #9 plan (2026-10-18) — reviewed by THE OVERSEER.** Pushed
`50cd9ad` (ride-along: `transition: none` on every waybar node —
Adwaita also fades sliders, scrollbars and rows; user to check the
instant tab switch live). Findings in `BUILD_SPEC.md` §4/§6: no GTK4 or
libadwaita installed, Dolphin is Qt6, Firefox uses its own dark theme,
no Settings/FileChooser portal, no polkit agent running, sddm
installed. **User picked kitty `field` + P2** (render
`2.1-kitty-field-P2-x3.png`), with tab-bar and border feedback — now
round #10.

**Round #12 (2.7 wallpaper + 2.5 cursor/icons + R1–R5) — built,
tested, pushed (`d9e8bab`, 2026-10-22).** Approved by THE OVERSEER.
User: "Beautiful stuff!" Commits: a984dea docs sync; 2a8a77b no
default wallpaper/logo/splash, `background_color` `--bevel-dark`
(pre-compensated); 8012c69 compensated border/group colors, groupbar
square/flat/token/DepartureMono; e603da6 `bevel.py` fallback prints
one stderr line; 2b75318 QT_* pushed to the D-Bus/systemd activation
env at start; 2199394 `make-wallpaper.py`; 1255bd7 `hyprpaper.conf`;
575ff8d groupbar back to plain hexes (not shifted); 56d73ad hazard
band dropped; 2a7e179 hyprpaper shows `wallpaper.png` (V1); 42542ad
lxqt-policykit, its dialog floats; 546c052 `make-icons.py`; b634f2e
SVGs misnamed `.png` remapped by content; 7e08e4c GTK/KDE icon theme
SITE-9, GTK cursor 32px; d9e8bab Hyprland cursor env 32px.
- **User's picks:** wallpaper **V1 without the hazard band**; icons
  **C2** (Chicago95 remapped to the tokens); cursor
  **Chicago95_Cursor_White 32px**; Dolphin icon view **48px**. a–g were
  "all leans" (except b: lxqt-policykit, not mate-polkit — reason
  asked in round #13, G3).
- **Outside the repo** (backups in `~/.local/share/site-9/backup/`):
  gsettings `icon-theme` Adwaita → SITE-9, `cursor-theme` default →
  Chicago95_Cursor_White, `cursor-size` 24 → 32; `dolphinrc`
  `[IconsMode]` IconSize unset (32) → 48, PreviewSize unset (64) → 48
  (via `kwriteconfig6`); activation env XCURSOR_SIZE / HYPRCURSOR_SIZE
  24 → 32, XCURSOR_THEME unset → Chicago95_Cursor_White;
  `~/.local/share/icons/SITE-9` (3386 png, 596 svg, 11759 links);
  `~/.local/share/site-9/wallpaper.png` (the logo file there is the
  user's). hyprpolkitagent stopped, lxqt-policykit started.
- **Pick c (user, 2026-10-22):** `sudo pacman -Rns polkit-gnome
  hyprpolkitagent` — also removes hyprland-qt-support (only
  hyprpolkitagent needed it). UNIT-1 confirms in round #13 (G8).
- **After the user's 08:24 reboot:** lxqt-policykit autostarts,
  hyprpolkitagent doesn't; hyprpaper shows the wallpaper; QT_* in the
  systemd env; `hyprctl configerrors` empty.
- **Unexplained:** the user's workspace-2 kitty closed during testing
  (UNIT-1 killed only its own test kitties, by PID — asked in round
  #13, G5; new `AGENTS.md` rule); a polkit window flashed on workspace
  1 and closed by itself. A root `polkit-agent-helper-1` from the
  cancelled test was still running.
- **Accepted:** Dolphin draws hidden files faded (off-token colors) —
  user, 2026-10-22. A few Qt/GTK pixels 1 off the tokens (`e5a84f`,
  `cacfc7`) — where exactly asked in round #13 (G7).
- **Report gaps** (asked in round #13, G1–G4): four lines cut off in
  the relay; hyprpaper version/memory/idle CPU not reported; why
  lxqt-policykit; cursor native sizes.
- Phase 2 left: **2.4 Firefox** (round #13).

**Round #11 (2.2 GTK + 2.3 Dolphin + kitty frame + R1–R4) — built,
tested, pushed (`24b6bd5`, 2026-10-18).** Approved by THE OVERSEER.
User: "I'm enjoying this so far! It's all coming together nicely."
Commits: 4b457f2 docs sync (removed lines checked); b2c32e8 group
borders (R3); 3991e27 VOL padding from `#volume` only (R1 — ink-to-edge
21/20 → 11/10, NET/PWR 10/10); 8027ba9 kitty F3 frame (`bevel.py`);
d56061c `settings.ini` (message wrongly claims the theme too);
6d23a95 theme files + `.gitignore` `!.local`; 6bc75c7 VOL slider knob
cleared; c5e49eb placeholders `--text-dim`; fef87e4 Kvantum theme;
0ce6c98 `kdeglobals` + `SITE-9.colors`; aa3918f DepartureMono
antialias off; 24b6bd5 QT_* env. Installed: xdg-desktop-portal-gtk
1.15.3-1, gtk3-demos 1:3.24.52-2, kvantum 1.1.8-1. Outside the repo:
gsettings (gtk-theme Adwaita → SITE-9, color-scheme default →
prefer-dark, font Adwaita Sans 11 → DepartureMono Nerd Font 8.25,
cursor-blink true → false, overlay-scrolling true → false,
button-layout `appmenu:close` → `:`); `dolphinrc` ColorScheme
BreezeDark → SITE-9 (backup kept). R4: `~/.config/hypr` is a real dir,
the backup is outside the repo.
- **User's picks in round #11:** a none · b both square · c dotted
  focus · d no blink · e disabled `--text-dim` · f gtk3-demos; frame
  **F3** (F2 rejected: "borders need to be the same as a clicked
  workspace button"), no always-on tab strip; DepartureMono antialias
  off everywhere.
- **R2 result:** `sdr_eotf` doesn't reach Hyprland-drawn colors;
  pre-compensated hexes do (§6). Pick in round #12.
- **Mishaps (reverted, now `AGENTS.md` rules):** Space sent to
  Firefox's file dialog opened a screenshot in the user's claude.ai
  tab (UNIT-1 went Back); `pkill -f` stopped hyprpolkitagent for a few
  seconds (restarted). UNIT-1 also switched the user's workspace
  several times for screenshots.
- **User after round #11:** wants a matching wallpaper and Hyprland's
  splash quotes gone → round #12.

**Round #10 (2.1 kitty + 2.6 borders + bar trim) — built, tested,
pushed (`7ff55e8`, 2026-10-18).** Approved by THE OVERSEER. Commits:
c99efb3 docs sync (removed lines checked: old round #9 brief and the
CPU/RAM/MET spec; no UNIT-1 commits lost); f96c6a8 CPU, RAM, MET off
the bar; b3011ea kitty stow package (`kitty.conf` + `tab_bar.py`);
4472245 live `hyprland.lua` added as-is (backup
`~/.config/hypr/hyprland.lua.pre-stow.bak`); 91773c0 hyprpolkitagent
autostart, `nm-applet` and terminal autostarts dropped, stray
`.gitkeep` removed; 7ff55e8 flat 1px borders. Tests: configerrors
empty, getoption reads back the new values, polkit agent registered,
kitty's only stderr is the known portal line, waybar log clean at
1920×30. Findings in `BUILD_SPEC.md` §6 (tab-bar mechanics, border
color shift and its likely cause, polkit unit vs uwsm). Nit: the
`2.6-borders` crop is ×6 but was named `-x3`.
- **User's picks in round #10:** selection S1, cursor blink off, borders
  active `--bevel-light` / inactive `--bevel-dark`, hyprpolkitagent,
  terminal autostart dropped (THE OVERSEER had leaned keep), tab bar T3.
  All in `BUILD_SPEC.md` §3.
- **User feedback after round #10:** VOL field has too much inner
  padding next to NET/PWR (→ R1); the terminal should look like the
  VOX console — olive frame around a darker box — not field edge to
  edge (→ frame options F1/F2).
- **Border color shift:** a/b/c from UNIT-1 (accept / CM off /
  pre-compensate) are superseded by the `sdr_eotf` test (R2).

**Picks for round #11 (user, 2026-10-18: "all leans"):** G1 SITE-9's own
GTK3 theme; install `xdg-desktop-portal-gtk`; Kvantum (Q1) for Dolphin
in 2.3; kitty frame options rendered at 8px and picked on screen. GTK
settings (`gtk-theme`, `prefer-dark`, `settings.ini`, 11px font) come
with G1. Recorded in `BUILD_SPEC.md` §3–§4. The options not picked: G2
recolor Chicago95 (2px bevels, grey assets), G3 (= G1 without GTK4 — moot,
none installed), Q2 qt6ct + Fusion + QSS, Q3 kdeglobals + Breeze.

**Background (2026-09-21, superseded 2026-10-09):** the VOX reference
was first found as a terminal-only idea; the two open questions it
raised (bevels for the terminal only? a lighter register for it?) are
answered by "the VOX look everywhere". kitty takes colors only — no
bevels; its window frame comes from Hyprland (2.6).

## Phase 3 — Shell polish
Not scoped. Carry-overs: `fuzzel.ini` already gets VOX colors in 1.4
(the launcher question in `BUILD_SPEC.md` §4 is still open); mako is
unstyled, and kitty's notices (e.g. Claude Code's "waiting for your
input") show in mako's default blue until it gets a config.

## Phase 4 — Motion
Not scoped. User (2026-10-09): wants animations later, in the VOX
style. `BUILD_SPEC.md` §2 performance constraints still govern
whatever gets decided here.

**Starting point — Hyprland's stock values, left as they are in round
#10** (UNIT-1, 2026-10-18). Gaps: `gaps_in 5`, `gaps_out 20`.
Animations on. Curves: easeOutQuint, easeInOutCubic, linear,
almostLinear, quick, and spring `easy` (mass 1, stiffness 238.1191,
dampening 24.21279333). Leaves (speed / curve; speed is in
100 ms units):
- global 10 / default · border 5.39 / easeOutQuint
- windows 4.79 / easy · windowsIn 4.1 / easy, popin 87% · windowsOut
  1.49 / linear, popin 87%
- fadeIn 1.73, fadeOut 1.46 / almostLinear · fade 3.03 / quick
- layers 3.81 / easeOutQuint · layersIn 4 / easeOutQuint, fade ·
  layersOut 1.5 / linear, fade · fadeLayersIn 1.79, fadeLayersOut 1.39
  / almostLinear
- workspaces 1.94, workspacesIn 1.21, workspacesOut 1.94 /
  almostLinear, fade · zoomFactor 7 / quick

**Against the spec (THE OVERSEER, 2026-10-18):** the `easy` spring is
slightly underdamped (critical damping is 2·√238 ≈ 31, set 24), so
windows overshoot a little — a bounce, which §3 "Motion" rules out —
and windows take ~0.4–0.5 s, not "short". Easing curves beyond linear
are also against §3. Left alone on purpose until this phase; also set
`misc.vfr = true` explicitly here (§2).

## Phase 5 — Login screen
**Pulled forward (user, 2026-10-22: "the ugly default one is getting on
my nerves").** The gate is met: sddm 0.21.0 is installed (round #9);
round #13 confirms it's what shows at boot.

**Scope (user, 2026-10-22):** login screen only — **5.1 SDDM theme**.
No boot menu or boot splash for now (could be a 5.2 later, if asked).

**Picks (user, 2026-10-22: "all leans"):**
- **SDDM + a SITE-9 SDDM theme** (QML). Not greetd + ReGreet: that
  would switch the login system and add GTK4 just for this screen.
- **Look P1 "access terminal"** (`BUILD_SPEC.md` §3 "Login screen"),
  P2 rendered beside it; final pick on UNIT-1's renders.

**THE OVERSEER's checks (2026-10-22):** SDDM's latest stable release is
still 0.21.0 (Feb 2024) — slow upstream. KDE moved Plasma to its own
SDDM fork, **Plasma Login Manager** (first in Plasma 6.6), which **does
not take custom QML themes** — no use here. greetd + **ReGreet 0.5.0**
(Arch `extra`, built 2026-07; GTK4, custom CSS, runs under cage or a
compositor) is the maintained alternative if SDDM ever stalls.

## Phase 6 — Sidebar (+ SITE-9 settings panel)
Not scoped. Ask what "sidebar" should actually cover — content, trigger,
placement, all of it — before proposing anything; don't assume it carries
over from waybar's decisions.

**SITE-9 system settings panel** (user request 2026-10-09, placed here
2026-10-18): a self-built settings surface in the VOX style that takes
the network actions dropped from the picker (WiFi/networking/Bluetooth
on-off, connection editing, deleting connections, show password) and
likely more — including **system diagnostics: CPU, RAM and uptime**,
moved off the bar (user, 2026-10-18). Waybar can't build panels, so this phase needs a widget
toolkit — check what's current and maintained when it's scoped (tool
freedom, `BUILD_SPEC.md` §4). Until then those actions are only
reachable via `nmcli`/`nmtui`.

## Log

_(newest first, short entries)_

- 2026-10-22 — **Round #12 approved; login screen pulled forward;
  round #13 briefed.** New Overseer chat, picked up from the 2026-10-18
  docs. UNIT-1 built and pushed round #12 (`d9e8bab`, 15 commits):
  facility-wall wallpaper V1 (hazard band dropped) on hyprpaper,
  SITE-9 icon set (Chicago95 remapped to the tokens, C2),
  Chicago95_Cursor_White 32px, Dolphin icons 48px, lxqt-policykit
  (floating, Kvantum-themed), compensated borders, themed groupbar,
  splash/logo/default wallpaper off. Picks in Phase 2 → round #12.
  User removed the old polkit agents (pick c). Report gaps (cut-off
  lines, hyprpaper numbers, the closed workspace-2 kitty) go into
  round #13. User asked for the login screen → Phase 5 pulled forward;
  THE OVERSEER checked SDDM, Plasma Login Manager, greetd/ReGreet and
  Firefox userChrome. User: "all leans" — SDDM + SITE-9 theme, P1
  access-terminal look, login screen only, Firefox via userChrome.css,
  hidden-file fade accepted, README Status rewritten. Round #13 = 2.4
  Firefox + 5.1 login. New `AGENTS.md` rules: check what a PID owns
  before killing; the user runs `sudo` and AUR installs.

- 2026-10-18 — **Round #11 approved; round #12 briefed; Overseer handoff
  recommended.** UNIT-1 built and pushed round #11 (`24b6bd5`, 12
  commits): SITE-9 GTK3 theme, Kvantum + KDE color scheme for Dolphin,
  kitty F3 frame (8px `--panel` + recessed bevel per pane, user's own
  pick over F2), VOL padding fixed, group borders, DepartureMono
  without antialiasing (user's pick, fixes Qt's half-pixel offset).
  `sdr_eotf` didn't fix the border shift — pre-compensated hexes do.
  hyprpolkitagent's window is hyprtoolkit, unthemed. Two mishaps on the
  user's windows → new `AGENTS.md` rules. User: happy with progress;
  wants a wallpaper and the splash quotes gone. Round #12 = 2.7
  wallpaper + 2.5 cursor/icons + follow-ups. User: "all leans" on a–g
  and handed the wallpaper design to THE OVERSEER (suggested
  `andr1cs` and their logo) → "facility wall" concept, mockup shown in
  chat, spec in `BUILD_SPEC.md` §3. THE OVERSEER checked: polkit-gnome
  is dead upstream (out).

- 2026-10-18 — **Round #10 approved; round #11 briefed.** New Overseer
  chat, picked up from the 2026-10-18 handoff (Project docs matched
  UNIT-1's `c99efb3` sync). UNIT-1 built and pushed round #10
  (`7ff55e8`, 6 commits): bar trimmed to clock / VOL NET PWR tray,
  kitty live with T3 tab bar, `hypr` stowed with hyprpolkitagent and
  flat 1px borders. User's round #10 picks recorded (S1, no blink,
  light/dark borders, hyprpolkitagent, no terminal autostart, T3).
  THE OVERSEER traced the border color shift to an sRGB → gamma 2.2
  conversion (numbers match exactly) — `sdr_eotf = "srgb"` to test.
  User: VOL field padding too big; terminal should have the VOX
  console's olive frame around the field. Picks: "all leans" — own
  GTK3 theme, portal-gtk, Kvantum, frame renders at 8px. Round #11 =
  2.2 GTK + 2.3 Dolphin + kitty frame + ride-alongs (VOL padding,
  `sdr_eotf`, group borders, hypr dir check).

- 2026-10-18 — **Round #9 plan reviewed; kitty look picked; round #10
  briefed.** UNIT-1: plan for 2.1/2.2 with renders, ride-along
  `50cd9ad` pushed (instant tab switch). User: kitty **field + P2**;
  kitty's tab bar must be uniform olive with button-like tabs; the
  gradient window border on every window has to go (2.6 pulled
  forward); **CPU, RAM and MET off the bar** → settings panel "system
  diagnostics". New rule: chat-size check every reply + handoff prompt
  when switching. Round #10 = kitty build + tab-bar options + stow
  `hypr` + flat borders + bar trim; UNIT-1 asks the user five small
  picks first. GTK/Qt picks wait for round #11. THE OVERSEER
  recommends a fresh Overseer chat after this reply.

- 2026-10-18 — **Round #8 approved; Phase 1 closed; Phase 2 scoped;
  round #9 briefed.** UNIT-1 built and pushed the VOX re-skin
  (`105c8fb`, 11 commits) — review in Phase 1 "Resolved". Found:
  Adwaita's hidden button/tooltip text-shadows (now cleared), its 200ms
  eased button fade (cleared next round, per §3 motion), tooltip CSS
  node is GTK's `tooltip`, `nmcli device wifi rescan` behavior. User:
  "much better", some changes later (unlisted); **tool freedom** — not
  tied to waybar/Hyprland, any current, good tool is fine, same
  Half-Life theme (`BUILD_SPEC.md` §4). Picks (leans): slow refresh
  left as is, settings panel → Phase 6, kitty kept. Phase 2 scope: all
  of terminal, GTK apps, file manager, Firefox, cursor/icons, window
  borders/wallpaper — terminal first; apps in use: file manager,
  terminal, Firefox. Round #9 = plan for 2.1 kitty + 2.2 GTK theme,
  with the tab-fade fix riding along.

- 2026-10-18 — **Round #7 approved; VOX picks locked; round #8 briefed.
  New Overseer chat.** Picked up from the 2026-10-09 handoff (Project
  docs matched UNIT-1's `42b792b` sync). UNIT-1's report: 13 commits,
  pushed `b4352b8`; cursor/second-click bug fixed (Hyprland gives a new
  layer pointer focus; zero-distance pointer move); passphrase test
  passed (re-prompt, cleanup, no password in argv); slow open fixed by
  opening from NM's cache, F5 / right-click NET rescan; NET tooltip
  off; networkmanager-dmenu uninstalled; scratch renders of layouts
  A/B in both weights. Review: approved, one ride-along fix (skip the
  pointer nudge on F5). THE OVERSEER measured the renders: tokens
  pixel-exact; red `#b8452e` only 2.1:1 on the field. User: "all
  leans" — regular weight everywhere (double-strike and its §2
  exception retired), render details kept, warning/critical brightened
  to `#e6a84f` / `#ff7a5c`, tokens locked, `[ACTIVE]` kept, fuzzel
  colors from the reference's drop-down list, background rescan after
  connect. `BUILD_SPEC.md` §3 rewritten as the locked VOX spec (HUD-era
  sections condensed under "Retired"), §4–§6 updated. Round #8 brief
  (1.3 + 1.4) in "Next up".

- 2026-10-09 — **Layout A picked; Overseer handoff.** User picked bar
  layout A, took the leans on the SCP leftovers (SITE-9 tag as a plain
  title, labels and MET kept), left the slider touchpad bug as is,
  chose passphrase test (a). Correction: "dim `connected`" in the
  picker isn't possible in fuzzel — re-asked in round #8. New user
  rules for THE OVERSEER recorded under "How this actually works"
  ("What to do" at the end; ask drastic questions before drafting).
  This Overseer chat hands off to a fresh one; it will receive UNIT-1's
  round #7 report.
- 2026-10-09 — **SCP dropped; VOX is the only theme. Round #7 tests
  passed.** User: ditch SCP now, focus on the VOX picture, loved the
  mockup's blocky buttons, no theme mixing; update the README.
  `BUILD_SPEC.md` §3 rewritten around VOX (proposed tokens, HUD-era
  sections marked as being replaced), README updated. Read as settled:
  no HUD green, no corner ticks. Tests: VOL, NET picker all as expected;
  found a waybar slider touchpad bug (truncation, upstream) and a
  cursor/second-click bug on NET (UNIT-1 to fix). Open: layout A/B and
  weight (on renders), SCP leftovers on screen, the touchpad bug.
- 2026-10-09 — **Design pivot requested: VOX console look everywhere.**
  User: the half-life-vox-console style should apply system-wide, not
  only the terminal; the current HUD look isn't working for them.
  Tokens taken from the reference CSS, options and leans under Phase 1
  "Still open" → "Design pivot"; THE OVERSEER showed a mockup in chat.
  Round #7 continues with functional work only plus scratch renders of
  the two bar layouts; restyle is the next round once picks lock.
- 2026-10-09 — **Round #7, mid-round: picker reworked to a SITE-9
  script.** UNIT-1 built steps 1–7 (bar 1920×30, log clean). The user
  saw the networkmanager-dmenu menu live and asked for: networks only
  (other actions → a future SITE-9 system settings panel), no clickable
  blank rows, close on click-away. networkmanager-dmenu can't hide its
  actions, so it's replaced by an `nmcli` + fuzzel script (spec in
  `BUILD_SPEC.md` §3, brief in "Next up"). Connected network tagged
  `[ACTIVE]`, wrong passphrase reopens the prompt. Notices stay silent
  (option (a) by default). System settings panel recorded under
  Phase 1 "Still open", unplaced.
- 2026-10-09 — **Round #7 picks made; build is a go.** User took every
  lean: N1a (fuzzel + networkmanager-dmenu from `extra`) with a stopgap
  token-only `fuzzel.ini`, `▂▄▆█` signal, menu top-right under the bar,
  Super+R unchanged until Phase 3; V1 slider 80×4 cream, 5% scroll;
  bar 30px; active tab keeps `--accent` on hover. Locked in
  `BUILD_SPEC.md` §3 (new "Locked volume slider" and "Locked network
  picker" blocks) and §4. 7-step build brief in "Next up for UNIT-1".
- 2026-10-09 — **Round #7: plan for 1.1 + 1.2 reviewed (approved in
  structure); tab hover fix and push done.** First round under the new
  Overseer chat. UNIT-1 synced docs (49553c7; removed lines checked,
  nothing of its own dropped), fixed the hover shadow (cf4319a) and
  pushed (cf4319a on `origin/main`). Plan checks recorded in
  `BUILD_SPEC.md` §6: NM lets the user connect without polkit;
  networkmanager-dmenu's fuzzel support (masked passphrase) vs
  hyprlauncher `-m` (centred, no masking, stdout unconfirmed);
  pinentry-gtk/qt work; `hl.dsp.exec_cmd` with rules places a floating
  kitty; the bar's natural height is 24px. THE OVERSEER found:
  fuzzel's defaults are Solarized light with radius 10 (breaks §3, must
  be overridden); networkmanager-dmenu 2.7.2 is already in
  `extra-testing`. Found by UNIT-1: stray `nm-applet` autostart in the
  live `hyprland.lua` (§5), polkit agent installed but not running
  (§4), `pacman -F` unsynced. Options and leans in Phase 1 → "Still
  open". Next: the user's picks, then the build brief.
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
