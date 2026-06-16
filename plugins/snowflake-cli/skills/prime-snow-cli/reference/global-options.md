# Global options & flags

Flags that ride on most `snow` commands. Commands that open a Snowflake session (e.g. `snow sql`) accept the connection/session overrides; session-less commands (e.g. `snow connection list`) don't.

## Connection selection
- `-c, --connection, --environment <name>` — use a named connection from `config.toml`.
- `-x, --temporary-connection` — build an ad-hoc connection from CLI flags, ignoring `config.toml`. Use in CI.
- `--config-file <path>` — use a specific config file (top-level).

## Session / auth overrides (long flags only — no `-a/-u/-r/-d/-w`)
`--account/--accountname` · `--user/--username` · `--password` · `--role/--rolename` · `--database/--dbname` · `--schema/--schemaname` · `--warehouse` · `--authenticator` · `--private-key-file` · `--token-file-path` · `--mfa-passcode`

> Prefer env vars / 1Password over `--password` on the command line (it lands in shell history). See `connection-and-auth.md`.

## Output & logging
- `--format TABLE|JSON|JSON_EXT|CSV` — output format. `--format json` for anything an agent parses.
- `-v/--verbose`, `--debug`, `--silent` — log verbosity.
- `--enhanced-exit-codes` — distinct exit codes per failure type (use in scripts).

## Top-level only (bare `snow --help`)
- `--version`, `--info`, `--help`.

## Single-letter flags that exist
Only `-c` (connection), `-x` (temporary connection), `-v` (verbose), and on `snow sql`: `-q` (query), `-f` (filename), `-i` (stdin), `-D` (variable). Everything else is a long flag.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/overview
