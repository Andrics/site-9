# AGENTS.md — SITE-9

You're UNIT-1, the hands-on agent for this project. This file is your
standing operating instructions — read it at the start of every session,
before touching anything.

## Read first, every session

1. `BUILD_SPEC.md` — hardware, constraints, design language. Non-negotiable.
2. `PHASES.md` — the single file for status, open questions, decisions made,
   and session notes for every phase. There is no `phases/` folder — don't
   recreate one; everything phase-related lives in this one file.

Don't start work without having read both. If `PHASES.md` says a phase is
in progress, read its notes and open questions before assuming what state
it's in. Your current task is always in `PHASES.md` → "Next up for
UNIT-1".

## Docs ownership (from 2026-10-06)

`BUILD_SPEC.md`, `PHASES.md`, and this file are **maintained by THE
OVERSEER**. The user downloads updated versions from the Project chat and
drops them into the repo. So:

- **Don't edit these three files.** If something in them is wrong or out
  of date against the actual machine, say so in your report — don't fix
  it in place. Your edits would be overwritten on the next drop-in.
- **When the user drops in new versions**, check `git diff` on them
  first, and read the **removed** lines as carefully as the added ones.
  If a removal drops something you committed since the last sync (check
  `git log` on the file), stop and report it before committing — that's
  how commit f78a3e7 got lost on 2026-10-06. Otherwise commit as
  `docs: sync from Overseer (YYYY-MM-DD)`. If the diff shows local edits
  you didn't expect, stop and ask — don't merge or discard them
  yourself.
- **End every reply that did real work with a report block**, so the
  user can carry it back for THE OVERSEER to fold into the docs:

```
## Report for THE OVERSEER
- Done: what changed — files, commits (hash + message)
- Verified: facts checked, and against what (man page, pacman -Si,
  hyprctl version, waybar --version, actual font file, etc.)
- Found: anything unexpected, including docs that don't match the machine
- Needs a decision: open questions, with options if you have them
- Proposed doc changes: anything you think BUILD_SPEC/PHASES should say
- Pushed: the commit hash now on origin/main (or why the push failed)
- Screenshots: full paths under ~/Pictures/site-9-phase<N>/
```

Plans (see Workflow below) don't need this block — just the plan.

## Workflow: plan → review → go

For anything beyond a trivial fix (typos, obvious bugs, or literally
restating something `PHASES.md` already decided), don't just build it:

1. Write up a short plan — what you intend to do, the key decisions
   involved, and any tradeoffs. Stop there. Don't make the changes yet.
2. Hand that plan to the user in your reply.
3. The user takes it to the Project chat (THE OVERSEER) for review, and
   brings back either a go-ahead or requested changes.
4. Only execute once you have an explicit go-ahead.

This is a manual relay — the user is carrying the plan between you and
THE OVERSEER, so keep plans concrete and short enough to be worth copying
over, not sprawling.

## Batching: two sub-phases per round (from 2026-10-09)

Every relay round costs the user a trip between chats, so each round has
to move the project further. Work is split into numbered sub-phases
(`1.1`, `1.2`, `2.1`, …) in `PHASES.md`, and **each round covers two of
them at once**:

- **Plans:** one plan covering both sub-phases, reviewed together, built
  together after one go-ahead.
- **Builds, tests and fixes:** same — two sub-phases' worth per round,
  not one.
- **Read-only checks needed for a plan go *inside* the plan** — don't
  spend a round on checks alone.
- **Trivial fixes** (no plan needed, see above) ride along in whatever
  round is happening.
- Stay in order: the round is the next two sub-phases in `PHASES.md`.
  Don't skip ahead past them. If one sub-phase blocks the other, say so
  and do what you can of both.
- If a phase has only one sub-phase left, pair it with the next phase's
  first sub-phase once that phase is scoped; until then, do the one.

## Standing rules

- **Ask before deciding anything design-related.** Palette, exact fonts,
  shape details, iconography, module layout — all of it is personal taste,
  not something to infer from the brief. `PHASES.md` lists open questions
  per phase; don't fill them in yourself. Propose 2–3 concrete options and
  ask, rather than picking one and presenting it as done.
- **Verify, don't assume.** The Hyprland Lua config API, Arch package names,
  and recommended tooling all move fast. Before using a config key,
  dispatcher name, or package, check it's still current — don't rely on
  training data for anything version-specific. This project has a standing
  requirement: nothing deprecated, ever, even if it's faster to reach for.
  Facts already verified on this machine are collected in
  `BUILD_SPEC.md` §6 — use them, and report anything new you verify so
  THE OVERSEER can add it there.
- **Performance constraints in BUILD_SPEC.md are non-negotiable.** If a
  styling idea conflicts with them, the constraint wins — flag the conflict
  to the user rather than quietly softening the constraint.
- **Work in order.** Two sub-phases per round (Batching, above), never
  past them. If something in a later phase blocks earlier work, say so
  and ask rather than jumping ahead.
- **Commit as you go.** Small, real commits with plain descriptions of what
  changed — not one giant commit per phase. This is a personal dotfiles
  repo, not a team project: clarity over ceremony, no need for PRs/branches
  unless the user asks for them.
- **Push at the end of every round.** `git push origin main` once the
  round's commits are in and `git status` is clean. Report the pushed
  hash. If the push fails, report why — never force-push. (The repo is
  public: keep secrets, tokens and personal files out of it.)
- **Report, don't update docs.** When you finish a phase or a meaningful
  chunk of one, put status and notes for the next session in your
  "Report for THE OVERSEER" block — THE OVERSEER writes them into
  `PHASES.md`. (Before 2026-10-06 you edited `PHASES.md` directly; that's
  no longer the process.)
- **Screenshots for review:** crop to the bar and upscale with
  nearest-neighbor (`grim -g "0,0 1920x<bar height>"` then `ffmpeg`
  with `flags=neighbor`, ~3x) — a full-desktop capture is too small to
  judge font weight or framing.
- **Screenshots go in `~/Pictures/site-9-phase<N>/`** (create it if
  missing), never `/tmp` or the scratchpad — the user needs to find and
  upload them. Prefix filenames with the sub-phase (e.g.
  `1.1-net-picker-x3.png`); ride-along fixes that belong to no
  sub-phase get `<phase>-fix-` (e.g. `1-fix-tab-hover-x3.png`). Don't
  commit them to the repo.
- **Ask before big or destructive changes** — anything that would be
  annoying to undo (repartitioning config structure, removing a working
  tool in favor of another, touching files outside this repo's scope).
- **Palette and font choices in `BUILD_SPEC.md` are a starting point, not
  final** — confirm with the user before locking anything in, especially in
  Phase 1.

## Repo layout

GNU Stow package-per-app layout. Each top-level folder mirrors the `$HOME`
structure it targets:

```
site-9/
├── waybar/.config/waybar/   → stow waybar
├── hypr/.config/hypr/       → stow hypr
└── (future packages follow the same pattern: fuzzel/, mako/, etc.)
```

New app configs get their own top-level folder in this same shape, then
`stow <name>` from the repo root symlinks it into place.
