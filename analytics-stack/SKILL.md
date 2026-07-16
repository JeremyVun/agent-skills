---
name: analytics-stack
description: Onboard a project onto the shared self-hosted analytics service (multi-tenant Go service in ~/projects/analytics). Use when adding analytics, telemetry, event tracking, or durable user-feedback submission to a project; wiring a client; choosing events/dimensions; or debugging missing events or feedback in the API or /ui dashboard.
---

# Onboarding a project onto the shared analytics service

One deployment of the `analytics` service (source: `~/projects/analytics`) serves every
project. Clients POST small JSON events to `/e`; the service keeps live per-project
stats in memory, flushes one aggregate row per project per hour to Postgres, optionally
archives raw events, and serves a generic dashboard at `/ui`. Durable freeform feedback
uses the separate `/feedback` contract described below. Full wire contract:
`~/projects/analytics/README.md` (trust it over this skill if they disagree).

**Do not** build a per-project Loki/Promtail pipeline, a bespoke events table, or any
other analytics backend for a project — this service is the standard path.

## Step 0 — facts to collect before wiring anything

1. **Service URL.** Ask the user for the deployed analytics endpoint (it is not in the
   project repos). For local dev: `docker compose up` in `~/projects/analytics` serves
   `http://localhost:8789`.
2. **Project key** (`p`): short kebab-case, ≤64 chars, stable forever — e.g. `steeple`.
   It partitions all data; changing it later orphans history.
3. **Ingest key.** The server may require `X-Analytics-Key`. Per-project keys are
   configured server-side via `ANALYTICS_INGEST_KEYS="project:key,..."` (deny-by-default
   once set — an unregistered project's events are silently dropped). Registering a new
   project = the operator adds `yourproject:yourkey` to the deployment env and restarts.
   Ask the user to do this (or note it as a deploy prerequisite); generate the key with
   `openssl rand -hex 24`. A browser-shipped key is a bot-hurdle, not a secret.

## Step 1 — wire a client

The contract is plain HTTP + JSON; anything that can POST can emit.

**Browser / TypeScript:** copy `~/projects/analytics/client/analytics.ts` into the
project (it is dependency-free, batches, heartbeats, never throws). Construct once:

```ts
const analytics = new Analytics({
  endpoint: ANALYTICS_URL, project: 'myproject',
  unit: pseudonymousUserId, session: pageLoadId, ingestKey: KEY,
})
analytics.startHeartbeat()
analytics.count('search_performed', { d: { zero: 'true' } })
```

**Server-side (any language):** POST an array of events to `/e` with header
`X-Analytics-Key` when required. Fire-and-forget with a short timeout:

```csharp
// C# sketch — swallow all failures; analytics must never break a request path
await http.PostAsJsonAsync($"{url}/e",
  new[] { new { p = "myproject", t = "search_performed",
                d = new { zero = "true", results = "0" }, sid = sessionId } }, ct);
```

Non-negotiable rules for any client you write:
- **Never block or throw on the app's request path.** Queue/batch, catch everything.
- Batch where possible (≤500 events/request, ≤64 KiB body).
- `204` = all accepted; `200 {recorded, dropped}` = partial (dropped = malformed,
  over-cap, or wrong tenant key); `401` = your key matches nothing; `429` = rate limited
  (default 240 req/10s/IP — batch harder).

## Step 2 — model the events

One event object; only `p` is required. Primitives:

| field | primitive | effect |
|---|---|---|
| `t` | counter | `counters[t] += n` (n defaults to 1) |
| `t` + `d` | histogram | `histograms[t][dim][value] += n` — categorical counts |
| `u` + `st` | gauge | live presence: online total + per-state buckets |
| `u` | unique | distinct units per window |
| `k` | dedup | that event's count applied at most once per TTL (6h default) |
| `sid`, `ts` | — | carried, not aggregated — kept in the raw event archive (queryable in SQL via DuckDB) |

Modelling rules that trip people up:

- **Numeric values must be bucketed client-side** (`d: {results: "0"|"1-5"|"6-20"|"20+"}`)
  — `n` is a count increment, not a value; there is no avg/percentile primitive.
- **Joint questions on the live dashboard/aggregates need composite dims composed at
  emit time** (`d: {"outcome.difficulty": "kill.heroic"}`) — histograms are
  per-dimension, independent, and can't be joined at read time there; post-hoc joint
  questions can instead be answered from the raw archive with DuckDB SQL.
- **Funnels** = one counter per step + shared dims; ratios computed at read time.
- **Presence**: send a beat (`u` + `st`, no `t`) every ~30s; units auto-expire after
  ~75s silence. The TS client's `startHeartbeat()` does this.
- **Naming**: event types `snake_case`, past tense (`search_performed`,
  `listing_viewed`); dims short lowercase. Stay under the caps: ≤256 distinct
  counter/dim keys per project (overflow folds into `"other"`), ≤16 dims/event,
  values ≤64 chars.
- **Aggregation is by arrival time**, not `ts` — offline/late batches land in the
  current hour.
- **PII: never.** No names, emails, phones, addresses, gov IDs, or raw IPs in any
  field. `u` must be a pseudonymous id. High-cardinality ids (listing slugs etc.) are
  allowed but will fold into `"other"` past 256 distinct values.

Record the project's event taxonomy in the project's own docs (e.g. a CONTRACTS.md
table: event, source, dims) — the analytics service is generic and won't remember it
for you.

## Step 3 — project-side configuration conventions

Add to the consuming project's config (names by that project's own conventions):

- analytics base URL (e.g. `Analytics:BaseUrl` / `ANALYTICS_URL`)
- project key (or hardcode it — it never changes)
- ingest key, from secrets/env, never committed

Unset URL ⇒ the client no-ops. Analytics must be safe to run without.

## Step 4 — verify end-to-end

```bash
# 1. Send a test event (add -H "X-Analytics-Key: $KEY" if required):
curl -sS -X POST "$URL/e" -d '{"p":"myproject","t":"onboard_test","u":"smoke-1"}'
# expect: 204 (or {"recorded":1,"dropped":0})

# 2. Read it back live:
curl -sS "$URL/stats?project=myproject"   # counters.onboard_test == 1, online == 1
# add the read key if the deployment sets ANALYTICS_READ_KEY (header X-Analytics-Key or ?key=)

# 3. Dashboard: open $URL/ui (append ?key=… once if read-gated; it sets a cookie).
```

If the event doesn't appear: `401` → key matches nothing configured; a `200` with
`dropped:1` → wrong project's key (deny-by-default) or malformed event; nothing at
all → check the project key spelling (unknown projects return a well-formed zero
payload on `/stats`, which masks typos).

Then verify from the real app flow, not just curl.

## Durable feedback — separate workflow

Use `POST /feedback` only for user-authored freeform feedback. Never put feedback text,
category text, or other personal data into `/e` or the raw archive. The feedback route
stores individual records synchronously in Postgres so operators can review, export,
and delete them.

Before wiring a product, collect the service URL, the same stable kebab-case project
key, and its dedicated feedback submission key. The operator must:

- enable `ANALYTICS_FEEDBACK=1` with both `DATABASE_URL` and
  `ANALYTICS_READ_KEY` configured;
- register a per-project key in `ANALYTICS_FEEDBACK_KEYS="project:key,..."` (preferred
  for product apps) or configure the master `ANALYTICS_FEEDBACK_KEY` for a trusted
  server-side caller; and
- restart the service after deployment configuration changes.

Submission is always deny-by-default. Feedback keys are independent from ingest and
read keys, and a browser-shipped project key is only a bot hurdle. The server also
applies a separate limit of 5 submission attempts per 10 minutes per IP by default.

Submit the long-form JSON contract and wait for the result:

```ts
async function submitFeedback(category: string, feedback: string, rating?: number) {
  const response = await fetch(`${ANALYTICS_URL}/feedback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Feedback-Key': FEEDBACK_KEY,
    },
    body: JSON.stringify({ project: 'myproject', category, feedback, rating }),
  })
  if (!response.ok) throw new Error(`feedback failed: ${response.status}`)
  return response.json() as Promise<{ id: string; receivedAt: string }>
}
```

Clear the form only after `201 Created`; on every failure retain its contents and show
a retry action. A `201` means the complete row committed. Handle `400` as invalid input,
`401` as an unknown key, `403` as a key for another project, `413` as a body over 10
KiB, `429` using `Retry-After`, and `503` as unavailable Postgres. A disabled route
returns `404`. Retries can create duplicates if the insert committed but the response
was lost.

Contract limits are 128 UTF-8 bytes for `category` and 8 KiB for `feedback`, both
required after trimming. `rating` is optional; when present it must be an integer from
1 to 5. Do not add identity, email, IP, User-Agent, referrer, cookies, or browser
metadata. Never log bodies or feedback values. A separate content-free
`feedback_submitted` analytics counter may be emitted only after `201`.

Verify with synthetic, non-personal text:

```bash
curl -i -X POST "$URL/feedback" \
  -H "Content-Type: application/json" \
  -H "X-Feedback-Key: $FEEDBACK_KEY" \
  -d '{"project":"myproject","category":"smoke-test","feedback":"feedback route verification"}'
# expect HTTP 201 with id + receivedAt
```

Then confirm the record in `/ui` using the read key. Operators can also use
`GET /feedback?project=myproject`, `/feedback/download?project=myproject&format=csv`,
and project-scoped `DELETE /feedback/{id}?project=myproject`. Product clients must not
receive the read key or deletion capability. V1 has no automatic retention; manual
deletion does not erase database backups or prior exports. Full privacy and operator
contract: `~/projects/analytics/docs/FEEDBACK_SPEC.md`.

## What the service does and doesn't give you

- ✅ Live gauges + window aggregates (`/stats`), hourly time series (`/series`,
  Postgres), generic dashboard (`/ui`).
- ✅ Contract is additive-only; unknown JSON fields ignored — old clients keep working.
- ✅ Raw event storage: every recorded event is also archived as gzipped NDJSON to an
  S3-compatible bucket (DigitalOcean Spaces) when the deployment sets the
  `ANALYTICS_ARCHIVE_*` env vars (off by default), under keys
  `raw/p=<project>/dt=YYYY-MM-DD/<HHMMSS>-<rand>.ndjson.gz`. `sid`/`ts` are kept, so
  session funnels and post-hoc breakdowns are possible with DuckDB
  (`read_json_auto('s3://<bucket>/raw/p=<project>/dt=*/*.ndjson.gz')`). Design record
  and query recipes: `~/projects/analytics/docs/ARCHIVE_SPEC.md`. Best-effort — the
  hourly aggregates remain the durable totals — and dedup is NOT applied to the raw
  stream.
- ✅ Durable user feedback: synchronous project-scoped Postgres records, protected
  operator reads/downloads/deletion, and a dashboard Feedback view. This is separate
  from analytics events and requires explicit server-side enablement.
- ❌ Per-user profiles, retention cohorts, A/B stats — out of scope; compose dims or
  query the raw archive.
