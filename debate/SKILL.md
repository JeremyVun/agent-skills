---
name: debate
description: Adversarially review a backlog design.md or build_plan.md with an external model (Codex, GPT 5.6 sol) over several rounds, then triage, verify and fix the surviving findings. Use when the owner types /debate [doc] [rounds] or asks for a design doc to be stress-tested before building.
---

# Debate

The current session is the defender and editor. Codex is the attacker. Each
round Codex reads the doc and the repo, returns findings, and this session
decides which are real, fixes them in the doc, and carries the verdicts into
the next round so nothing is relitigated.

## Arguments

`$ARGUMENTS` holds up to two tokens in any order:

- a path ending in `.md` is the document;
- an integer is the maximum number of rounds. Default 3.

If no document is given, infer it: the `.md` file most recently edited or
discussed in this session, else the single `design.md` or `build_plan.md` in
the backlog item being worked on. If more than one candidate remains, ask.
Never guess between two plausible docs.

## Round loop

Run `review.sh` from this skill's directory:

    <skill-dir>/review.sh <doc> <round> [prior-verdicts-file]

It prints the findings, or `NO FINDINGS`. Then:

1. **Triage each finding.** Check the anchor exists and the evidence holds by
   reading the cited files yourself. Verdicts are FIXED, REJECTED (with the
   reason) or ASK. Codex has no design intent, so a finding that contradicts a
   decision the owner already made is REJECTED with that decision as the
   reason, not fixed.
2. **Fix.** Edit the doc for every FIXED verdict. Prefer the smallest change
   that removes the ambiguity; do not rewrite sections. Collect ASK verdicts
   and raise them in one AskUserQuestion at the end of the round, only when
   the fix has more than one defensible answer.
3. **Record verdicts** in a temp file, appended each round, one line per
   finding: `R<round> F<n> <VERDICT>: <claim> — <reason or change made>`.
   Pass this file to the next round. It exists only for the run; do not write
   it next to the doc.
4. **Stop** when any of these holds, otherwise start the next round:
   - the review returned `NO FINDINGS`;
   - nothing was FIXED this round (every finding REJECTED or answered by the owner in a way that changed nothing);
   - every finding this round is LOW severity;
   - the round limit is reached.

## Report

Finish with a short summary the owner can act on without reading the
transcript: rounds run, why it stopped, a table of findings with verdicts,
and any ASK items still open. Findings the owner rejected in an earlier
session of the same doc are worth mentioning in the doc itself as a decision,
so future debates do not raise them again.
