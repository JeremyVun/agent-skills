---
name: playtest-guide
description: Build an owner's playtest guide for a game build — an HTML page of verdict cards in play order with evidence, proposal cards and a copyable export — and fold the export back in. Use when a round of changes is ready for the owner to play, when asked for a playtest or playthrough guide, or when an exported verdict list is pasted back.
---

# Playtest guide

A single local HTML page the owner keeps beside the game while playing a build. One card per change or question, in
the order they are met; each verdict (Approve / Change / Drop, or a ruling's own answers) and note is saved in the
browser; one button copies the whole set as plain text to paste back. `template.html` beside this file is the page:
copy it, fill its placeholders (`__TITLE__`, `__HEAD__`, `__GAME_URL__`, `__BRANCH__`, the storage keys) and replace
the example `ROOMS` and `IDEAS` data.

## When a round is ready

1. **Check the build yourself first.** Read full-size frames of every beat the cards cover; strips and agent reports
   are not a check. Nothing goes on a card you have not looked at.
2. **Put the build where the owner plays it** and write its branch and commit into the header and the export line, so
   every verdict names the build it judged.
3. **New storage keys every round** (project, feature, round number), so this round's answers never mix with the last.
4. **Assets beside the page** (`assets/`): copy every board, clip and render the cards show; never link into scratch
   folders that may be cleaned.

## Cards

- **Order:** rooms in play order, cards in the order the player meets them. Each card has a chapter-start button for
  jumping straight to its moment.
- **One card per thing the owner asked for**, quoting their key line verbatim (`said`), then what changed and the cause
  found in one or two plain sentences (`see`), the before/after evidence (`pairs`, `clips`, `links`), and what is still
  weak or unseen (`look`). Plain words; no code names or file paths in card text.
- **Changes beyond the ask** each get their own card with before/after, so the owner can see and overrule them.
- **Every weakness is its own card with its evidence** (a frame, clip or render) and the choice it asks. Never one
  bundled "still weak" list: the owner cannot rule on what they cannot see.
- **Proposal cards (`IDEAS`, P1…)** for anything the round was less sure of, or that would change something the owner approved:
  what is there now, the idea, its cost, your view. Build only what is certain; propose the rest.
- **Sound:** renders from the real game with the story's marks beside them; say what to listen for and at which second;
  say plainly when nobody has heard them.
- **Say what nobody has watched or heard.** The owner's play is often the first real-speed viewing.

## Before handing over

- The page's script parses, it loads with no console errors, the export copies, and every file it names exists.
- Open it for the owner and give the game address and where to start.

## Folding the export back

1. Save the pasted export verbatim in the feature's docs (a verdicts file per round).
2. Write the round's rulings from it: approved, changes with the owner's words as the spec, reversals, proposals answered.
3. Notes on approved cards are still work; read every note, not only the verdict.
