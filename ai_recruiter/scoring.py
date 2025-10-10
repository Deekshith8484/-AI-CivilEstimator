"""Utilities for parsing and representing LLM based candidate scores."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ScoreBreakdown:
    criterion: str
    score: float
    evidence: str


@dataclass
class ScoreVerdict:
    label: str
    rationale: str


@dataclass
class MatchScore:
    overall: float
    summary: str
    verdict: ScoreVerdict
    breakdown: List[ScoreBreakdown]
    raw_response: str


def parse_llm_json(raw_text: str) -> Dict[str, Any]:
    """Parse the JSON body from a llama response, handling stray text."""
    if not raw_text:
        raise ValueError("Empty response from language model")

    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object could be located in response: {raw_text!r}")

    snippet = raw_text[start : end + 1]
    try:
        data = json.loads(snippet)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse llama JSON payload: {raw_text!r}") from exc

    return data
