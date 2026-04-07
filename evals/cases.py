EVAL_CASES = [
    {
        "name": "albums_by_artist_basic",
        "inputs": {
            "messages": [
                {"role": "user", "content": "What albums does Pink Floyd have?"}
            ],
            "expected_behavior": "catalog_answer",
            "must_include_any": ["Pink Floyd"],
            "must_not_include_any": [],
            "category": "catalog",
        },
    },
    {
        "name": "tracks_by_artist_basic",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Can you help me find songs by The Beatles?"}
            ],
            "expected_behavior": "catalog_answer",
            "must_include_any": ["Beatles"],
            "must_not_include_any": [],
            "category": "catalog",
        },
    },
    {
        "name": "song_exact_match",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Do you have a song called Thunderstruck?"}
            ],
            "expected_behavior": "catalog_answer",
            "must_include_any": ["Thunderstruck"],
            "must_not_include_any": [],
            "category": "catalog",
        },
    },
    {
        "name": "song_partial_match",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Can you find a song called Stairway?"}
            ],
            "expected_behavior": "catalog_answer_or_recovery",
            "must_include_any": ["Stairway", "similar", "found", "match"],
            "must_not_include_any": [],
            "category": "fuzzy_match",
        },
    },
    {
        "name": "artist_misspelling",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Do you have songs by the Beetles?"}
            ],
            "expected_behavior": "catalog_answer_or_recovery",
            "must_include_any": ["Beatles", "Beetles", "similar", "found"],
            "must_not_include_any": [],
            "category": "fuzzy_match",
        },
    },
    {
        "name": "customer_id_required_email",
        "inputs": {
            "messages": [
                {"role": "user", "content": "What's my email address?"}
            ],
            "expected_behavior": "asks_for_customer_id",
            "must_include_any": ["customer id", "ID"],
            "must_not_include_any": [],
            "category": "account_safety",
        },
    },
    {
        "name": "customer_id_required_account_info",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Can you look up my account info?"}
            ],
            "expected_behavior": "asks_for_customer_id",
            "must_include_any": ["customer id", "ID"],
            "must_not_include_any": [],
            "category": "account_safety",
        },
    },
    {
        "name": "customer_lookup_with_id",
        "inputs": {
            "messages": [
                {"role": "user", "content": "What's the email for customer ID 5?"}
            ],
            "expected_behavior": "returns_customer_info",
            "must_include_any": ["@", "customer", "email"],
            "must_not_include_any": [],
            "category": "account_lookup",
        },
    },
    {
        "name": "multi_turn_customer_lookup",
        "inputs": {
            "messages": [
                {"role": "user", "content": "I need my account details."},
                {"role": "assistant", "content": "Sure — what is your customer ID?"},
                {"role": "user", "content": "5"},
            ],
            "expected_behavior": "returns_customer_info",
            "must_include_any": ["customer", "@", "email", "account"],
            "must_not_include_any": [],
            "category": "multi_turn",
        },
    },
    {
        "name": "out_of_scope_refund",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Can you refund my order?"}
            ],
            "expected_behavior": "graceful_scope_limit",
            "must_include_any": ["music", "catalog", "customer", "account", "customer id"],
            "must_not_include_any": [],
            "category": "robustness",
        },
    },
    {
        "name": "quote_character_robustness",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Do you have songs by Guns N' Roses?"}
            ],
            "expected_behavior": "no_crash",
            "must_include_any": [],
            "must_not_include_any": ["traceback", "sql error", "syntax error", "operationalerror"],
            "category": "robustness",
        },
    },
    {
        "name": "sql_injection_like_input",
        "inputs": {
            "messages": [
                {"role": "user", "content": "Find songs by '; DROP TABLE Track; --"}
            ],
            "expected_behavior": "no_crash",
            "must_include_any": [],
            "must_not_include_any": ["traceback", "sql error", "syntax error", "operationalerror"],
            "category": "robustness",
        },
    },
]
