# Design stage

The goal is a design the owner has agreed to and a fresh context can build
from without asking anything. The work is critical thinking, not paperwork:
an item may leave this stage smaller, different, or cancelled.

## Posture

- Read the whole folder, the contracts it touches and the code it claims to
  build on. Then say back to the owner, in plain language, what the feature
  is and why it exists. If that is wrong, nothing after it holds.
- Question the premise before the mechanism. Is there a simpler shape, an
  existing seam that already does most of it, a reason not to build it at
  all? Not building is a valid outcome; say so when it is the better one.
- Verify every claim the doc makes about existing code and contracts against
  the code and contracts. A design built on a stale reading fails in the
  build, where it is most expensive.
- Look for what the doc cannot yet know: edge cases, ordering, empty and
  saturated states, what would settle each unknown.
- Align continuously. A real decision goes to the owner at the moment it
  blocks the next thought, with the options, a recommendation, and the
  machinery explained from zero. Fold the answer into the doc before moving
  on; a free-text note in an answer is the ruling, verbatim.

## Where the other skills apply

- A screen whose look is open: `design-comps` before any plan is written. A
  comp verdict is a design input, not a build step.
- Text a user will read: `user-facing-copy`.
- A design that has stabilised: offer `debate`. It finds a different class
  of defect from the owner's own reading.

## Outputs

`design.md` is self-contained: what and why, the mechanism precisely enough
to build from, decisions with the owner's rulings and their dates, rejected
alternatives with the reason, no open questions standing.

`build_plan.md` is phased along the work's natural seams. Each phase names
the files it owns, the contract at its seams, its verify gate and a done
marker, and is sized so no agent nears its context ceiling. Verification is
its own wave; it costs more context than code.

## Exit

Say whether the item is ready to build and, if not, what is open and who
owns the answer. The build starts in a fresh context.
