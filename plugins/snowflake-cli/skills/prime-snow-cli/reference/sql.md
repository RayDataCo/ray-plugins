# `snow sql` — execute SQL (the primary use)

`snow sql` runs a query, a `.sql` file, or stdin against a Snowflake connection. This is the main reason this skill exists.

## Invocations
```bash
snow sql -q "SELECT current_version();"      # inline query (-q / --query)
snow sql -f path/to/script.sql               # run a file (-f / --filename); -f is repeatable, runs in order
cat script.sql | snow sql -i                  # from stdin (-i / --stdin)
snow sql -q "SELECT 1" -c dev                 # target a named connection (-c / --connection)
snow sql -q "SELECT 1" -x --account ... --authenticator EXTERNALBROWSER
                                              # -x / --temporary-connection: ad-hoc, ignores config.toml (CI-friendly)
```
You can combine `-q` and multiple `-f`; they execute in the order given.

## Options that matter
- `--format TABLE|JSON|JSON_EXT|CSV` — output format. Use `--format json` whenever a script or agent needs to parse results. TABLE is the human default.
- `-D, --variable key=value` — client-side templating; reference in SQL as `<% key %>`. Example: `snow sql -f deploy.sql -D schema=analytics` with `CREATE SCHEMA <% schema %>;`.
- `--single-transaction` — wrap the whole file/batch in one transaction (rollback on error). Use for multi-statement DDL so a partial failure doesn't half-apply.
- `--retain-comments` — keep comments when sending SQL.
- `-c/--connection`, `-x/--temporary-connection` — see `global-options.md`.

## Examples
```bash
snow sql -f migrations/001_init.sql -c dev --single-transaction --format json
snow sql -q "SELECT current_account(), current_role(), current_warehouse();" -c dev
snow sql -f deploy.sql -D schema=analytics -c dev
```

## Tips
- Run against a dev/sandbox connection first for anything destructive; promote to prod only after a verified run.
- Idempotent DDL (`CREATE ... IF NOT EXISTS`); `CREATE OR REPLACE` only when you mean it.
- A multi-statement `.sql` file runs statement-by-statement; without `--single-transaction`, a mid-file error leaves earlier statements committed.
- `--enhanced-exit-codes` distinguishes failure types in scripts.
- Snowflake treats PK/FK/UNIQUE constraints as informational (not enforced) — worth knowing if you later move the schema to an engine that does enforce them.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/sql-commands/sql
