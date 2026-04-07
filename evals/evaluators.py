from __future__ import annotations

from typing import Any


def _get_text(outputs: dict[str, Any]) -> str:
    text = outputs.get("output", "")
    return text if isinstance(text, str) else str(text)


def asks_for_customer_id(inputs: dict, outputs: dict, reference_outputs=None) -> dict:
    expected = inputs.get("expected_behavior")
    if expected != "asks_for_customer_id":
        return {"key": "asks_for_customer_id", "score": 1, "comment": "Not applicable"}

    text = _get_text(outputs).lower()
    ok = ("customer id" in text) or ("id" in text and "customer" in text)
    return {
        "key": "asks_for_customer_id",
        "score": 1 if ok else 0,
        "comment": "Agent should ask for customer ID before account lookup.",
    }


def graceful_scope_limit(inputs: dict, outputs: dict, reference_outputs=None) -> dict:
    expected = inputs.get("expected_behavior")
    if expected != "graceful_scope_limit":
        return {"key": "graceful_scope_limit", "score": 1, "comment": "Not applicable"}

    text = _get_text(outputs).lower()
    ok = any(
        phrase in text
        for phrase in [
            "music",
            "catalog",
            "customer account",
            "customer id",
            "i can help with",
            "i can help you with",
        ]
    )
    return {
        "key": "graceful_scope_limit",
        "score": 1 if ok else 0,
        "comment": "Agent should gracefully state its supported scope.",
    }


def contains_expected_any(inputs: dict, outputs: dict, reference_outputs=None) -> dict:
    expected_terms = inputs.get("must_include_any", [])
    if not expected_terms:
        return {"key": "contains_expected_any", "score": 1, "comment": "No required terms"}

    text = _get_text(outputs).lower()
    ok = any(term.lower() in text for term in expected_terms)
    return {
        "key": "contains_expected_any",
        "score": 1 if ok else 0,
        "comment": f"Expected one of: {expected_terms}",
    }


def avoids_forbidden_terms(inputs: dict, outputs: dict, reference_outputs=None) -> dict:
    forbidden_terms = inputs.get("must_not_include_any", [])
    if not forbidden_terms:
        return {"key": "avoids_forbidden_terms", "score": 1, "comment": "No forbidden terms"}

    text = _get_text(outputs).lower()
    offenders = [term for term in forbidden_terms if term.lower() in text]
    ok = len(offenders) == 0
    return {
        "key": "avoids_forbidden_terms",
        "score": 1 if ok else 0,
        "comment": "Forbidden terms found: " + ", ".join(offenders) if offenders else "None",
    }


def returns_nonempty_answer(inputs: dict, outputs: dict, reference_outputs=None) -> dict:
    text = _get_text(outputs).strip()
    ok = len(text) > 0
    return {
        "key": "returns_nonempty_answer",
        "score": 1 if ok else 0,
        "comment": "Agent should return a non-empty answer.",
    }
