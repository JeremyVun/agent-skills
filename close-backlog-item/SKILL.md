---
name: close-backlog-item
description: Review or close completed ephemeral backlog folders by migrating durable contracts and assets, repairing references, cleaning item-specific worktrees, and deleting obsolete history. Use for closure audits or explicitly authorized close-and-delete tasks, not active work.
---

# Close Backlog Item

Backlog folders and their worktrees are disposable workspaces. A completed
item leaves current behavior in the product, its canonical contracts, and the
root `assets/` folder, not an archive folder. Git is the history.

## Respect the requested authority

- For a review or “can this close?” request, inspect and report the verdict;
  do not edit or delete.
- For an explicit close/delete request, perform the migration, reference
  repair, deletion, and verification.
- Do not infer permission to close sibling backlog items merely because they
  also look complete.
- Resolve the exact deletion target read-only before removing anything. Never
  use a broad directory, unresolved variable, or glob as a destructive target.

## Decide what survives

Move only information that changes future implementation decisions:

- public or cross-component contracts;
- storage, API, event-ordering, caching, lifecycle, and concurrency seams;
- current product invariants and owner decisions;
- performance or geometry budgets that remain acceptance criteria;
- operational rules that can otherwise cause a broken deploy or client;
- current assets still used by product documentation, tests, or calibration.

Fold these into the relevant existing file under `docs/contracts/` whenever
one exists. Create another contract only when it has a distinct durable owner;
do not duplicate the same rule across several documents.

Do not retain phase plans, completion reports, verification narratives,
rejected concepts, old screenshots, superseded decisions, defect stories,
dated ruling labels, or a condensed historical summary. Do not move them into
`docs/archive`, a renamed backlog folder, or comments. Git already preserves
them.

An asset survives only if it has a current role after closeout. Move surviving
images, video, audio, and other media to the repository's root `assets/`
folder and update every consumer. Preserve meaningful organization within
that folder rather than flattening unrelated assets together. Delete
exploration assets and evidence shots. If a durable contract can state the
rule without an asset, do not preserve the asset merely because it exists.

## Closeout workflow

1. Read repository instructions, inspect the current checkout, and inventory
   linked worktrees with `git worktree list --porcelain`. Existing changes
   belong to the user or another session; preserve them and re-read shared
   files immediately before editing.
2. Read the entire backlog item, current contracts, relevant implementation,
   and tests. Do not assume a checked-off plan matches current behavior.
3. Audit completion against shipped behavior and proportionate gates. If the
   item still owns genuine unfinished scope, stop deletion and report exactly
   what remains. Superseded scope is not unfinished scope.
4. Search outside the folder for its path, filenames, headings, exemplar
   names, copied source comments, and numbered or lettered registers such as
   “defect 3” or “ruling B”. Search the register identifiers as well as paths.
5. Build a migration map from each still-current rule to its canonical
   contract. Confirm the contract describes current code, not merely the old
   backlog design.
6. Update contracts and consumers first. Replace references to historical
   register labels with direct semantic references to the migrated rule.
   Correct adjacent stale documentation when deletion would expose it.
7. Repair every surviving consumer: README media, roadmap and agent docs,
   code provenance comments, calibration links, test comments, and tool output
   defaults. A generator or screenshot tool must not recreate the deleted
   backlog directory on its next run; default disposable output to the system
   temp directory unless it is a deliberate durable artifact.
8. Delete the exact backlog folder only after the migration and reference
   repair are present. Binary assets may require a filesystem deletion when a
   text patch tool cannot remove them; keep the target absolute and previously
   validated.

## Retire item worktrees

A closure audit reports item-related worktrees but does not alter them. An
explicit close request also authorizes cleanup of stale or inactive dirty
worktrees that are demonstrably attributable to that backlog item.

For every candidate, record its absolute path, branch, HEAD, status, untracked
files, and commits not reachable from the destination branch. "Merged" needs
four checks, not one: `git merge-base --is-ancestor` plus `git cherry` (re-landed
work shows as unmerged but is marked equivalent), a clean `status --porcelain`,
no `locked` flag in `git worktree list`, and `lsof -a -d cwd` showing no process
still running inside it; the last check has caught a live agent the other three
cleared. Establish the
connection from the branch, path, commits, or contents; a suggestive name alone
is not enough. Check for an active process or session before changing it.

Inspect all dirty and unique work before removal. Migrate and land anything
that remains current. Changes confirmed to be item-specific obsolete residue
may be discarded under the explicit close authority. If ownership is
uncertain, the worktree is active, or unique current work cannot safely be
landed, stop and report the exact blocker instead of force-removing it.

Remove only the resolved worktree path, with `git worktree remove`, never `rm -rf`
(which leaves stale admin entries). Use force only after the preceding
inspection proves every remaining change is obsolete and in scope. Delete an
associated local branch only when it is clearly item-specific and has no
current unmerged work. Preview stale administrative entries before pruning
them, and do not prune unrelated worktree state.

## Verification

At minimum:

- prove the target no longer exists;
- search the repository for the deleted path and every removed canonical-doc
  path or register name;
- prove each retired item worktree is absent from both disk and
  `git worktree list`, while unrelated worktrees retain their prior state;
- check the diff for whitespace errors and accidental edits to unrelated work;
- run the relevant unit and contract gates;
- syntax-check changed tools and smoke any changed default output path;
- check surviving local documentation/media links and all migrated
  `assets/` consumers that were in scope.

Use the repository's documented invocations. Do not load secrets merely to run
a closeout check; use non-network gates or an explicit harmless test value when
the application supports it.

Report what was removed, which worktrees and branches were retired, where the
durable rules and assets now live, verification results, and whether each
deletion is recoverable from version control. Mention unrelated dirty work
only when it affects handoff.
