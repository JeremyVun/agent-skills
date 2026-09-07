---
name: feature-flags
description: Put a project's feature flags on the shared flagsd service (~/projects/flags). Use when adding, changing or removing a feature flag, deciding public vs private, minting an SDK key, wiring the Go or .NET SDK, exposing flags to a browser/mobile client, or debugging why a flag evaluates the way it does.
---

# Feature flags on the shared flagsd service

One deployment serves every project. The admin UI at `https://flags.jeremyvun.com`
(Authelia SSO) is the only public piece; `flagsd` itself is internal-only and speaks
one generic JSON API. Source and normative spec: `~/projects/flags`, `docs/CONTRACT.md`
(trust it over this skill). **Do not** build a per-project flag service, a flags table,
or env-var "flags" for anything that should be toggled at runtime.

## The model in six lines

- **Project** (`perchd`, `steeple`, …) → **environments** (`production` by default) → **flags**.
- A **flag definition** is project-wide: `key`, `type` (`boolean|string|number|json`),
  `variations`, `description`, `public`. Boolean flags always have exactly `off`/`on`.
- A **flag config** is per environment: `enabled`, `off_variation`, `targets` (specific
  context keys), `rules` (clauses, first match wins), `fallthrough` (a variation or a
  percentage rollout whose weights sum to 100).
- Keys match `^[a-z][a-z0-9_.-]*$`; convention is `area.thing` (`checkout.v2`, `mobile.apply_enabled`).
- SDKs stream the raw ruleset over SSE and evaluate **locally**; the evaluation context
  (`key` + attributes) never leaves the app. A disabled or missing flag returns the caller's default.
- `type` and `key` are immutable; change them by delete + recreate.

## Step 0: collect the facts

1. Project key (stable forever) and environment. New projects get `production` only;
   creating a project needs a **global** key, so that is the owner's job in the UI.
2. Who creates the flag. Agents normally cannot reach flagsd (no route from a laptop,
   and the UI sits behind SSO). Either hand the owner the exact `key`, `type`,
   `description`, `public` and initial config to enter in the UI, or run the API
   calls below from a shell that can reach flagsd (local dev, or a container on the
   flags stack's Docker network on the host).
3. Which flags the browser/mobile client needs. Those become `public` (next section).

## Public vs private

`public` is project-wide metadata on the definition, not an environment setting.

- **Private** (default): backend-only. Evaluated by a server-side SDK with the full context.
- **Public**: may be shown to untrusted clients, but only as **evaluated values**. flagsd
  never serves browsers. The project's own edge/API service evaluates its `public`
  flags with an SDK (`AllFlags`, filtered to `public`) and returns `{key: value}`;
  rules, targets and rollouts never leave the trusted network. Client-asserted context
  is spoofable, so public flags gate rollout and UX, never security.
- The UI list filters All/Public/Private; flip visibility there or `PATCH` `{"public":true}`.

## Adding a flag

**UI:** project → Flags → new flag (boolean, private, disabled by default; the chosen
environment is preconfigured to return `on` for everyone once enabled). Toggle, set a
percentage rollout, or edit targets/rules in the configuration JSON dialog.

**API:** every mutation needs a write-capable `ffk_` key plus attribution headers.

```bash
URL=http://flagsd:8080            # local dev: http://127.0.0.1:8080
H=(-H "Authorization: Bearer $FLAGS_ADMIN_KEY" -H "X-User: $USER" -H 'X-Application: cli' -H 'Content-Type: application/json')

# 1. definition (project-wide)
curl -sS -X POST "$URL/v1/projects/perchd/flags" "${H[@]}" -d '{
  "key":"checkout.v2","type":"boolean","description":"New checkout flow","public":false,
  "variations":[{"key":"off","value":false},{"key":"on","value":true}]}'

# 2. per-environment behaviour (whole-document PATCH; send full arrays)
curl -sS -X PATCH "$URL/v1/projects/perchd/environments/production/flags/checkout.v2" "${H[@]}" -d '{
  "enabled":true,"off_variation":"off",
  "targets":[{"variation":"on","keys":["user_123"]}],
  "rules":[{"clauses":[{"attribute":"country","operator":"in","values":["NZ","AU"]}],"variation":"on"}],
  "fallthrough":{"rollout":{"variations":[{"variation":"on","weight":10},{"variation":"off","weight":90}]}}}'
```

Multivariate: `"type":"string"` with `variations:[{"key":"red","value":"red"},…]` and a
`fallthrough` naming one of them. Operators: `eq neq in not_in contains not_contains
starts_with ends_with gt gte lt lte exists not_exists`. Rollouts bucket on the context
`key` with the flag key as seed; changing weights moves users between buckets.

## Removing a flag

1. Delete the code reads first and ship them, so nothing depends on the flag.
2. Remove the flag: UI flag page → Delete, or `DELETE /v1/projects/{p}/flags/{key}`
   (always allowed, never blocked by validation). Connected SDKs get the new snapshot
   immediately; any stale read returns the caller's default with reason `ERROR`.
3. Every mutation lands in the project's audit log (`/projects/{p}/audit`).

## Wiring an SDK

**Key.** Mint an environment-scoped `{read}` key: UI → project → Keys (secret shown
once), or `POST /v1/keys` with `{"capabilities":["read"],"project":"perchd","env":"production","name":"backend"}`.
One key per consuming service; rotate by minting a new one and revoking the old
(`DELETE /v1/keys/{prefix}`). Never embed a key in a browser or mobile build.

**Reach.** flagsd publishes no ports. A deployed consumer must sit on a Docker network
flagsd joins (ask the owner which; wire it with the `deploy-stack` skill) and use
`http://flagsd:8080`. Store the key as a secret, never in config or git. Suggested
settings: `FLAGS_URL`, `FLAGS_KEY`, `FLAGS_PROJECT`, `FLAGS_ENV`. Unset URL ⇒ the
client should no-op and return defaults; flags must be safe to run without.

**Install.** Both SDKs live in the private `JeremyVun/flags` repo; install steps and
credentials are in `docs/PUBLISHING.md` Part 2 (`GOPRIVATE` + `go get
github.com/JeremyVun/flags/sdk/go@vX.Y.Z`; NuGet `FlagsSdk` from GitHub Packages).
If the tag or package is missing, the SDK has not been released yet: ask the owner
rather than vendoring a copy.

**Go** (package `flags`):

```go
client, err := flags.NewClient(flags.Config{
    ServiceURL: os.Getenv("FLAGS_URL"), Key: os.Getenv("FLAGS_KEY"),
    Project: "perchd", Environment: "production",
    User: "svc:checkout", Application: "checkout-api", // optional read attribution
})
defer client.Close()                       // NewClient never blocks boot
_ = client.WaitReady(ctx)                  // optional: readiness probe
ec := flags.EvalContext{Key: userID, Attributes: map[string]any{"country": "NZ"}}
if client.BoolVariation("checkout.v2", ec, false) { /* new path */ }
d := client.BoolVariationDetail("checkout.v2", ec, false) // Value, Variation, Reason
client.OnChange(func(changed []string) { /* react */ })
```

**.NET** (namespace `FlagsSdk`, `net10.0`):

```csharp
await using var flags = await FlagsClient.CreateAsync(new FlagsConfig {
    ServiceUrl = url, Key = key, Project = "steeple", Environment = "production",
    User = "svc:steeple", Application = "steeple-api" });
await flags.WaitReadyAsync(ct);                                   // optional
var ctx = new EvalContext(userId);
bool on = flags.BoolVariation("payments.enabled", ctx, def: false);
flags.OnChange += keys => { /* react */ };
```

Also available: `String/Int/Float(Double)/Json` variations, `*Detail` variants,
`AllFlags(ctx)`. Register one client per process as a singleton. `FailMode`
(`FailDefault|FailOpen|FailClosed`) only applies before first sync or when stale; a
missing flag always returns the caller's default. There is no browser SDK: web and
mobile clients call the project's own edge endpoint for evaluated public flags.

## Verify

```bash
# server-side check of the stored rules (read key is enough)
curl -sS -X POST "$URL/v1/projects/perchd/environments/production/flags/checkout.v2/evaluate" \
  -H "Authorization: Bearer $FLAGS_KEY" -H 'Content-Type: application/json' \
  -d '{"context":{"key":"user_123","attributes":{"country":"NZ"}}}'
# → {"value":true,"variation":"on","reason":"TARGET_MATCH"}
```

Then confirm from the real app with a `*VariationDetail` log line. `401` = missing or
revoked key; `403` = key lacks the capability or is scoped to another project/env;
`400 missing_attribution` = mutation without `X-User`/`X-Application`; `503` = flagsd
cache still warming (retry). Record the project's flag inventory (key, type, public,
owner, removal condition) in the project's own docs; the service will not do it for you.
