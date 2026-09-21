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
it's in.

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
- **Performance constraints in BUILD_SPEC.md are non-negotiable.** If a
  styling idea conflicts with them, the constraint wins — flag the conflict
  to the user rather than quietly softening the constraint.
- **Work one phase at a time.** Don't start Phase 3 work while Phase 2 is
  still open. If something in a later phase blocks earlier work, say so and
  ask rather than jumping ahead.
- **Commit as you go.** Small, real commits with plain descriptions of what
  changed — not one giant commit per phase. This is a personal dotfiles
  repo, not a team project: clarity over ceremony, no need for PRs/branches
  unless the user asks for them.
- **Update `PHASES.md`** when you finish a phase (or a meaningful chunk of
  one) — status, and a short note for the next session.
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
