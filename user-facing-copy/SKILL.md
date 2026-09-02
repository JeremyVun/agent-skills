---
name: user-facing-copy
description: Rules for any text a user reads in a product: UI labels, buttons, error messages, empty states, onboarding, notifications, marketing, game narration. Use before drafting or reviewing copy, and when an owner says copy reads awkward, robotic, corny, confusing, or full of made-up words.
---

# Writing user-facing copy

Three golden rules. They outrank any project style guide. A project voice
(formal, playful, archaic) operates inside them, never instead of them.

1. **One pass.** The reader understands every sentence the first time. If a
   human has to read a sentence twice, the copy has failed. Length is the
   cheap resource; re-reading is the expensive one.
2. **Plain, never corny.** No epigrams, aphorisms, trailer lines, fortune
   cookies or ceremony. At most one quiet turn of phrase per passage, and
   only if it survives being read aloud.
3. **Call things what they are.** Use the ordinary word for the thing. Never
   coin a word, rename a familiar concept, or add a flavour noun that makes
   the reader learn a new idea. One thing, one name, used the same way
   everywhere.

## Why model copy fails

Model drafting treats each sentence as a payload of facts, then decorates
it. Its two reflexes are compression (welding several ideas into one
sentence with structural joints) and invention (dressing a plain thing in a
coined word). A human writes a speaker: a person saying sentences aloud, one
idea landing at a time, in words everyone already knows.

## Rule three in practice: no invented words

The tell is a noun the reader has never seen doing the job of a noun they
have. "Watchword" for a password field. "The register" for a name list.
"That name stands too near a power the register already knows" for "That
name is taken." Each one makes the reader build a concept before they can
act.

- **Product and UI copy** uses the industry-standard word: Password, Sign
  in, Save, Delete, Settings, Search, Name is taken. If a competitor's
  product would use the plain word, so do we.
- **Narrative copy** may have world vocabulary, but every coined term is
  introduced once, defined in its own plain sentence, and then used
  consistently. A term not worth a sentence of definition is not worth
  coining. Use the plain word.
- **The cover test.** Cover the unusual word and ask what the plain word is.
  If a plain word exists and the unusual one adds only flavour, the plain
  word wins.
- **Consistency is part of the rule.** Never alternate between "workspace",
  "project" and "space" for the same thing, even for variety.

## Two registers

Functional copy is read mid-task. Narrative copy is read for its own sake.
Decide which you are writing before you write a word. Narration an owner
has already polished is not retroactively wrong when a functional string
nearby gets flagged; the split is by register, not by age.

### Functional copy

Labels, buttons, errors, refusals, empty states, tooltips, notifications,
onboarding steps.

- A label is the plain noun. A button is the plain verb.
- An error or refusal says what happened and what to do, in one or two
  short sentences, and nothing else. The tell of a bad one is a second
  sentence that is atmosphere.
- An empty state says what will appear here and how to make it appear.
- No developer vocabulary: shard, fixture, client, payload, null, instance.
- No "Oops", no exclamation marks, no apologising, no jokes.
- A heading never restates the content beneath it.
- Sentence case. Full stops on sentences, none on labels.

### Narrative copy

Game narration, story, lore, long-form marketing.

The named tics, with flagged examples and their fixes:

| tic | flagged | fix |
|---|---|---|
| Parallel-snap aphorism | "The garden was real. The welcome was nine centuries of silence." | "No message ever reached the fleet. We found out when we landed." |
| Abstracted referent | "the power that sent it had put out the lights behind it" | "The Empire abandoned the frontier, and everyone in it, including us." |
| Portentous epigram | "How it ends… is not yet written." | "No one knows how this age will end." |
| Fragment stack | "garden-class, reserved, awaiting settlement" | "It describes an empty garden, waiting for settlers." |
| Constructed intimacy | "our grandmothers boarded ships" | "We came here nine hundred years ago, on colony ships the Empire built." |

**Sentence shape is the deepest tic.** With every surface tic fixed, an
owner could still tell a machine wrote it from the grammar alone. The
machine sentence welds two or three ideas together with joints: a
colon-appositive, a dash bolt-on, a participial tail, a payoff clause
welded to the end. Each joint is another thing the reader holds open.

The overcorrection is a tic too. Chopping everything into short sentences
reads "like a series of bullet points that don't tie together". Uniform
staccato is as machine-shaped as uniform welding. The target is rhythm and
cohesion:

- Vary sentence length on purpose. A long sentence that unspools, then a
  short one that lands. The short one gets its power from the long one.
- Sentences hold hands. Each picks up a thread from the last: a pronoun, an
  echoed word, a connective ("But", "So", "And then"). A paragraph of true
  but disconnected statements is a bullet list in disguise.
- Subordination and dashes are seasoning, not banned. "When the Empire
  pulled back, it left them at their posts" is how people talk. The tic is
  three joints in one sentence, not one.
- Rhythm is characterisation. A soldier speaks in drill cadence, a diplomat
  flows, an archivist defines terms. Choose the speaker's rhythm, then vary
  within it.

The same beat in three drafts:

> welded: "The Empire left before anyone could judge the results. …Nine
> hundred years later, it is still running, and it worked."
>
> staccato: "Then the Empire left. It never came back to see how the
> experiment turned out. But the experiment did not stop. It worked."
>
> written: "Then the Empire left, and never came back to learn how its
> experiment had ended. But the experiment had not ended, and it has not
> ended yet. Nine hundred years later, it is still running. It worked."

## Mechanics

- **Grammar.** Complete sentences with a subject and a verb. Fragments only
  in labels and headings. Named subjects, not pronouns doing a name's work.
- **Punctuation.** Full stops and commas do nearly all the work. One dash
  or colon per sentence at most, and rarely. No semicolons in product copy.
  No ellipses. No exclamation marks in functional copy, almost none in
  narrative.
- **Paragraphs.** One idea per paragraph. A new idea starts a new
  paragraph. A one-sentence paragraph is for emphasis, at most once per
  passage. Functional copy is usually one paragraph or none.
- **Teaching facts.** Each new noun gets its own sentence that defines it
  before anything depends on it.

## Process

1. Decide the register, then the speaker: a historian, a settler, an
   instrument, the product. Draft as that person talking, not as a spec
   being covered.
2. Read every line aloud, literally. If it sounds like a trailer, an
   epigram, or something no person would say, rewrite it plainly. If you
   stumble, the reader will too.
3. Run the cover test on every unusual noun.
4. Never compress to fix length. Cut whole sentences or beats. Squeezing
   words out of sentences reintroduces every tic above. Richness first,
   structural cuts after.
5. Check the project's copy guards before shipping. Projects may enforce
   banned-word tests, often by substring, so grep the actual list against
   the draft rather than trusting memory of it.

## Review checklist

Run on every line before shipping.

- Understood on the first read?
- Every noun is the plain standard word, or a defined term used the same
  way everywhere?
- No sentence carries more than one joint?
- Sentence lengths vary, and each sentence connects to the last?
- Functional copy says what happened and what to do, and nothing else?
- No epigram, trailer line or fortune cookie, and at most one quiet phrase
  in the passage?
- Would a person say this out loud?

## Log

Append dated learnings. Promote one into the sections above once it has
bitten twice.

- 2026-08-22: founding rules from an owner verdict on game narration
  (rules one and two, the tics table).
- 2026-08-22: surface fixes were not enough; sentence architecture alone
  gave the machine away. Then the one-idea-per-sentence fix overcorrected
  into staccato. Both promoted to "Sentence shape".
- 2026-08-28: functional strings in a strong world voice failed ("Watchword"
  for a password field, an atmospheric refusal). Promoted to the register
  split.
- 2026-09-02: owner named invented flavour words as a recurring failure:
  new nouns that introduce concepts instead of naming the thing plainly.
  Promoted to golden rule three and the cover test.
