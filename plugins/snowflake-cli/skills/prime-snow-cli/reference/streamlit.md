# `snow streamlit` — Streamlit-in-Snowflake apps

Deploy and manage Streamlit apps that run inside Snowflake.

| Subcommand | Purpose |
|---|---|
| `deploy` | Deploy a Streamlit app to Snowflake |
| `list` | List Streamlit apps in the account |
| `describe` | Show details about an app |
| `get-url` | Retrieve the app's URL |
| `execute` | Run a Streamlit app |
| `logs` | View logs for an app |
| `share` | Grant a role/user access to the app |
| `drop` | Remove a Streamlit app |

```bash
snow streamlit deploy -c caf_sandbox
snow streamlit get-url <name> -c caf_sandbox
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/streamlit-commands/overview
