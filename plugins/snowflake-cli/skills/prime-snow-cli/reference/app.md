# `snow app` — Snowflake Native Apps

Develop → run → version → publish a Snowflake Native Application.

| Subcommand | Purpose |
|---|---|
| `run` | Create or upgrade the app in the account |
| `deploy` | Deploy app artifacts to the account stage |
| `bundle` | Package application files for deployment |
| `open` | Open the app in a browser |
| `validate` | Verify app configuration and files |
| `events` | Retrieve and display application events |
| `setup` | Set up application infrastructure |
| `teardown` | Remove app objects and infrastructure |
| `publish` | Publish an app version to a listing |

### `snow app version` (subgroup)
`create` · `drop` · `list` — manage versioned Native App builds.

### `snow app release-channel` (subgroup)
`list` · `add-version` · `remove-version` · `add-accounts` · `remove-accounts` · `set-accounts`

### `snow app release-directive` (subgroup)
`list` · `set` · `unset` · `add-accounts` · `remove-accounts`

```bash
snow app run -c caf_sandbox
snow app version create v1 -c caf_sandbox
snow app publish --version v1 -c caf_sandbox
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/native-apps-commands/overview
