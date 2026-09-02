---
name: design-comps
description: Explore UI/screen design directions as cheap visual comps before writing any product code. Use when the owner asks for a new screen/layout/visual direction, when a design verdict is needed on look-and-feel, or before briefing a build agent on visually novel UI.
---

# Design comps before code

When a screen's design is open, do NOT iterate in product code: every idea
costs a build loop and the owner cannot steer until it lands. Run rounds of
throwaway comps instead: comps → contact sheet → owner verdict → iterate on
the winner → record → only then build. A round is one workshop directory,
one contact sheet, one report and one recorded verdict. Expect several rounds;
the design is closed when the owner says so, not when a comp looks good.

## Roles

- **Orchestrator** writes the brief, relays steers, opens the sheet, records
  the verdict. It NEVER renders comps for a verdict itself: the owner judges
  agent-taste iteration, and orchestrator-made comps get refused.
- **Comp agent** is a top-taste (Opus-class) model with intent, instruments
  and creative latitude, never dictated geometry. It must LOOK at every shot
  and iterate at least once before reporting. A low-taste model given the
  same brief produces centred text and cards; the comps ARE the design.
- **Owner** rules on pixels that reach their screen, and which pixels do
  depends on their client. On a desktop CLI, an image read into the chat is
  seen by the model only: open the contact sheet in their browser (or a shot
  in the OS image viewer). On a mobile chat client, opening reaches nothing:
  the owner sees only what the agent reads into the conversation. Assume
  desktop unless told otherwise; ASCII and prose are never comps.

## Project inputs

The project's design-process doc (or its UI contract) supplies these; the
brief restates them, and if one is missing, the first round establishes it:

- The standard frames (sizes) and every colour scheme the product ships.
- The stress scenarios a screen must survive (longest strings, degraded and
  error states, both ends of any positional device, deepest scroll, the
  least flattering content).
- Where real data, real stylesheets, real fonts and real copy live.
- Where the durable design record and calibration assets live, and any
  existing screenshot instrument to inherit.
- Which mechanics, information architecture and rules are FROZEN.

## The round

1. **Spec = the owner's words.** Number the owner's complaints or intents
   near-verbatim and put them at the top of the design doc and the brief.
   Every direction must answer every item in one composition; divergence is
   forced into HOW, never into which item gets skipped. Paraphrases get
   decorated around; verbatim complaints get answered.
2. **Real materials only.** The product's stylesheet copied verbatim (not
   re-typed) as the comp base, its real fonts, real copy in its voice, and
   real values from its own data files. Never lorem ipsum, never invented
   values. Where the real data cannot show a required state (no delayed
   record on a clean day, no reverse journey captured), apply the smallest
   named synthetic delta and declare it in the data file, the sheet lede and
   the report. Flag any comp property that is a fixture artifact so the owner
   does not rule on it.
3. **Workshop in one /tmp directory per round**, numbered, inheriting the
   previous round's files. It holds the concept HTMLs, base.css, data.js,
   shoot.js, index.html (the contact sheet), the pinned exemplar image and
   OPTIONS.md. The repo stays untouched until the verdict is recorded. The
   disk is the transcript: a fresh agent must be able to reclaim the round
   from the directory alone.
4. **Force divergence.** 3–5 genuinely different concepts, not one at three
   sizes, and at least one braver than the brief strictly needs. Each concept
   states: the idea in three sentences and its emotional target; where every
   numbered spec item lands; motion language; build cost S/M/L; one honest
   "why this might be the wrong choice" line; and a passes log of what each
   iteration fixed and why. Mechanics and IA settled earlier stay frozen;
   iterate composition only. When a concept can only satisfy the spec by
   breaking a binding rule, present that as an explicit owner call in the
   report, never absorb it.
5. **Shoot every concept at every standard frame, in every scheme, in every
   stress scenario.** Full-resolution device-pixel-ratio-2 PNGs, never
   resampled. Where a decision lives in a few pixels, capture a clipped
   region at 4× from the live cascade rather than enlarging a PNG.
6. **Build the contact sheet** (below) and **write OPTIONS.md** (below).
7. **Verdict.** Show the sheet through the owner's channel (open it in the
   browser on desktop; on mobile, read the exemplar and each direction's
   decisive frames into the chat at full resolution, in sheet order), then
   ask the verdict questions. Read the key shots yourself either way so you
   can discuss them. A verdict
   is often a synthesis, not a pick; the synthesised comp then becomes the
   calibration exemplar. Record the owner's words near-verbatim in the design
   doc immediately, as a dated round-N section: workshop path, sheet name,
   each ruling, what carries forward, and what was refused.
8. **Iterate on the winner.** Every later comp is rendered like-for-like and
   shown side-by-side against the exemplar, with the owner's complaint in the
   next brief near-verbatim. Steal the best organ of each rejected concept;
   a losing direction usually contains one right idea.
9. **Close.** Migrate into the project's durable design authority: the chosen
   composition, measured constraints, per-element rulings, contract or
   vocabulary amendments, and every defect found in comps restated as a build
   invariant with a test. Move the exemplar image to a durable path before
   the workshop folder is deleted. Brief the build against the exemplar
   image, not prose. Keep no build plans, rejected comps or history outside
   git.

## The contact sheet

One HTML file the owner opens in a browser. Its job is to make the decision
obvious without reading the report.

- **Title and lede** name the round, the question it answers, what is real and
  what is synthetic.
- **A "things to judge" block** at the top: the two or three decisions the
  owner is being asked to make this round, each pointing at the frames that
  decide it, with the recommendation stated.
- **The exemplar row first**, visibly marked: the shipped screen or the last
  round's winner, the thing every comp must beat.
- **One section per direction**: label, a two-sentence note, then a
  horizontally scrolling strip of frames in a fixed order (hero, the decisive
  stress shot, degraded states, deep scroll, the second frame size, the other
  scheme). Same order for every direction so the eye can compare down the page.
- **Decisive comparisons**: the same scenario across all directions side by
  side, one row per scenario that decides the round.
- **Before/after pairs** when iterating on the exemplar, the owner's frame on
  the left and the corrected frame beside it.
- **Zoom figures** for anything decided at pixel scale.
- **Captions carry measurements**, never adjectives: heights, counts above
  the fold, contrast ratios, scroll positions, deviation from true.
- Frames display at roughly phone width so a row of them fits the screen,
  with the full-resolution file one click away.

## OPTIONS.md, the round's report

A complete handoff, in this order:

1. Where everything is, the recommendation in one line, and a pointer to the
   findings that outrank the concepts.
2. Ground rules the round was held to: the spec, what was borrowed, what data
   and why each source, every synthetic delta, what stayed frozen.
3. **Findings that outrank the concepts**: measurements that decide the round
   regardless of taste (a count that changes between frames, a contrast that
   fails per scheme, a rule that cannot be kept). These lead because they are
   the part of the report that is not opinion.
4. Per concept, the block from step 4 of the round.
5. Vocabulary and contract additions the comps need, each named for an owner
   call.
6. Recommendation, with named transplants from each loser and a "why this
   over each other direction" paragraph, including the condition under which
   the recommendation flips.
7. Open questions for the owner, numbered.
8. What the next agent must know: shoot invocation, scenario names, instrument
   traps found this round, class-name collisions with the copied stylesheet,
   layout traps that cost a cycle.

## Instrument requirements

Inherit the project's screenshot instrument where one exists; otherwise the
first round builds one and later rounds inherit it. Whoever touches it leaves
it cheaper for the next round. It must:

- Drive the browser through its devtools protocol with a device-metrics
  override, and ASSERT the resulting viewport width AND height, refusing to
  save a frame otherwise. Command-line window sizing silently clamps on some
  platforms and crops the PNG; a wrong frame is worse than no frame.
- Ship the viewport meta the real product ships; mobile emulation without it
  lays out at desktop width.
- Emulate each colour scheme through the browser's media emulation, so comps
  exercise the product's own scheme rules with no CSS fork.
- Report per shot: any element past the right edge, any element past the
  fold, any tap target under the product's minimum, text that spills its box
  (scroll width over client width, separated from deliberate ellipsis
  clipping) and, where the content lives in a scroller, counts and scroll
  position measured against the scroller's box rather than the viewport.
- Size every fixed track against the widest legal value in the vocabulary,
  not the scenario's value: an over-long right-aligned line start-aligns and
  silently invades the column to its left, and no overflow probe fires.
- Use classic scripts for file:// comps (modules are blocked by the opaque
  origin), a unique browser profile per round (a locked profile from an
  orphaned headless tree fails with an unrelated error), and kill the browser
  in a finally block.
- Comps whose artifact the OS re-renders (icons, widgets, notifications) pass
  through the real system renderer before the verdict.

Believe the instrument over the CSS: when it reports a viewport lie or a
below-fold element, fix the instrument or the comp, never silence the probe.

## Craft rules

These belong verbatim in the comp agent's brief.

- **Borrow, don't invent.** Inventory the product's visual grammar first
  (type scale, letter-spacing, label and row idioms, how it already handles
  the thing being designed) and assemble every concept from house parts. A
  new screen is an existing idiom promoted to a new context. If there is no
  language to borrow, establishing one exemplar IS the exploration.
- **Measure before a concept depends on a perceptual property.** Items above
  the fold per frame, contrast of every colour against every ground in every
  scheme, the widest string against its track, geometric truth of any device
  that claims to be to scale; for imagery, edge luminance and crop floors.
  Numbers kill weak concepts honestly and early.
- **Photograph the stress case.** A comp that survives its worst content is a
  design; one that survives its best is a mockup.
- **Argue each choice from the material and record the argument in one line.**
  Which of two data sets, which crop, which frame proves the complaint. When
  colour or a device carries no information the existing marks do not, say so.
- **Subtraction is the default.** Each pass leaves less chrome, fewer
  devices, emptier edges. Type like an editorial spread: one column measure,
  one scale ladder, letterspaced small-caps labels, no centred blocks. A
  label that explains a gesture is a design admitting it failed.
- **Copy is a material.** Real verbs in the product's voice, real values,
  lines mined from the project's own docs; the best copy usually already
  exists unused.
- **UI over imagery is a photography problem.** Type sits in the image's own
  quiet third, respects gaze and eye-line, extends the image's darkness with
  gradients. Never a scrim box or blur panel. Ask for source-art changes as
  in-camera direction, and name any derivative-looking generated art for
  reroll.

## Operating rules

- Relay owner steers to a running comp agent immediately, as binding over the
  brief where they differ, with what-this-changes spelled out.
- Fold every ruling into the design doc the moment it lands, so later briefs
  cite the doc and never the chat.
- A round's brief carries the exemplar image, the numbered spec, the frozen
  list, the frames, schemes and scenarios, the instrument to inherit, and the
  previous round's "what the next agent must know" section.
