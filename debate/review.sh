#!/usr/bin/env bash
# Usage: review.sh <doc> <round> [prior-verdicts-file]
# Runs one adversarial review of <doc> with Codex and prints the findings.
set -euo pipefail

doc="$1"
round="$2"
prior="${3:-}"
model="${DEBATE_MODEL:-gpt-5.6-sol}"

[ -f "$doc" ] || { echo "no such doc: $doc" >&2; exit 2; }
doc_abs="$(cd "$(dirname "$doc")" && pwd)/$(basename "$doc")"
repo="$(git -C "$(dirname "$doc_abs")" rev-parse --show-toplevel 2>/dev/null || dirname "$doc_abs")"
out="$(mktemp -t debate-r${round}.XXXXXX)"

prior_block=""
if [ -n "$prior" ] && [ -s "$prior" ]; then
  prior_block="
## Prior rounds
These findings were already raised. Do not repeat them or relitigate a REJECTED verdict unless you have new evidence the reason given is wrong.

$(cat "$prior")
"
fi

prompt="You are an adversarial reviewer. Round $round. Your job is to find real defects in the document at:
$doc_abs

Read the document and inspect the repository around it (read-only) to check its claims: referenced files, functions, contracts, data shapes, numbers and sequencing. Attack it as a design or build plan: contradictions, unstated assumptions, missing failure modes, ordering and concurrency hazards, claims the code does not support, scope that cannot be built as written, ambiguities that two implementers would resolve differently.
$prior_block
## Output format
Return only findings, nothing else. If you have none, return exactly:
NO FINDINGS

Otherwise, one finding per block:

### F<n>: <one-line claim>
Severity: HIGH | MEDIUM | LOW
Anchor: <short verbatim quote from the document>
Evidence: <what in the repo or the document itself supports the claim; cite paths>
Fix: <the smallest change that resolves it, or the question the owner must answer>

Severity guide. HIGH: the item cannot be built or would be built wrong. MEDIUM: an implementer would likely make a mistake or need to ask. LOW: polish, wording, or a nice-to-have.
Do not pad. Style, formatting and tone are not findings unless they cause ambiguity. Do not restate the document."

codex exec -C "$repo" -m "$model" -s read-only --skip-git-repo-check --ephemeral \
  -o "$out" "$prompt" >/dev/null 2>"$out.err" || { cat "$out.err" >&2; exit 1; }

cat "$out"
echo
echo "[review output: $out]"
