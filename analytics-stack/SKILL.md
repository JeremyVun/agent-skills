---
name: analytics-stack
description: Onboard a project onto the shared self-hosted analytics service (multi-tenant Go service in ~/projects/analytics). Use when adding analytics/telemetry/event tracking to any project stack, wiring a client to the analytics service, choosing event names/dimensions, or debugging why events aren't showing up in /stats or the /ui dashboard.
---

# Onboarding a project onto the shared analytics service

One deployment of the `analytics` service (source: `~/projects/analytics`) serves every
project. Clients POST small JSON events to `/e`; the service keeps live per-project
stats in memory, flushes one aggregate row per project per hour to Postgres, and serves
a generic dashboard at `/ui`. There are no product concepts baked in — you compose
events from generic primitives. Full wire contract: `~/projects/analytics/README.md`
(trust it over this skill if they disagree).

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
- ❌ Per-user profiles, retention cohorts, A/B stats — out of scope; compose dims or
  query the raw archive.
