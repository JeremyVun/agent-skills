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
into the doc before moving on.

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
