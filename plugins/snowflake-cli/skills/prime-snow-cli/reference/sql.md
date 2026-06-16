# `snow sql` — execute SQL (the primary use)

`snow sql` runs a query, a `.sql` file, or stdin against a Snowflake connection. This is the main reason this skill exists.

## Invocations
```bash
snow sql -q "SELECT current_version();"      # inline query (-q / --query)
snow sql -f path/to/script.sql               # run a file (-f / --filename); -f is repeatable, runs in order
cat script.sql | snow sql -i                  # from stdin (-i / --stdin)
snow sql -q "SELECT 1" -c caf_sandbox         # target a connection (-c / --connection)
snow sql -q "SELECT 1" -x --account ... --user ... --authenticator EXTERNALBROWSER
                                              # -x / --temporary-connection: ad-hoc, ignores config.toml (CI-friendly)
```
You can combine `-q` and multiple `-f`; they execute in the order given.

## Options that matter
- `--format TABLE|JSON|JSON_EXT|CSV` — output format. **Use `--format json` whenever an agent needs to parse results.** TABLE is the human default.
- `-D, --variable key=value` — client-side templating. Reference in SQL as `<% key %>`. Templating is on by default; `--enable-templating` controls the engine. Example: `snow sql -f deploy.sql -D schema=catalog_v1` with `CREATE SCHEMA <% schema %>;`.
- `--single-transaction` — wrap the whole file/batch in one transaction (BEGIN/COMMIT; rollback on error). **Use for multi-statement DDL** so a partial failure doesn't leave a half-applied schema.
- `--retain-comments` — keep comments when sending SQL (useful when comments carry hints).
- `-c/--connection`, `-x/--temporary-connection` — see `global-options.md`.

## RDCO patterns (CAF catalog deploy)
```bash
# Deploy the catalog DDL to the sandbox, all-or-nothing, parseable result:
snow sql -f ddl/catalog.sql -c caf_sandbox --single-transaction --format json

# Smoke-test a connection + role before deploying:
snow sql -q "SELECT current_account(), current_role(), current_warehouse();" -c caf_sandbox

# Parameterize the target schema across sandbox/prod:
snow sql -f ddl/catalog.sql -D schema=catalog_v1 -c caf_sandbox
```
Guardrails: **sandbox-first** (never point a destructive run at prod until it's verified on a sandbox connection); **idempotent DDL** (`CREATE ... IF NOT EXISTS`, `CREATE OR REPLACE` only when intended); author **enforced-style constraints** (PK/FK/UNIQUE/NOT NULL) even though Snowflake treats them as informational — they document intent and become live on a Postgres migration (see the CAF ERD doc); prefer `GENERATED ALWAYS AS IDENTITY` and **lowercase-unquoted** identifiers for portability; never echo secrets in logged SQL.

## Gotchas
- Exit codes: add `--enhanced-exit-codes` to distinguish failure types in scripts.
- A `.sql` file with multiple statements runs statement-by-statement; without `--single-transaction` a mid-file error leaves earlier statements committed.
- `snow sql` opens a session, so it accepts all the session/auth global flags (account/user/role/warehouse/database/schema) and connection selection.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/sql-commands/sql
