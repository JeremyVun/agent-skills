---
name: council
description: Blind playtest of a game section by Opus and Sol from contact sheets, then a findings doc comparing what they understood with the design. Use when the owner types /council [section], asks for a council round, or wants outside eyes on how a level reads, paces and feels.
---

# Council

A hill-climbing experiment: two models play a section of the game as blind players and report what they saw, felt and
understood. The target is both rating it at least 9/10. Rounds are manual. The owner reviews every finding and decides
what to act on; never act on findings without that.

Each reviewer's narration of what happened is the main signal. Where it departs from the design is the gap between what
was written and what reaches the screen. Scores show the trend across rounds.

## A round

1. **Frames.** Capture the section at a constant rate of game time, by default one frame per game second. Resample
   if the capture is wall-timed. Keep the rate the same for every round so pacing judgements stay comparable. Use the
   project's own capture tool (see its docs for "council"). If the game has a pointer, show it in the frames along
   with a short trail of its recent movement, which one frame a second otherwise loses. Keep a per-frame record of the
   story beat for yourself; never give it to the reviewers.
2. **Review.** Run from this skill's directory:

       python3 <skill-dir>/council.py <frames-dir> <out-dir> --game "<Name>" [--fps 1] [--note "<text>"] [--previous <file>]

   It tiles the frames into timestamped sheets (`<out-dir>/sheets/`) and runs both reviewers in parallel, writing
   `opus.md` and `sol.md`. `--note` adds what any player would know about the screen, such as "The small ring is your
   mouse cursor, and the faint line behind it is where you moved it during the last second." `--previous` chains
   sections: pass the earlier round's "What happened" text so a later section is not judged cold. It takes several
   minutes, so run it in the background and wait for it.
3. **Findings.** Read both reviews in full, then the section's design docs. Write `<out-dir>/findings.md`:
   - the scores side by side;
   - where their narration departs from the design, most important first, saying which reviewer saw it, with
     timestamps and **the sheet file for each** (sheet n covers frames 12(n-1) to 12n-1 for landscape frames);
   - spell breaks, pacing, what works for them and their asks for a 10.

   Look at the sheets behind every finding you lead with and mark each finding checked or not. Note when a scripted
   player's timing, rather than the game's, shapes a pacing complaint.
4. **Hand over.** Summarise the findings for the owner, open the referenced sheets in Preview, and wait for their
   decision.

## Blindness

Reviewers get only the sheets and `brief.md`: the game's name and what a player sees. Opus runs in an empty temp folder
with its system prompt replaced (`player.md`), so it gets no project files and no memory. Codex has its base
instructions replaced the same way but still loads the user's global `AGENTS.md`. Never add design context, earlier
findings or the other reviewer's output to a round.

## Limits

One frame a second carries story, staging, poses, composition and pacing, not motion: camera smoothness and animation
quality stay with the owner's eye and the project's traces. A scripted player sets the interaction timing, so the
reviewers cannot judge how interactive the game feels.
