import pytest

from evals.cases import EVAL_CASES
from evals.run_evals import run_sql_support_bot


@pytest.mark.parametrize("case", EVAL_CASES, ids=[c["name"] for c in EVAL_CASES])
def test_agent_smoke(case):
    inputs = case["inputs"]
    result = run_sql_support_bot(inputs)
    text = result["output"].lower()

    assert text.strip(), "Agent returned empty output"

    expected_behavior = inputs.get("expected_behavior")

    if expected_behavior == "asks_for_customer_id":
        assert ("customer id" in text) or ("customer" in text and "id" in text)

    if inputs.get("must_include_any"):
        assert any(term.lower() in text for term in inputs["must_include_any"])

    if inputs.get("must_not_include_any"):
        assert not any(term.lower() in text for term in inputs["must_not_include_any"])
