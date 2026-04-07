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
uv run pytest tests/test_agent_smoke.py -q
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
