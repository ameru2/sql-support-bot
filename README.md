# SQL Support Bot Evals

This repo includes two fast eval loops:

1. `pytest` smoke tests for quick local regression checks
2. LangSmith dataset-style evals for experiment-style runs

## Why these evals

The agent supports two main jobs:
- music/catalog lookup
- customer account lookup

The key behaviors to test are:
- basic catalog retrieval
- fuzzy match / recovery behavior
- requiring customer ID before account lookup
- multi-turn account flows
- robustness to malformed / adversarial input
- graceful handling of out-of-scope requests

## Run locally

Install dependencies:

```bash
uv sync
```

Set required env vars:

```bash
export OPENAI_API_KEY=your_key_here
```

Optional for LangSmith uploads:

```bash
export LANGSMITH_API_KEY=your_langsmith_key_here
export LANGSMITH_TRACING=true
```

Run smoke tests:

```bash
uv run pytest tests/agent_smoke_tests.py -q
```

Run eval script:

```bash
uv run python -m evals.run_evals
```

If `LANGSMITH_TRACING = true`, the results will also upload to LangSmith.

## Design choices

I intentionally used:

- small representative datasets
- mostly deterministic evaluators
- a stable target wrapper around the agent
- both single-turn and multi-turn test cases

This makes it easy to change prompts, tools, or model settings and quickly see regressions. 

## Robustness Bug Discovered via Evals

During evaluation, I included robustness test cases designed to simulate real-world user input, including punctuation and edge cases.

One such test uncovered a bug in the agent’s SQL tool layer:

**❌ Failing Case**

Input:

```bash
Do you have songs by Guns N' Roses?
```

**Observed behavior:**

The agent attempted to construct a SQL query using string interpolation
The apostrophe in N' broke the SQL syntax
Resulted in a runtime SQL error (sqlite3.OperationalError)

**Root cause:**
The SQL query was built using raw string interpolation:

```python
WHERE Artist.Name LIKE '%Guns N' Roses%';
```
This breaks because ' terminates the string early.

**🛠 Fix Implemented**

I fixed this by escaping user-provided input before inserting it into SQL queries.

``` python
def escape_sql_string(value: str) -> str:
    return value.replace("'", "''")
```

Then applied it in all SQL tool functions:

```python
artist_escaped = escape_sql_string(artist)
```

This ensures:

```bash
Guns N' Roses → Guns N'' Roses
```

which is valid SQL.

**✅ Result (after fix)**
- The same test case now passes
- The agent successfully returns songs by "Guns N' Roses"
- No SQL errors are thrown
