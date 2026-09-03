---
name: backlog-item
description: Work a docs/backlog/<feature> item through its life - design session, orchestrated build, closeout. Use when the owner types /backlog-item <feature> [design|build|close], names a backlog folder, or asks to review, design, build or orchestrate a feature that has one.
argument-hint: "<feature> [design|build|close]"
---

# Backlog item

A feature lives in `docs/backlog/<feature>/`. It always has `design.md` and,
unless the item is very small, a phased `build_plan.md`. Supporting files
(`comps/`, notes, narration drafts) may sit beside them. Lowercase names
throughout. The folder is ephemeral: when the feature ships, durable rules
migrate to `docs/contracts/` and the folder is deleted.

The two documents exist so that a **fresh context** can be briefed with the
folder plus the contracts and nothing else, with most of its budget left for
thinking about the build. Everything the build needs must be in the doc, not
in a chat.

## Arguments

`$ARGUMENTS` holds a feature name and an optional stage. With no feature,
infer it from the backlog folder discussed in this session; if more than one
candidate remains, ask. With no stage, read the folder:

| Folder state | Stage |
| --- | --- |
| no `build_plan.md`, or one whose phases are not yet ready to execute | design → read [design.md](design.md) |
| `build_plan.md` with phases not yet marked done | build → read [build.md](build.md) |
| every phase marked done | close → invoke `close-backlog-item` |

Read only the file for the current stage. An explicit stage argument
overrides detection (reopening design on a planned item is common).

## What ready looks like

`design.md` is self-contained: what and why, the mechanism precisely enough
to build from, decisions with the owner's rulings and their dates, rejected
alternatives with the reason, and no open questions left standing. A reader
who knows the codebase but not this conversation can build from it.

`build_plan.md` is phased. Each phase names the files it owns, the
behavioural contract at its seams (input semantics, event ordering, timing
handoffs), its verify gate, and a done marker. Each phase is independently
verifiable and sized so no agent approaches its context ceiling.

## Standing rules

- Owner answers given mid-work go into the doc immediately, so every later
  brief cites the doc and never the chat.
- Numbers the owner edits in an answer are the binding spec; record them
  verbatim.
- Ask the owner whenever a reading is uncertain. Aligned beats fast.
- Contracts record as-built law only. A "when X lands, do Y" note, however
  small, goes in the backlog item, never a contract.
- Closing a finished item is standing practice, not a question to raise:
  migrate what is durable, delete the folder, and say it is done.
- The build stage runs in a fresh context. If design finished in this
  session, say so and tell the owner to clear and run the build stage anew
  rather than orchestrating on a context full of design discussion.
