# `snow dcm` — Declarative Change Management (PREVIEW)

Declarative, plan/apply-style project deployment (think Terraform-for-Snowflake). **Preview**, feature-flagged behind `SNOWFLAKE_CLI_FEATURES_ENABLE_SNOWFLAKE_PROJECTS` — re-verify before relying on it.

| Subcommand | Purpose |
|---|---|
| `create` | Create a DCM project |
| `plan` | Preview deployment changes before applying |
| `deploy` | Deploy a DCM project |
| `preview` | Preview project configuration |
| `describe` | Show project details |
| `list` / `list-deployments` | List projects / deployments |
| `refresh` | Update project state |
| `test` | Validate project configuration |
| `drop` / `drop-deployment` / `purge` | Tear down |

`plan` → `deploy` is a declarative (Terraform-like) deployment flow. Preview status = don't build production on it yet.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/dcm-commands/overview
