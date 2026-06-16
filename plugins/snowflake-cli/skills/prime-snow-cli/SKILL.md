---
name: prime-snow-cli
description: Prime Claude Code to use the Snowflake CLI (`snow`) — primarily to EXECUTE SQL and deploy DDL against Snowflake, and as a navigable reference to the whole `snow` command tree. Use when running SQL/queries against Snowflake from the command line, deploying schema/DDL, managing connections, objects, stages, Snowpark, Streamlit, or Native Apps, or when the user says "use snow", "snow CLI", "run this in Snowflake", "deploy to Snowflake", "/prime-snow-cli". Mirrors `snow --help`; each command group has a reference file with pointers to the official docs.
---

# Prime: Snowflake CLI (`snow`)

The modern Snowflake CLI is **`snow`** (pip package `snowflake-cli`) — the developer/agent-facing tool. Use it over the legacy `snowsql` REPL for anything scripted. This skill is an **index**: the two quickstarts below cover the 90% case (connect securely, run SQL); the command tree maps every group to a `reference/` file that mirrors `snow <group> --help` and points at the official docs.

> Verified against docs.snowflake.com/en/developer-guide/snowflake-cli (June 2026). The CLI changes — re-verify a specific command against its doc page before relying on edge details. Not installed by default: `brew install snowflake-cli` (or `uv tool install snowflake-cli` / `pipx install snowflake-cli`, Python ≥3.10); confirm with `snow --version`.

## Quickstart 1 — Connect securely (do this once)
Full detail + all `snow connection` subcommands: **`reference/connection-and-auth.md`**. The short version, RDCO no-secrets-on-disk posture:

- Connections live in `~/.snowflake/config.toml` (`[connections.<name>]`); the CLI **requires `chmod 0600`** on it. Override the dir with `SNOWFLAKE_HOME`.
- **Use key-pair auth, not a password.** config.toml stores only the key FILE PATH — never key material or a password:
  ```toml
  [connections.caf_sandbox]
  account = "<org-account>"
  user = "<user>"
  authenticator = "SNOWFLAKE_JWT"
  private_key_file = "~/.snowflake/keys/caf.p8"
  role = "..."; warehouse = "..."; database = "..."; schema = "..."
  ```
- Passphrase via env, never config: `export PRIVATE_KEY_PASSPHRASE="$(op read 'op://Private/snowflake-caf/passphrase')"` (1Password).
- `snow connection add` → `snow connection test -c caf_sandbox` → `snow connection set-default caf_sandbox`.
- SSO alternative (no stored secret): `authenticator = "EXTERNALBROWSER"`.

## Quickstart 2 — Execute SQL (the main job)
Full detail: **`reference/sql.md`**. The commands that matter:
```bash
snow sql -q "SELECT current_version();"          # inline query
snow sql -f schema/use_case.sql                  # run a .sql file (-f repeatable)
snow sql -f ddl.sql --single-transaction         # all-or-nothing DDL
snow sql -q "..." -D env=sandbox                  # templating: <% env %> in the SQL
snow sql -q "..." --format json                  # parseable output (TABLE default; JSON/JSON_EXT/CSV)
snow sql -f ddl.sql -c caf_sandbox               # -c picks a connection (-x = temporary, config-less, for CI)
```
RDCO guardrails: sandbox-first; idempotent DDL (`CREATE ... IF NOT EXISTS`); per the CAF ERD, author enforced-style PK/FK/UNIQUE/NOT-NULL constraints even though Snowflake won't enforce them (they go live on a Postgres migration); `GENERATED ALWAYS AS IDENTITY` keys + lowercase-unquoted identifiers for portability; `--format json` whenever an agent parses results; never echo secrets.

## The command tree — `snow <group>` → reference file
Mirrors `snow --help`. Read the reference file for a group before using it; each ends with its official doc URL.

| Group | What it does | Reference |
|---|---|---|
| `sql` *(leaf)* | Execute a query / .sql file / stdin | **reference/sql.md** |
| `connection` | Manage connections + auth (config.toml) | **reference/connection-and-auth.md** |
| `object` | Generic object create/describe/drop/list | **reference/object.md** |
| `stage` | Stages + staged-file put/get (`stage copy`) | **reference/stage.md** |
| `snowpark` | Build/deploy Snowpark funcs & procs (+ `package`) | **reference/snowpark.md** |
| `streamlit` | Deploy/manage Streamlit-in-Snowflake apps | **reference/streamlit.md** |
| `app` | Native Apps lifecycle (+ version, release-*) | **reference/app.md** |
| `spcs` | Snowpark Container Services (compute-pool, service, image-*) | **reference/spcs.md** |
| `cortex` | Cortex AI (complete, summarize, translate, …) | **reference/cortex.md** |
| `dbt` | Manage dbt project objects in Snowflake | **reference/dbt.md** |
| `git` | Git repository integration in Snowflake | **reference/git.md** |
| `notebook` | Manage Snowflake notebooks | **reference/notebook.md** |
| `dcm` | Declarative change management (PREVIEW, flagged) | **reference/dcm.md** |
| `bootstrap` · `custom-image` · `logs` · `helpers` | Small/utility groups (init, image validate, logs, snowsql migration) | **reference/misc-and-helpers.md** |
| *(global flags)* | `-c/-x`, `--format`, auth/session overrides | **reference/global-options.md** |

## Notes
- `init` is `snow bootstrap init` (not top-level). `dcm` is preview, behind `SNOWFLAKE_CLI_FEATURES_ENABLE_SNOWFLAKE_PROJECTS`.
- Single-letter flags exist only for `-c` (connection), `-x` (temporary connection), `-v` (verbose), `-q`/`-f`/`-i`/`-D` (on `snow sql`). Everything else uses long flags (`--account`, `--role`, …) — no `-a/-u/-r/-d`.
- Official docs root: https://docs.snowflake.com/en/developer-guide/snowflake-cli/index
