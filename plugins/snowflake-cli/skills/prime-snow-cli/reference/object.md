# `snow object` — generic object management

CRUD for generic Snowflake objects (tables, schemas, warehouses, roles, etc.) when there isn't a more specific group.

| Subcommand | Purpose |
|---|---|
| `create` | Create Snowflake objects |
| `describe` | Show details about an object |
| `drop` | Remove an object |
| `list` | List available objects of a type |

```bash
snow object list table -c caf_sandbox
snow object describe table CAF.CATALOG.USE_CASE -c caf_sandbox
snow object drop schema CAF.CATALOG_OLD -c caf_sandbox
```
Note: for actual DDL (create tables with columns/constraints) you'll usually run `snow sql -f ddl.sql`; `snow object create` is for simpler/templated object creation. `object list <type>` is the quick "what exists?" check.

Docs: https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/object-commands/overview
