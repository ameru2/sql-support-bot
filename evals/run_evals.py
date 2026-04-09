from __future__ import annotations

import os
from typing import Any

from langsmith.evaluation import evaluate

from agent import create_agent
from evals.cases import EVAL_CASES
from evals.evaluators import (
    asks_for_customer_id,
    avoids_forbidden_terms,
    contains_expected_any,
    graceful_scope_limit,
    returns_nonempty_answer,
)

_agent = create_agent()

def run_sql_support_bot(inputs: dict[str, Any]) -> dict[str, str]:
    """
    Stable wrapper around the repo's global `agent`.
    Expects:
      {
        "messages": [...],
        ...
      }
    Returns:
      {
        "output": "<final assistant message text>"
      }
    """
    _agent = create_agent()

def run_sql_support_bot(inputs: dict[str, Any]) -> dict[str, str]:
    result = _agent.invoke({"messages": inputs["messages"]})
    messages = result.get("messages", [])

    if not messages:
        return {"output": ""}

    last = messages[-1]
    content = getattr(last, "content", str(last))
    if isinstance(content, list):
        content = " ".join(str(x) for x in content)
    return {"output": str(content)}


if __name__ == "__main__":
    upload_results = os.getenv("LANGSMITH_TRACING", "").lower() in {"1", "true", "yes"}

    results = evaluate(
        run_sql_support_bot,
        data=EVAL_CASES,
        evaluators=[
            returns_nonempty_answer,
            asks_for_customer_id,
            graceful_scope_limit,
            contains_expected_any,
            avoids_forbidden_terms,
        ],
        experiment_prefix="sql-support-bot",
        upload_results=upload_results,
    )

    print(results)
