# `snow dbt` — dbt project objects in Snowflake

Manage dbt projects as Snowflake objects (deploy + run them in-account).

| Subcommand | Purpose |
|---|---|
| `deploy` | Deploy a dbt project to Snowflake |
| `execute` | Run dbt commands against the deployed project |
| `list` | List dbt project objects |
| `describe` | Show info about a dbt project object |
| `drop` | Remove a dbt project object |

```bash
snow dbt deploy -c caf_sandbox
snow dbt execute run -c caf_sandbox
```
Relevant if the CAF catalog transforms move to dbt later.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/dbt-commands/overview
