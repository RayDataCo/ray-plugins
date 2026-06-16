# `snow stage` — stages and staged files

Manage Snowflake stages and move files in/out. There is **no `put`/`get`** — upload and download both use `stage copy`.

| Subcommand | Purpose |
|---|---|
| `copy` | Transfer files between local and a stage (both directions) |
| `create` | Create a new stage |
| `list` | List stages |
| `list-files` | List files within a stage |
| `describe` | Show stage details |
| `execute` | Run/execute staged files (e.g. SQL on a stage) |
| `remove` | Delete files from a stage |
| `drop` | Remove a stage |

```bash
snow stage create CAF.CATALOG.LOAD -c caf_sandbox
snow stage copy ./seed/use_cases.csv @CAF.CATALOG.LOAD -c caf_sandbox   # upload
snow stage copy @CAF.CATALOG.LOAD ./out/ -c caf_sandbox                 # download
snow stage list-files @CAF.CATALOG.LOAD -c caf_sandbox
snow stage execute @CAF.CATALOG.LOAD/setup.sql -c caf_sandbox
```
Typical CAF use: stage a CSV/Parquet of seed use-cases, then `COPY INTO` from SQL.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/stage-commands/overview
