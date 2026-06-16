# `snow notebook` — Snowflake notebooks

Manage Snowflake notebooks.

| Subcommand | Purpose |
|---|---|
| `create` | Create a new notebook |
| `deploy` | Deploy a notebook to Snowflake |
| `execute` | Execute a notebook |
| `get-url` | Get a notebook's URL |
| `open` | Open a notebook in the browser |

```bash
snow notebook deploy -c caf_sandbox
snow notebook execute <name> -c caf_sandbox
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/notebook-commands/overview
