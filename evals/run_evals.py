from __future__ import annotations

import os
from typing import Any

from langsmith import Client
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
ls_client = Client()

DATASET_NAME = "sql-support-bot-evals"


def run_sql_support_bot(inputs: dict[str, Any]) -> dict[str, str]:
    """Stable wrapper for LangSmith evaluation."""
    result = _agent.invoke({"messages": inputs["messages"]})
    messages = result.get("messages", [])

    if not messages:
        return {"output": ""}

    last = messages[-1]
    content = getattr(last, "content", str(last))
    if isinstance(content, list):
        content = " ".join(str(x) for x in content)

    return {"output": str(content)}


def ensure_dataset(dataset_name: str) -> str:
    """Create or refresh a LangSmith dataset from local EVAL_CASES."""
    try:
        dataset = ls_client.read_dataset(dataset_name=dataset_name)

        # Clear old examples so the dataset stays in sync with local cases
        for ex in ls_client.list_examples(dataset_id=dataset.id):
            ls_client.delete_example(example_id=ex.id)

    except Exception:
        dataset = ls_client.create_dataset(
            dataset_name=dataset_name,
            description="Eval cases for the SQL support bot take-home.",
        )

    examples = []
    for case in EVAL_CASES:
        examples.append(
            {
                "inputs": case["inputs"],
                "outputs": {
                    "expected_behavior": case["inputs"].get("expected_behavior", "")
                },
                "metadata": {
                    "name": case["name"],
                    "category": case["inputs"].get("category", ""),
                },
            }
        )

    ls_client.create_examples(dataset_id=dataset.id, examples=examples)
    return dataset.name


if __name__ == "__main__":
    upload_results = os.getenv("LANGSMITH_TRACING", "").lower() in {"1", "true", "yes"}

    dataset_name = ensure_dataset(DATASET_NAME)

    results = evaluate(
        run_sql_support_bot,
        data=dataset_name,
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
