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
snow stage create MYDB.PUBLIC.LOAD -c dev
snow stage copy ./seed/use_cases.csv @MYDB.PUBLIC.LOAD -c dev   # upload
snow stage copy @MYDB.PUBLIC.LOAD ./out/ -c dev                 # download
snow stage list-files @MYDB.PUBLIC.LOAD -c dev
snow stage execute @MYDB.PUBLIC.LOAD/setup.sql -c dev
```
Typical use: stage a CSV/Parquet file, then `COPY INTO` a table from SQL.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/stage-commands/overview
