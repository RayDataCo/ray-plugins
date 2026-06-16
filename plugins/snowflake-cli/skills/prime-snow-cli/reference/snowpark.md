# `snow snowpark` — Snowpark functions & procedures

Build, deploy, and manage Snowpark (Python/Java/Scala) user-defined functions and stored procedures.

| Subcommand | Purpose |
|---|---|
| `build` | Compile Snowpark code into deployable artifacts |
| `deploy` | Upload + register functions/procedures |
| `execute` | Run Snowpark code or a function |
| `describe` | Show details of a deployed object |
| `list` | List Snowpark objects |
| `drop` | Remove a function/procedure |

### `snow snowpark package` (subgroup — dependency management)
| Subcommand | Purpose |
|---|---|
| `create` | Build a package zip from a PyPI dependency |
| `lookup` | Check whether a package is natively available in Snowflake |
| `upload` | Upload a package zip to a stage |

```bash
snow snowpark package lookup pandas
snow snowpark build
snow snowpark deploy -c caf_sandbox
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/snowpark-commands/overview
