---
name: deploy-stack
description: Register, deploy, redeploy, and manage a project's Compose stack on the `projects` infra repo (deployctl GitOps; host syd1 or another host/group). Use when asked to deploy, redeploy, ship, or host an app; add or rotate a secret (secrets.env → secrets.env.age); give an app a database on the shared Postgres; gate it behind Authelia SSO; route a domain through the edge-proxy; push an image to the registry; or debug a deploy.
---

# Deploy a project as a stack

Infra repo: `/Users/jeremy/projects/projects`. Its `README.md` and `docs/` are
authoritative; this skill is the workflow and the rules. **Git is the desired state:**
the VM pulls `origin/main` and converges. A deploy is edit → commit → push → trigger.
Never SSH to deploy.

- `stacks/<stack>/` = one Compose project; dir name = project name = volume prefix.
- `hosts/<host>.yaml` + `groups/<g>.yaml` decide placement. One line moves a stack.
- `deployctl` is one binary: agent on the VM, client on the laptop (`--host`/`--group`).
- Real host today: `syd1`, app domains `<stack>.jeremyvun.com`. `vm1` is a template.
- Exemplars: `stacks/ilovetrains` (public app, one secret), `stacks/analytics`
  (Postgres tenant + path-scoped SSO), `stacks/mortgage-calc` (static, has a README).

## 1. Collect facts

Derive from the project repo; ask only for the rest: stack name
(`^[a-z0-9][a-z0-9_-]*$`, permanent), target host/group, public hostname(s), which
paths need SSO, whether it needs Postgres or volumes, every env var the image reads
classified secret vs non-secret, image name, listen port, health endpoint.

## 2. Secrets and config

| file | committed | holds |
|---|---|---|
| `config.env` | yes | ports, URLs, flags, DB user/name |
| `secrets.env` | never | plaintext you edit locally (chmod 600) |
| `secrets.env.age` | yes | the sealed ciphertext the box decrypts |
| `secrets.env.example` | yes | key map, empty values, one comment per key |

Compose reads them by `${VAR}` interpolation; guard required secrets with
`${VAR:?message}` so a missing value fails loudly.

**Never read `secrets.env`.** Use `secrets.env.example` for keys and
`make verify STACK=<s>` for parity. If you truly must, ask for approval first, then
view only `sed -E 's/=.*/=***/' stacks/<s>/secrets.env`. Never `cat`, `source`, echo a
value, run a bare `docker compose config`, or put a secret in a commit or report.

Write without reading: generated values go in via one command so they never print,
mirrored wherever they must match:

```bash
pw="$(openssl rand -hex 24)"
printf 'DB_PASSWORD=%s\n' "$pw" >> stacks/<s>/secrets.env
printf '<S>_DB_PASSWORD=%s\n' "$pw" >> stacks/postgres/secrets.env
```

User-supplied values: the user adds them (`! $EDITOR stacks/<s>/secrets.env`), not via chat.

Seal: `make seal STACK=<s>`. The pre-commit hook reseals drifted stacks and blocks
staged plaintext. Secret *files* (rare): `deployctl secrets seal-file <path>`.

## 3. Register the stack

1. Create `stacks/<stack>/docker-compose.yml`, `config.env`, `secrets.env.example`
   (plus a short `README.md` if the wiring is non-obvious). Minimal public service:
   ```yaml
   name: <stack>
   services:
     <stack>:
       image: ${REGISTRY_DOMAIN}/<image>:latest      # REGISTRY_DOMAIN is injected; never define it
       environment: { PORT: "${<STACK>_PORT}", API_KEY: "${API_KEY:?seal API_KEY}" }
       expose: ["${<STACK>_PORT}"]                   # never ports: — Caddy is the only entry
       networks: [edge-proxy]                        # + shared-db for Postgres, <stack>-net for sidecars
       labels:
         caddy: <stack>.jeremyvun.com
         caddy.reverse_proxy: "{{upstreams ${<STACK>_PORT}}}"
       restart: unless-stopped
       healthcheck:                                  # required; the engine gates on it
         test: ["CMD-SHELL", "wget -q -O /dev/null http://localhost:${<STACK>_PORT}/healthz || exit 1"]
         interval: 15s
         timeout: 5s
         retries: 5
         start_period: 10s
   networks:
     edge-proxy: { external: true }
   ```
2. Stage secrets (§2), `make seal STACK=<stack>`.
3. Add `<stack>` to `hosts/syd1.yaml` (or a group). Unassigned stacks 404 on redeploy.
4. Commit by explicit file list, never `git add -A` (a background auto-committer sweeps
   this tree, so do not leave a half-built stack uncommitted). Push.
5. DNS: an owner action unless the repo provides a tool. State the exact record:
   `<stack>.jeremyvun.com` → the VM, proxied (orange), SSL mode Full (strict). Caddy
   issues the certificate itself.

## 4. Build, push, deploy, verify

```bash
# project repo (copy examples/project-build/* if it has no bake files)
docker buildx bake -f docker-bake.hcl -f versions.hcl --push     # linux/amd64 → registry.jeremyvun.com/<image>
# infra repo — OIDC secret is read from a file and scoped to the run
cli/deploy.sh <stack>            # hard redeploy, waits, prints the job log tail
cli/deploy.sh --stacks a,b       # several together (e.g. postgres,<stack> on first tenant deploy)
cli/deploy.sh --all              # gentle reconcile of every assigned stack
deployctl --help                 # raw client: redeploy/reconcile/status/hosts; flags BEFORE the stack name
```

Modes: gentle (`up -d`, also applies config/secret changes), hard (recreate + pull,
after an image push), sledgehammer (`down` then `up`, wedged stack; volumes survive).
Push before deploying: reconcile resets to `origin/main`. `409` = busy, retry.
Registry push 401 → user runs `! docker login registry.jeremyvun.com`; never handle the password.

Verify every time: `curl -sSI https://<host>/healthz` returns 200 with a valid cert,
then drive one real flow. A healthy container but 404/502 from Caddy means a bad label
(non-numeric ordered suffix, malformed directive). On-box inspection needs the owner's
break-glass SSH; ask first and never read an on-box `.env` or `.runtime.env`.

## 5. Shared services

**edge-proxy (caddy-docker-proxy).** Routing is entirely `caddy.*` labels on your
service; nothing in the proxy stack changes. Numeric prefixes order directives
(`caddy.route.0_…`). Multiple hostnames are space-separated on `caddy:`. Trust
`X-Forwarded-For` from the proxy.

**postgres (shared instance, one database + role per project).** Reachable only over
the external `shared-db` network at `postgres:5432`. Onboard with three edits in
`stacks/postgres/`: copy `provision.d/analytics.sql` to `<stack>.sql` (edit role, db,
`\getenv` name); add `<STACK>_DB_PASSWORD` to its `secrets.env` and seal; forward it in
`docker-compose.yml` `provision.environment:` as plain `${<STACK>_DB_PASSWORD}` (no
`:?`). Your stack sets `POSTGRES_USER`/`POSTGRES_DB` in `config.env`, the identical
password in `secrets.env`, builds
`postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable`,
joins `shared-db`, and runs its own migrations as its own role. Deploy postgres before
or with the app.

**authelia (SSO).** Add to your service:
```yaml
caddy.forward_auth: "authelia:9091"
caddy.forward_auth.uri: "/api/authz/forward-auth"
caddy.forward_auth.copy_headers: "Remote-User Remote-Groups Remote-Email Remote-Name"
```
and a `domain: '<host>'` / `policy: 'one_factor'` rule under `access_control.rules` in
`stacks/authelia/configuration.yml` (domain-scoped; see the file's notes before using
`resources:`). `*.jeremyvun.com` is already a cookie domain; a new parent domain needs a
cookie block, a portal hostname, and DNS. Config changes need `cli/deploy.sh authelia`.
Trust `Remote-User` only on gated routes and strip it from clients first
(`stacks/analytics` shows how). Leave `stacks/authelia/auth/` alone.

**registry.** `${REGISTRY_DOMAIN}/<image>:<tag>`; box and laptop are already logged in.

## 6. Change, move, retire

New image → push + `cli/deploy.sh <stack>`. Config/secret change → edit, seal, commit,
push, deploy. Move → move the manifest line, reconcile both hosts. Retire → remove the
manifest line (next reconcile runs `down` without `-v`); delete the dir, Authelia rule,
and provision file only when asked. Roll back → `git revert`, push, reconcile.

## Gotchas

- `$` in a value reaching Compose interpolation (bcrypt hashes) must be `$$`.
- `secrets.env` must end in a newline before appending.
- Keep each stack's port in its own `config.env` key so healthcheck and label agree.
- `git status` before every push; the auto-committer moves `main` under you.
