# `snow spcs` — Snowpark Container Services

Manage container compute and services. Four subgroups.

### `snow spcs compute-pool` (subgroup)
`create` · `deploy` · `describe` · `list` · `status` · `set` · `unset` · `suspend` · `resume` · `stop-all` · `drop`

### `snow spcs service` (subgroup)
`create` · `deploy` · `describe` · `list` · `status` · `logs` · `metrics` · `events` · `execute-job` · `list-containers` · `list-endpoints` · `list-instances` · `list-roles` · `set` · `unset` · `suspend` · `resume` · `upgrade` · `drop`

### `snow spcs image-registry` (subgroup)
`login` · `token` · `url`

### `snow spcs image-repository` (subgroup)
`create` · `deploy` · `list` · `list-images` · `list-tags` · `url` · `drop`

```bash
snow spcs image-registry login -c caf_sandbox
snow spcs service list -c caf_sandbox
snow spcs service logs <name> -c caf_sandbox
```

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/spcs-commands/overview
(subgroup pages: `.../spcs-commands/<subgroup>-commands/overview`)
