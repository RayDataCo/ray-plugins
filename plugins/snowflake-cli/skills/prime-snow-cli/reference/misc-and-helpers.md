# Small & utility groups: `bootstrap`, `custom-image`, `logs`, `helpers`

Single-command or utility groups, kept together. Each still mirrors `snow <group> --help`.

## `snow bootstrap`
| Subcommand | Purpose |
|---|---|
| `init` | Create a project directory from a template (`snow bootstrap init <name>`) |

This is where `init` lives — it is **not** a top-level `snow init`.

## `snow custom-image`
| Subcommand | Purpose |
|---|---|
| `validate` | Validate a Docker image against Snowflake (SPCS) requirements |

## `snow logs`
| Subcommand | Purpose |
|---|---|
| `logs` | Retrieve logs for a given Snowflake entity |

## `snow helpers` (migration off legacy SnowSQL)
| Subcommand | Purpose |
|---|---|
| `import-snowsql-connections` | Migrate SnowSQL connections into the new CLI |
| `check-snowsql-env-vars` | Verify SnowSQL env-var config |
| `v1-to-v2` | Migrate config from CLI v1 to v2 |

Docs (overviews under the same base):
- bootstrap: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/bootstrap-commands/overview
- custom-image: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/custom-image-commands/overview
- logs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/logs-commands/overview
- helpers: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/helpers-commands/overview
