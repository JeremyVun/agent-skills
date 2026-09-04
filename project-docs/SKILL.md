---
name: project-docs
description: Set up or maintain a project's docs layout, durable assets, shared tools, and concise index-style CLAUDE.md. Use when creating a project, adding a feature design, recording reference material, or repairing drift from this structure.
---

# Project docs layout

Every project keeps its documentation in a root-level `docs/` folder, durable media in a root-level `assets/` folder, agent tooling in a root-level `tools/` folder, and a concise `CLAUDE.md` index at the repo root. Create only what the project actually needs — empty placeholder files and folders are drift, not structure.

```
docs/
  project.md            # what this project is, for humans — always present
  roadmap.md            # milestones/roadmap, if the project has one
  styles.md             # visual design language, if the project has a UI
  contracts/            # one md per key contract/interface
  backlog/<feature>/    # design.md + build_plan.md per feature (backlog-item skill)
  references/           # external reference material, token-dense
assets/                 # durable images, video, audio, and other media
tools/                  # scripts agents build & share; verify, iterate, review UX
CLAUDE.md               # concise operational index at repo root
```

## Root bridging docs (`docs/*.md`)
Written for the human owner. They are the alignment bridge: the owner reads these to check that agents working on the project share their understanding. `project.md` describes the project (purpose, shape, key decisions). Add `roadmap.md` (milestones) and `styles.md` (visual/design language) only when applicable. Keep this set small — a handful of files, plain language, current.

## `docs/contracts/`
One markdown file per key contract or interface in the project (module boundaries, wire shapes, event semantics, invariants). Purpose: an agent new to the project reads these to align with the structure quickly, without spelunking code. State each contract precisely — inputs, outputs, ordering/timing semantics, and the invariants that must hold. Update the contract doc in the same change that alters the interface; a stale contract is worse than none.

## `docs/backlog/<feature>/`
Each feature gets its own folder with a self-contained `design.md` and, unless the item is very small, a phased `build_plan.md`. All file names are lowercase. The `backlog-item` skill owns what these documents must contain and how an item moves through design, build and closeout; when a feature ships, its lasting decisions migrate into contracts/root docs and the folder is deleted via the `backlog-item` close stage.

## `docs/references/`
External reference material (API docs, protocol notes, upstream specs). Audience is mainly AI agents, secondarily humans: maximise information per token — terse, factual, no marketing prose, no boilerplate. Ground these in the actual upstream source (fetch real docs/specs; verify against the live system when safe) and note the retrieval date and source URL at the top.

## `assets/`
Durable non-code media used by the product, documentation, tests, or calibration belongs here, including images, video, and audio. Organize it by stable purpose when useful and update consumers when moving files. Do not retain exploratory variants, evidence screenshots, generated scratch output, or backlog history merely because the files exist. Create the folder only when the project has an asset worth preserving.

## `tools/`
All scripts and tooling created by agents working on the project, kept so they can be shared and reused across sessions. Agents are encouraged to build tools to verify findings, iterate, and review usability — user-experience quality is make or break, so drive the real artifact, don't just run tests. Give each tool a usage comment/header at the top; a `tools/README.md` one-liner index helps once there are more than a few.

## CLAUDE.md
Very concise: operational and orientation information only — the project structure, commands to build/run/test, and where to find things (pointers into `docs/`, `assets/`, and `tools/`). It is an index, not a manual: if content is more than a couple of lines, it belongs in `docs/` with a pointer here. No narrative, no duplicated doc content.

## Maintaining
When asked to "set up docs", create the skeleton above (only applicable parts) and populate `project.md` and `CLAUDE.md` immediately. When working on any project that follows this layout: keep contracts in sync with interface changes, preserve durable media in `assets/`, add references when you fetch external material worth keeping, and put reusable scripts in `tools/`. Disposable generated output belongs in the system temporary directory, not `assets/` or an ad-hoc repository location.
