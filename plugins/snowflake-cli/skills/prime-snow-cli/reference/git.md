# `snow git` — Git repository integration

Manage Git repositories registered inside Snowflake (run SQL/files straight from a repo).

| Subcommand | Purpose |
|---|---|
| `setup` | Set up Git repository integration |
| `fetch` | Fetch latest changes |
| `list` | List Git repositories |
| `list-branches` / `list-tags` / `list-files` | Inspect a repo |
| `describe` | Show repo object details |
| `copy` | Copy files from a repo/stage |
| `execute` | Run `EXECUTE IMMEDIATE` files from a repo |
| `drop` | Remove a Git repository |

```bash
snow git list -c caf_sandbox
snow git execute @my_repo/branches/main/deploy.sql -c caf_sandbox
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/git-commands/overview
