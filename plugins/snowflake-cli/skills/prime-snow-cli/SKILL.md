---
name: prime-snow-cli
description: Prime Claude Code to use the Snowflake CLI (`snow`) — primarily to EXECUTE SQL and deploy DDL against Snowflake, and as a navigable reference to the whole `snow` command tree. Use when running SQL/queries against Snowflake from the command line, deploying schema/DDL, managing objects, stages, Snowpark, Streamlit, or Native Apps, or when the user says "use snow", "snow CLI", "run this in Snowflake", "deploy to Snowflake", "/prime-snow-cli". Mirrors `snow --help`; each command group has a reference file with pointers to the official docs.
---

# Prime: Snowflake CLI (`snow`)

The Snowflake CLI is **`snow`** (pip package `snowflake-cli`). This skill is an **index** for using it: the Execute SQL quickstart covers the main case; the command tree maps every group to a `reference/` file that mirrors `snow <group> --help` and points at the official docs.

**Prerequisite:** you already have `snow` installed and a working connection — i.e. `snow connection test` passes. This skill does **not** cover installation or connection/auth setup (those live in the Snowflake docs); it picks up once you can connect.

> Verified against docs.snowflake.com/en/developer-guide/snowflake-cli (June 2026). The CLI changes — re-verify a specific command against its doc page before relying on edge details.

## Quickstart — Execute SQL (the main job)
Full detail: **`reference/sql.md`**. The commands that matter:
```bash
snow sql -q "SELECT current_version();"          # inline query
snow sql -f schema/migration.sql                 # run a .sql file (-f repeatable)
snow sql -f ddl.sql --single-transaction         # all-or-nothing DDL
snow sql -q "..." -D schema=analytics            # templating: <% schema %> in the SQL
snow sql -q "..." --format json                  # parseable output (TABLE default; JSON/JSON_EXT/CSV)
snow sql -f ddl.sql -c dev                       # -c picks a connection (-x = temporary, config-less, for CI)
```
Tips: dev/sandbox connection first for destructive runs; idempotent DDL (`CREATE ... IF NOT EXISTS`); `--format json` when a script parses results.

## Switching connections
With more than one connection: `snow connection list`, then `snow connection set-default <name>`, or pick per-command with `-c <name>`. Detail: **`reference/connection.md`**. (Creating/authenticating a connection is out of scope — see the docs.)

## The command tree — `snow <group>` → reference file
Mirrors `snow --help`. Read the reference file for a group before using it; each ends with its official doc URL.

| Group | What it does | Reference |
|---|---|---|
| `sql` *(leaf)* | Execute a query / .sql file / stdin | **reference/sql.md** |
| `connection` | Select/switch among configured connections | **reference/connection.md** |
| `object` | Generic object create/describe/drop/list | **reference/object.md** |
| `stage` | Stages + staged-file transfer (`stage copy`) | **reference/stage.md** |
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
| *(global flags)* | `-c/-x`, `--format`, session overrides | **reference/global-options.md** |

## Notes
- `init` is `snow bootstrap init` (not top-level). `dcm` is preview, behind `SNOWFLAKE_CLI_FEATURES_ENABLE_SNOWFLAKE_PROJECTS`.
- Single-letter flags exist only for `-c` (connection), `-x` (temporary connection), `-v` (verbose), `-q`/`-f`/`-i`/`-D` (on `snow sql`). Everything else uses long flags (`--account`, `--role`, …) — no `-a/-u/-r/-d`.
- Official docs root: https://docs.snowflake.com/en/developer-guide/snowflake-cli/index
