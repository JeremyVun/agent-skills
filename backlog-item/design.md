# Design stage

Goal: a `design.md` and phased `build_plan.md` that a fresh build context can
execute without asking anything. The work is contextual; these are lenses to
apply and report on, not a script. Some items need one lens for an hour,
others need all of them.

## Open

Read the whole folder, the contracts it touches, and the code it claims to
build on. Then summarise the feature back to the owner in plain language:
what it is, why it exists, what it changes for the player or user. This
summary is the first alignment check; if it is wrong, nothing after it holds.

## Lenses

- **Should it exist?** Challenge the premise before the mechanism. Is there
  a cheaper mechanic, an existing seam that already does most of it, or a
  reason the feature is not worth its complexity? Deleting is a valid
  outcome; say so if it is the better one.
- **Verify the core claims.** Every "the code already does X" and "the
  contract guarantees Y" in the doc gets checked against the as-built code
  and contracts. A design built on a stale reading of the repo fails in the
  build stage where it is most expensive.
- **Simplify.** Each mechanism earns its place. Look for two things that
  could be one, a state that could be derived, a flag that could be a fact.
- **Edge cases and unknown unknowns.** Concurrency, ordering, empty and
  saturated states, what happens when the owner's numbers hit their bounds,
  what an adversarial user does. Name what the doc cannot yet know and what
  would settle it.
- **Consistency.** Contradictions between sections, between the doc and the
  contracts, between the design and the plan.
- **UI work.** If a screen's look is open, run the `design-comps` skill
  before any plan is written; a comp verdict is a design input, not a build
  step. Verify inherited visual premises empirically rather than in prose.
- **Copy.** Anything a user reads follows the `user-facing-copy` skill.

Offer the `debate` skill once the design is stable; it finds a different
class of defect from the owner's own reading.

## Align continuously

Every real decision goes to the owner as a question with the options laid
out, a recommendation, and the mechanism explained from zero: what the
machinery is and whether it earns its keep, as if to a friend who has not
read the doc. Do not batch a session's worth of decisions into one wall;
ask at the point the decision blocks the next thought. Fold each answer
into the doc before moving on. The owner's free-text note on an answer is
itself the ruling; record it verbatim.

Practices that have each cost a round when skipped:

- **No repo jargon in a question.** Any internal term the question leans on
  is defined in plain words in the same message, including the project's own
  generator and fairness internals; the owner does not carry them in his
  head even when he once ruled on them.
- **Pictures go on his screen.** An image read into the conversation is
  invisible to him. For any visual verdict, build one curated sheet (shots,
  captions, numbers, honest counterarguments, the questions inline) and open
  it on his display before asking.
- **Photograph before claiming.** Before asserting what a route or framing
  shows, shoot that exact route at his framing and look. A header or doc is
  a hypothesis until a shot confirms it; a confident wrong claim about what
  he can see reads as a lie.
- **"Feel like X" means X's form.** A named referent (a council chamber, a
  real place) is a statement about spatial composition and affordances, not
  mood. Confirm with reference images before running a round on it.
- **Close calls become two arms, not an argument.** When two treatments of
  one design are both defensible, build both behind a flag with a deadline
  and hand him the two commands; the loser's code is deleted when he picks.
  This never licenses building two different concepts.
- **Dials carry his names, anchors and zero-cases.** He validates a
  parameterisation by its degenerate cases. An equivalent-looking mechanism
  with different anchors fails those tests even when one setting matches.
  Ask before substituting a "better" model.
- **Scale calls: derive the ladder, he picks the rung.** Show the arithmetic
  and the physical thresholds at each size; expect the bolder pick and never
  pre-choose the restrained option. A timid derivation usually means the
  wrong anchoring constraint. Build the pick as a one-line knob so the
  dial-back he asks for later is cheap.
- **A bare tool run produces everything.** Before adding a mode flag, ask
  whether the bare invocation can emit the new artifact as well; flags only
  narrow.

## Write the plan

Phase along natural seams. For each phase record owned files, the seam
contract, the verify gate, and a done marker. Keep code waves and
verification waves separate: verification, not code, blows agent budgets.
Global passes (renames, copy sweeps) go first, before any parallel work
forks. Put the constraining arithmetic behind any owner number in the plan
so a builder can check its own work against it.

## Exit

State plainly whether the item is ready to build, and if not, what is still
open and who owns the answer. Remind the owner that the build stage starts
in a fresh context.
