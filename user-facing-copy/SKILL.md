---
name: user-facing-copy
description: "Rules for any text a user reads in a product: UI labels, buttons, error messages, empty states, onboarding, notifications, marketing, game narration. Use before drafting or reviewing copy, and when an owner says copy reads awkward, robotic, corny, confusing, or full of made-up words."
---

# Writing user-facing copy

Three golden rules. They outrank any project style guide. A project voice
(formal, playful, archaic) operates inside them, never instead of them.

1. **One pass.** The reader understands every sentence the first time. If a
   human has to read a sentence twice, the copy has failed. Length is the
   cheap resource; re-reading is the expensive one.
2. **Plain, never corny.** No epigrams, aphorisms, trailer lines, fortune
   cookies or ceremony. You need no turn of phrase at all. Keep one only
   if it arrived on its own and a person would say it aloud.
3. **Call things what they are.** Use the ordinary word for the thing.
   Never coin a word, rename a familiar concept, or add a flavour noun that
   makes the reader learn a new idea. One thing, one name, everywhere.

## Why model copy fails

A model treats each sentence as a payload of facts, then decorates it. Two
reflexes do the damage: compression, which welds several ideas into one
sentence, and invention, which dresses a plain thing in a coined word or a
grand abstraction. Both come from the same root: the model starts writing
before it has decided, in plain words, what the sentence is for.

A human writer decides the meaning first, then chooses a speaker, then lets
the facts ride inside that person's voice, one idea landing at a time.

## Before writing

**Know what you mean.** For every sentence you are about to write, you
should be able to state in one plain clause what it tells the reader. If
you cannot, the sentence has no job. Cut it. This single check removes
most abstraction, most epigrams and most invented words, because those are
what a writer produces when the meaning is vague.

**Know who is reading, and when.** Functional copy is read by someone in
the middle of doing something else, often after something went wrong.
Narrative copy is read by someone who chose to read. Decide which register
you are in before you write a word.

**Choose a speaker.** Draft as a person talking, not as a spec being
covered. For product copy the speaker is a calm, competent colleague at
the next desk who knows the product and respects the reader's time. For
narrative, the speaker is a character with a reason to be telling this,
and their rhythm is part of who they are.

## Words

- **The plain word wins.** Password, not Watchword. Name is taken, not
  "That name stands too near one the register already knows". Sign in,
  Save, Delete, Search, Settings. If another product would use the plain
  word, so do we.
- **The cover test.** Cover the unusual word and ask what the plain word
  is. If a plain word exists and the unusual one adds only flavour, use the
  plain word. If no plain word exists, the concept is new and needs a
  sentence of definition before it is used.
- **Coined terms are a cost.** A narrative world may have vocabulary of its
  own, but every coined term is a promise that it will matter. Introduce it
  once, define it in its own plain sentence, then use it unchanged. A term
  not worth a sentence of definition is not worth coining.
- **Consistency is part of the rule.** Never alternate between
  "workspace", "project" and "space" for the same thing. Variety in nouns
  is a bug, not style.
- **Filler words are never the plain word.** Seamless, robust, powerful,
  effortless, elevate, unlock, empower, leverage, journey, experience (as a
  noun for a feature), crafted, curated, bespoke, delve, and their
  relatives. Each one is a claim with no content. Say what the thing does.
- **Never invent a fact.** No made-up numbers, quotes, names or claims. If
  a fact is needed and unknown, leave a bracketed placeholder and say so.

## Functional copy

Labels, buttons, errors, refusals, empty states, tooltips, notifications,
onboarding, help.

- A label is the plain noun. A button is the plain verb for what it does.
- An error or refusal says what happened and what to do next, in one or
  two short sentences, and nothing else. The tell of a bad one is a second
  sentence that is atmosphere, apology or personality.
- An empty state says what will appear here and how to make it appear.
- Speak to the reader as "you". Use "we" only when people are genuinely
  behind the sentence. Contractions are normal ("can't", "didn't").
- Active voice, present tense. "Save" not "Saving will occur".
- No developer vocabulary: shard, fixture, client, payload, null, instance,
  session, token, unless the reader is a developer.
- No "Oops", no exclamation marks, no jokes, no apologising.
- A heading never restates the content beneath it.
- Match the product's existing conventions for case and punctuation. The
  default is sentence case, full stops on sentences, none on labels.
- World voice belongs in narration and events, never in a form label or a
  refusal. A player reads a label mid-task and needs the standard word.
- Short is not the same as done. Trimming a helper line to its load-bearing
  fact produces a patch note ("A level is recorded and confers nothing yet").
  The survivor of a cut must still carry the fact in the product's own voice.

## Narrative copy

Game narration, story, lore, long-form marketing.

**One idea per sentence is the default.** A second idea may join when a
connective states the relationship: because, when, but, so. Never a third.
The machine sentence welds ideas with structural joints instead: a
colon-appositive, a dash bolt-on, a participial tail, a payoff clause at
the end. Each joint is one more thing the reader holds open.

**Sentences hold hands.** Each picks up a thread from the last: a pronoun,
an echoed word, a connective. A paragraph of true but unconnected
statements is a bullet list in disguise, and reads as one.

**Vary length, but do not perform it.** A long sentence followed by a short
one is a device. Used once in a passage, the short sentence lands. Used at
the end of every paragraph, it is the loudest machine tell there is.
Uniform short sentences are as machine-shaped as uniform long ones. The
target is the rhythm of a person speaking, which is uneven and unforced.

**Rhythm is characterisation.** A soldier speaks in drill cadence, a
diplomat flows, an archivist defines terms. Choose the speaker's rhythm,
then vary within it.

**Name the subject.** Pronouns and abstractions ("the power that sent it")
doing a name's work force a re-read. Say who did what.

**Fragments belong in catalogues, not in speech.** A survey entry rendered
as a survey entry may be a list of fragments. The moment a sentence quotes
or narrates it, give it a subject and a verb.

**Paragraphs.** One idea per paragraph, and a new idea starts a new one. A
one-sentence paragraph is for emphasis, at most once per passage.

### The tics, with the meaning underneath

The fix for a tic is never a substitute phrase. It is to find the plain
statement the line was hiding and say that.

| tic | flagged line | what it meant | said plainly |
|---|---|---|---|
| Parallel-snap aphorism | "The garden was real. The welcome was nine centuries of silence." | The planet matched the survey. The Empire never contacted the colony again. | "The planet was everything the survey had promised. The Empire never spoke to us again. That was nine hundred years ago." |
| Abstracted referent | "the power that sent it had put out the lights behind it" | By the time the ship arrived, the Empire had withdrawn from the frontier. | "By the time the ship arrived, the Empire that sent it had already withdrawn from the frontier." |
| Portentous epigram | "How it ends… is not yet written." | Nothing. It exists to sound weighty. | Cut it. If the beat is needed, state the stake: "The colony could still fail." |
| Fragment stack | "garden-class, reserved, awaiting settlement" | The survey classed the planet habitable and reserved it for a colony not yet sent. | "The survey had listed the planet as habitable and set it aside for settlement. No one had been sent." |
| Constructed intimacy | "our grandmothers boarded ships" | Our ancestors came on colony ships. | "Nine hundred years ago, our ancestors boarded colony ships the Empire had built." |

### The same beat, three drafts

The first welds, the second chops, the third is written. Notice that the
third links its sentences by repeating "ended", varies its length without
a pattern, and earns its short last sentence with the long ones before it.

> welded: "The Empire left before anyone could judge the results. …Nine
> hundred years later, it is still running, and it worked."
>
> staccato: "Then the Empire left. It never came back to see how the
> experiment turned out. But the experiment did not stop. It worked."
>
> written: "Then the Empire left, and never came back to learn how its
> experiment had ended. But the experiment had not ended, and it has not
> ended yet. Nine hundred years later, it is still running. It worked."

## Punctuation

Full stops and commas do nearly all the work. A dash or a colon is
seasoning: at most one per sentence, and most sentences have none. No
semicolons in product copy. No ellipses. No exclamation marks in
functional copy, almost none in narrative. Quotation marks only for actual
quotations, never for distancing or irony.

## Process

1. Write the meaning list: each thing the copy must tell the reader, as a
   plain clause. If teaching facts, each new noun gets its own sentence
   that defines it before anything depends on it.
2. Decide the register and the speaker.
3. Draft as that speaker, in plain words, one idea at a time.
4. Read every line as if aloud. If it sounds like a trailer, an epigram, or
   something no person would say, rewrite it plainly. If you stumble, the
   reader will too.
5. Run the cover test on every unusual noun.
6. To shorten, cut whole sentences or beats. Never squeeze words out of
   sentences; that reintroduces every tic above. Richness first, structural
   cuts after.
7. Check the project's copy guards. Banned-word tests often match by
   substring, so grep the actual list against the draft.
8. Never fix a flagged tic by applying its inverse everywhere. Fix the
   line, then re-read the passage as a whole for monotony in either
   direction.

## Review checklist

Run on every line before shipping.

- Can I state in one plain clause what this sentence tells the reader?
- Would a reader understand it on the first pass?
- Is every noun the plain standard word, or a defined term used unchanged?
- Does the sentence carry at most one joint, and at most two ideas?
- Does it connect to the sentence before it?
- Functional copy: what happened and what to do, and nothing else?
- Is there any epigram, punch line, filler adjective or invented fact?
- Would a person say this out loud?

## Log

Append dated learnings. Promote one into the sections above once it has
bitten twice.

- 2026-08-22: founding rules from an owner verdict on game narration
  (rules one and two, the tics).
- 2026-08-22: surface fixes were not enough; sentence architecture alone
  gave the machine away. Then the one-idea-per-sentence fix overcorrected
  into staccato. Both promoted to the narrative section.
- 2026-08-28: functional strings in a strong world voice failed
  ("Watchword" for a password field, an atmospheric refusal). Promoted to
  the register split.
- 2026-09-02: owner named invented flavour words as a recurring failure:
  new nouns that introduce concepts instead of naming the thing. Promoted
  to golden rule three and the cover test. Same day, the first rewrite's
  tic fixes were rejected as context-free substitutions, two of which
  committed the tic they replaced. Promoted: a fix recovers the meaning
  underneath, never swaps in a new phrase.
- 2026-09-03: folded from project memory: the trimming trap (a cut that
  keeps the mechanic's half and drops the voice), and the owner's diagnosis
  that token-efficient copy reads as machine copy. Promoted to functional
  copy and already present in rule one.
