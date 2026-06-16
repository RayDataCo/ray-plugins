# `snow connection` — selecting & switching connections

This skill assumes you already have a working connection — i.e. `snow connection test` passes for it. **Setting up a connection and authentication is out of scope** (see the Snowflake docs). What's useful here: picking which connection a command runs against.

## Subcommands (`snow connection --help`)
| Subcommand | Purpose |
|---|---|
| `list` | Show all configured connections |
| `test` | Verify a connection authenticates and opens a session |
| `set-default` | Mark a connection as the default |
| `add` | Register a new connection *(setup — see docs)* |
| `remove` | Delete a connection |
| `generate-jwt` | Mint a JWT for key-pair auth |
| `generate-workload-identity-token` | Produce a workload-identity token |

## Switching between connections
```bash
snow connection list                 # see what you have
snow connection test -c dev          # confirm it works
snow connection set-default dev      # make it the default
snow sql -q "SELECT 1" -c prod       # or pick per-command with -c
snow sql -q "SELECT 1" -x ...        # -x = temporary, config-less (CI)
```
Most commands accept `-c <name>`; without it, the default connection is used.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/connection-commands/overview
