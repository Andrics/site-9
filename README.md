# SITE-9

Personal workstation configuration. Arch Linux / Hyprland, on an old
Intel UHD laptop — built with a hard performance ceiling and one visual
language everywhere: the **Half-Life VOX console** look (after
[suchipi/half-life-vox-console](https://github.com/suchipi/half-life-vox-console)) —
Valve-era olive panels, bevelled blocky buttons, monospace text. See
`BUILD_SPEC.md` for the actual design spec, `PHASES.md` for current
status.

## Requirements
- Arch Linux
- Hyprland (0.55+ — uses the Lua config)
- [GNU Stow](https://www.gnu.org/software/stow/) — `sudo pacman -S stow`

Why Stow and not chezmoi/yadm: this is one machine, no templating or
per-host differences needed. Stow is the simplest tool that does exactly
what's needed here and nothing more — matches the project's own "no
unnecessary complexity" stance.

## Setup on a fresh machine
```bash
git clone <this-repo-url> ~/site-9
cd ~/site-9
stow waybar
stow hypr
# stow <package> for anything else added later
```
Each top-level folder mirrors the `$HOME` path it targets (see `AGENTS.md`
for the exact layout convention). Stowing creates symlinks — nothing is
copied, so edits in `~/.config/...` are edits to this repo.

## Git workflow
This is a solo, single-machine project — no branches or PRs needed unless
that changes. The convention is just:
- Small, real commits — one meaningful change per commit, not one giant
  commit per phase.
- Plain-language commit messages (`waybar: switch to hazard-amber accent`,
  not `wip` or `update`).
- Push to `main` directly.

## Project docs
- `BUILD_SPEC.md` — hardware, constraints, and the design language. Read
  this before changing anything visual.
- `PHASES.md` — the single file for roadmap, status, open design
  questions, and session notes. Everything phase-related lives here, not
  split across separate files.
- `AGENTS.md` (+ `CLAUDE.md`, which just imports it) — standing
  instructions for Claude Code or any other coding agent working in this
  repo.

## Status
See `PHASES.md`. Short version: waybar is functionally done (layout,
readouts, volume slider, network picker) and is being restyled to the
VOX look as the last part of Phase 1. The rest of the desktop follows in
later phases with the same tokens.
