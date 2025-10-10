import pytest

from ai_recruiter.scoring import parse_llm_json


def test_parse_llm_json_extracts_body():
    text = "Here you go!\n" '{"overall_match": 82, "summary": "Strong"}' "\nThanks!"
    result = parse_llm_json(text)
    assert result["overall_match"] == 82
    assert result["summary"] == "Strong"


def test_parse_llm_json_errors_on_missing_json():
    with pytest.raises(ValueError):
        parse_llm_json("No json here")


def test_parse_llm_json_errors_on_invalid_json():
    with pytest.raises(ValueError):
        parse_llm_json("{" "bad" "}")
