# `snow connection` — connections & authentication

Manages the named connections in `config.toml` and how `snow` authenticates. Get this right once and every other command just uses `-c <name>`.

## Subcommands (`snow connection --help`)
| Subcommand | Purpose |
|---|---|
| `add` | Register a new connection (interactive prompts) |
| `list` | Show all configured connections |
| `test` | Verify a connection authenticates and can open a session |
| `set-default` | Mark a connection as the default (`default_connection_name`) |
| `remove` | Delete a connection |
| `generate-jwt` | Mint a JWT for key-pair auth (debugging/external use) |
| `generate-workload-identity-token` | Produce a workload-identity token |

```bash
snow connection add                 # interactive
snow connection test -c caf_sandbox
snow connection list
snow connection set-default caf_sandbox
```

## Where config lives
- File: **`~/.snowflake/config.toml`**, section `[connections.<name>]`. The CLI **requires `chmod 0600`** (owner-only) or it refuses to use the file.
- Override the directory with **`SNOWFLAKE_HOME`**, or a specific file with `--config-file`.
- A sibling `connections.toml` (shared with the VS Code ext / Cortex / SnowConvert) **takes precedence** if present — watch for it if a connection "won't update."

## Auth methods
| Method | `authenticator` | Where the secret lives |
|---|---|---|
| **Key-pair (preferred)** | `SNOWFLAKE_JWT` | config stores only `private_key_file` *path*; passphrase in `PRIVATE_KEY_PASSPHRASE` env |
| SSO / browser | `EXTERNALBROWSER` | nothing stored — opens a browser to auth |
| Password | (default) | **env only** — `SNOWFLAKE_PASSWORD` or `SNOWFLAKE_CONNECTIONS_<NAME>_PASSWORD`, never config |
| OAuth / PAT / MFA / Workload Identity | various | per docs |

## RDCO no-secrets-on-disk setup (do this)
```toml
[connections.caf_sandbox]
account = "<org-account>"
user = "<user>"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "~/.snowflake/keys/caf.p8"
role = "SYSADMIN"
warehouse = "DEV_WH"
database = "CAF"
schema = "CATALOG"
```
```bash
chmod 0600 ~/.snowflake/config.toml
export PRIVATE_KEY_PASSPHRASE="$(op read 'op://Private/snowflake-caf/passphrase')"   # 1Password
snow connection test -c caf_sandbox
```
**Rules:** never put a password or raw private key in `config.toml` or any repo. Key-pair = path-in-config + passphrase-in-env (1Password). Any TOML secret is plaintext; the docs themselves push env vars / `op read`. Generic env overrides also exist: `SNOWFLAKE_ACCOUNT/USER/ROLE/WAREHOUSE/AUTHENTICATOR/PRIVATE_KEY_PATH`.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/connection-commands/overview
· configure connections: https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections
