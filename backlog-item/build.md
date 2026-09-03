# Build stage

Start by reading the folder and the contracts it cites, then summarise the
feature to be built back to the owner in plain language before touching
anything. The doc is the spec; if it is silent or contradictory on something
the build needs, ask the owner and fold the answer into the doc first.

Orchestrate to completion: every phase built, verified, and marked done in
`build_plan.md`. Then offer the `close-backlog-item` skill.

## Subagents

- Only spawn a subagent when the work genuinely splits into isolated pieces,
  and give each one a real scope, not a fragment.
- Every subagent is Opus 5, passed explicitly; never rely on the default.
  Never use Haiku or Sonnet.
- Effort is high by default. Use xhigh for open-ended debugging,
  multi-constraint design, or anything where a wrong first pass means a
  rerun; use high for well-specified implementation with a written contract
  and a verify loop.
- FABLE 5 SUB AGENTS ARE FORBIDDEN UNLESS THE OWNER HAS EXPLICITLY GRANTED
  PERMISSION. Standing exception: one Fable 5 adversarial reviewer between
  the build and fix waves where approval is granted.
  - It attacks the round's named invariants in its own worktree and flags
    contract contradictions for an owner RULING rather than fixing them.
  - The Fable account limit kills agents mid-round (429, no warning), so
    reviewers commit probe tests as soon as they compile.
  - The fix agent inherits those probes as its acceptance suite and keeps
    them as permanent regressions, with at least one real-stack (wire/DB)
    probe per defect; hand-composed unit probes can model propagation the
    code doesn't have.
  - Opus 5 xhigh is the fallback when Fable is cut off, briefed with which
    probes passed, which are real defects and which failed on their own
    fixture.
- Every subagent brief carries the owner's comment rule verbatim: comments
  are rare and short, one line of *why* where the reason is non-obvious,
  never narrating what the code does. Opus 5 defaults to verbose comments
  and cleaning them up costs a second pass.

## Sizing and sequencing briefs

- No agent may approach the ~650k context ceiling. Landing at 90% is a
  planning failure even if the work is good. Split a full phase along its
  natural seam (build/sim agent, then client/verification agent), each
  committing green.
- Verification, not code, blows budgets. Split code waves from verification
  waves. Visual builds get code + unit verify + at most one smoke drive; the
  empirical loop goes wholesale to the following verification wave (the two
  find different defects). A calibration exemplar does not shrink the
  look-loop budget.
- Global passes (copy sweeps, renames) run on main BEFORE worktrees fork.
  Run late, they collide with everyone.
- Base each dependent phase's worktree on the previous phase's branch, not
  main, and land the stack as one merge. Sequenced merges beat one big
  integration. Budget an integration agent when a contract changes under
  parallel work.
- File- or directory-disjoint ownership gives zero merge conflicts. What
  remains is interaction semantics, so briefs carry behavioural contracts
  (input semantics, event ordering, timing handoffs) alongside file
  ownership.
- When a screen's design is open, that is design-stage work: stop and run
  the `design-comps` skill before any build.

## Briefing content

- Symptom over hypothesis: the measured symptom is the binding spec, any
  named seam is a hypothesis. Orchestrator effort before briefing (defect
  surface read, artifact generated, exact line anchors, owner quotes near
  verbatim) gets agents landing first pass.
- Relayed owner rulings include the mechanism, the constraints it must
  satisfy, and explicit permission to stop and report if the mechanism
  proves impossible. Numbers the owner edits in an answer are the binding
  spec; put the constraining arithmetic in the brief.
- "Keep the artifact, tweak A and B" is a PORT: same algorithm, same output,
  only the named tweaks. When a misread ships, amend the design doc
  immediately; two agents making the same mistake means fix the doc, not
  the next prompt. Don't redirect an agent deep in its budget onto a
  different spec; stop it and start fresh.
- Fold mid-round owner answers into the design doc immediately so later
  briefs cite the doc, never the chat. Every agent report ends with "what
  the next agent must know" and is a complete handoff (metrics, decisions,
  rejected alternatives, hazards). Chain it into the next brief.
- Creative/visual briefs: over-specification causes convergent mediocrity.
  One sentence of intent per claim, a calibration exemplar compared side by
  side each iteration, an objective probe offered as a mirror not a gate,
  explicit creative latitude. Verify inherited visual premises empirically.
  The first visual agent builds the screenshot instrument as a repo tool
  with its traps documented.

## Agent lifecycle

- Mid-flight steers to running agents are the cheapest correction. Relay
  owner feedback, peer warnings and the first finisher's report (tooling
  found, instrument traps) the moment they arrive.
- Resuming a finished agent is opportunistic, never planned around;
  transcripts get lost. NEVER resume an agent that stopped because its
  context filled. Check subagent tokens (~650k = full) before choosing
  resume vs fresh.
- Agents killed by API limits resume via transcript with "git status,
  reclaim ports/stack, continue at <last intent>". If the transcript is
  gone, the disk is the transcript: a salvage agent restates the original
  spec verbatim, surveys git status and reads every relevant file before
  editing, runs baseline suites first so inherited failures stay
  attributable, and rebuilds only genuine gaps.

## Verification discipline

- Verify the harness before believing a red. Rerun once with the tool's own
  documented invocation before spawning a fix agent. Stale lint caches and
  pruned worktrees produce convincing false reds.
- A verify loop is only as good as its instrument. Confirm it can display
  the failure class being risked, require one shot from the real client per
  defect, and fix the instrument rather than the next prompt's vigilance.
- Live-probe verification ranks equal with tests; the worst bugs are
  invisible to green suites. Prove each new regression test bites by
  temporarily breaking the guard. Behaviour-preserving splits need verbatim
  moves plus a line-multiset diff. A race-detector gate is a deliverable
  whenever concurrency boundaries move.
- Report outcomes faithfully to the owner: failing gates with their output,
  skipped steps named as skipped, done only when verified.
