---
name: design-comps
description: Explore UI/screen design directions as cheap visual comps before writing any product code. Use when the owner asks for a new screen/layout/visual direction, when a design verdict is needed on look-and-feel, or before briefing a build agent on visually novel UI.
---

# Design comps before code

When a screen's design is open, do not iterate in product code: every idea
costs a build loop and the owner cannot steer until it lands. Run rounds of
throwaway comps: comps → contact sheet → owner verdict → iterate on the
winner → record → only then build. A round is one workshop directory, one
sheet, one report, one recorded verdict. Expect several rounds; the design is
closed when the owner says so, not when a comp looks good.

## Golden rules

1. **Comps are made by a top-taste (Opus-class) agent, never by the
   orchestrator.** The owner judges agent-taste iteration; orchestrator-made
   comps get refused. The comp agent gets intent, instruments and creative
   latitude, never dictated geometry, and must look at every shot and iterate
   at least once before reporting. A low-taste model given the same brief
   produces centred text and cards. The comps ARE the design.
2. **The owner rules on pixels that reach their screen.** On a desktop CLI an
   image read into the chat is seen by the model only: open the contact sheet
   in their browser, or a shot in the OS image viewer. On a mobile chat client
   opening reaches nothing: the owner sees only what the agent reads into the
   conversation, so read the exemplar and each direction's decisive frames
   at full resolution in sheet order. Assume desktop unless told otherwise.
   ASCII and prose are never comps. Read the key shots yourself either way so
   you can discuss them.

## Project inputs

The project's design-process doc or UI contract supplies these; the brief
restates them, and a first round establishes any that are missing:

- Standard frames (sizes) and every colour scheme the product ships.
- Stress scenarios a screen must survive: longest strings, degraded and error
  states, both ends of any positional device, deepest scroll, least
  flattering content.
- Where real data, stylesheets, fonts and copy live.
- Where the durable design record and calibration assets live, and any
  existing screenshot instrument to inherit.
- Which mechanics, information architecture and rules are FROZEN.

## The round

1. **Spec = the owner's words.** Number their complaints or intents
   near-verbatim at the top of the design doc and the brief. Every direction
   answers every item in one composition; divergence is forced into HOW,
   never into which item is skipped. Agents answer verbatim complaints and
   decorate around paraphrases.
2. **Real materials only.** The product's stylesheet copied verbatim, its
   fonts, its copy in its voice, values from its own data files. Never lorem
   ipsum or invented values. Where real data cannot show a required state,
   apply the smallest named synthetic delta and declare it in the data file,
   the sheet lede and the report. Flag any comp property that is a fixture
   artifact so the owner does not rule on it.
3. **One numbered /tmp workshop per round**, inheriting the previous round's
   files: concept HTMLs, base.css, data.js, shoot.js, index.html (the sheet),
   the pinned exemplar image, OPTIONS.md. The repo stays untouched until the
   verdict is recorded. The disk is the transcript: a fresh agent must be
   able to reclaim the round from the directory alone.
4. **Force divergence.** 3–5 genuinely different concepts, at least one
   braver than the brief needs. Each states the idea in three sentences and
   its emotional target, where every spec item lands, motion, build cost
   S/M/L, one honest "why this might be wrong" line, and a passes log of what
   each iteration fixed. Frozen things stay frozen; iterate composition only.
   A concept that can only meet the spec by breaking a binding rule presents
   that as an owner call, never absorbs it.
5. **Shoot every concept at every frame, scheme and scenario.**
   Full-resolution 2× PNGs, never resampled; decisions that live in a few
   pixels get a 4× clip from the live cascade.
6. **Build the sheet and write OPTIONS.md** (shapes below).
7. **Verdict.** Show the sheet per golden rule 2, then ask. A verdict is
   often a synthesis, not a pick; the synthesised comp becomes the
   calibration exemplar. Record the owner's words near-verbatim in the design
   doc at once, as a dated round section: workshop path, sheet, each ruling,
   what carries forward, what was refused.
8. **Iterate on the winner.** Later comps render like-for-like beside the
   exemplar, with the owner's complaint in the next brief near-verbatim.
   Steal the best organ of each loser; a rejected direction usually holds one
   right idea.
9. **Close.** Migrate into the project's durable design authority: chosen
   composition, measured constraints, per-element rulings, contract and
   vocabulary amendments, and every defect found in comps restated as a build
   invariant with a test. Move the exemplar image to a durable path before
   the workshop is deleted. Brief the build against the exemplar image, not
   prose. Keep no build plans, rejected comps or history outside git.

## The contact sheet

One HTML file that makes the decision obvious without the report:

- **Title and lede**: the round, its question, what is real and synthetic.
- **"Things to judge"** block: the two or three decisions asked this round,
  each pointing at the frames that decide it, with the recommendation.
- **Exemplar row first**, visibly marked: the thing every comp must beat.
- **One strip per direction**: label, two-sentence note, frames in a fixed
  order (hero, decisive stress shot, degraded states, deep scroll, second
  frame, other scheme). Same order everywhere so the eye compares down the
  page.
- **Decisive comparisons**: one row per deciding scenario, all directions
  side by side.
- **Before/after pairs** when iterating on the exemplar, the owner's frame
  left.
- **Zoom figures** for pixel-scale decisions.
- **Captions carry measurements, never adjectives**: heights, counts above
  the fold, contrast ratios, scroll positions, deviation from true.
- Frames at roughly phone width so a row fits the screen, full-resolution
  file one click away.

## OPTIONS.md, the round's report

A complete handoff, in this order:

1. Where everything is, the recommendation in one line, a pointer to the
   findings that outrank the concepts.
2. Ground rules held to: spec, what was borrowed, data sources and why,
   every synthetic delta, what stayed frozen.
3. **Findings that outrank the concepts**: measurements that decide the round
   regardless of taste (a count that changes between frames, a contrast that
   fails in one scheme, a rule that cannot be kept). They lead because they
   are not opinion.
4. Per concept, the block from round step 4.
5. Vocabulary and contract additions needed, each an owner call.
6. Recommendation: named transplants from each loser, why this over each
   other direction, and the condition under which it flips.
7. Open questions for the owner, numbered.
8. What the next agent must know: shoot invocation, scenario names,
   instrument traps, class collisions with the copied stylesheet, layout
   traps that cost a cycle.

## Instrument requirements

Inherit the project's screenshot instrument if one exists; otherwise the
first round builds one and later rounds inherit it, each leaving it cheaper.
It must:

- Drive the browser over its devtools protocol with a device-metrics
  override and ASSERT the resulting viewport width and height, refusing to
  save otherwise. Command-line window sizing silently clamps on some
  platforms and crops the PNG.
- Ship the viewport meta the product ships; mobile emulation without it lays
  out at desktop width.
- Emulate each colour scheme through media emulation, no CSS fork.
- Report per shot: elements past the right edge or the fold, tap targets
  under the product's minimum, text spilling its box (scroll width over
  client width, separated from deliberate ellipsis), and for scrolled content
  counts and scroll position measured against the scroller, not the viewport.
- Size every fixed track against the widest legal value in the vocabulary,
  not the scenario's value: an over-long right-aligned line start-aligns and
  silently invades the column to its left without tripping any probe.
- Use classic scripts under file:// (modules are blocked), a unique browser
  profile per round (a locked profile from an orphaned headless tree fails
  with an unrelated error), and kill the browser in a finally block.
- Artifacts the OS re-renders (icons, widgets, notifications) pass through
  the real system renderer before the verdict.

Believe the instrument over the CSS: fix the instrument or the comp, never
silence the probe.

## Craft rules

These go verbatim into the comp agent's brief.

- **Borrow, don't invent.** Inventory the product's visual grammar (type
  scale, letter-spacing, label and row idioms, how it already handles the
  thing being designed) and build every concept from house parts; a new
  screen is an existing idiom promoted. With no language to borrow,
  establishing one exemplar IS the exploration.
- **Measure before a concept depends on a perceptual property**: items above
  the fold per frame, every colour against every ground in every scheme, the
  widest string against its track, geometric truth of anything claiming to be
  to scale; for imagery, edge luminance and crop floors. Numbers kill weak
  concepts early and honestly.
- **Photograph the stress case.** A comp that survives its worst content is a
  design; one that survives its best is a mockup.
- **Argue each choice from the material in one recorded line**: which data
  set, which crop, which frame proves the complaint. Say when a device carries
  no information the existing marks do not.
- **Subtraction is the default.** Each pass leaves less chrome, fewer
  devices, emptier edges. Editorial type: one measure, one scale ladder,
  letterspaced small-caps labels, no centred blocks. A label that explains a
  gesture is a design admitting it failed.
- **Copy is a material.** Real verbs in the product's voice, real values,
  lines mined from the project's own docs.
- **UI over imagery is a photography problem.** Type in the image's quiet
  third, respecting gaze and eye-line, darkness extended with gradients.
  Never a scrim box or blur panel. Ask for art changes as in-camera
  direction; name derivative-looking generated art for reroll.

## Operating rules

- Relay owner steers to a running comp agent immediately, binding over the
  brief where they differ, with what-this-changes spelled out.
- Fold every ruling into the design doc the moment it lands; later briefs
  cite the doc, never the chat.
- A round's brief carries the exemplar image, numbered spec, frozen list,
  frames, schemes and scenarios, the instrument to inherit, and the previous
  round's "what the next agent must know".
