# `snow cortex` — Cortex AI functions

Call Snowflake Cortex LLM features from the CLI.

| Subcommand | Purpose |
|---|---|
| `complete` | Generate a text completion from a model |
| `summarize` | Summarize provided text |
| `translate` | Translate text between languages |
| `sentiment` | Analyze sentiment of input text |
| `extract-answer` | Extract answers from a document |

```bash
snow cortex complete "Explain VARIANT vs JSONB in one line" -c dev
snow cortex summarize -f long.txt -c dev
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/cortex-commands/overview
