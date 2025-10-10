import json

import pytest

from ai_recruiter.model import LlamaRecruiterModel, RecruiterConfig


class DummyChatLlama:
    def __init__(self):
        self.messages = None
        self.kwargs = None

    def create_chat_completion(self, **kwargs):
        self.messages = kwargs["messages"]
        self.kwargs = kwargs
        payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "overall_match": 76,
                                "summary": "Good alignment with NLP focus",
                                "verdict": {"label": "consider", "rationale": "LLM skills evident"},
                                "breakdown": [
                                    {"criterion": "core skills", "score": 80, "evidence": "Python, LLM"},
                                    {"criterion": "soft skills", "score": 70, "evidence": "Led teams"},
                                ],
                            }
                        )
                    }
                }
            ]
        }
        return payload


def test_score_resume_parses_response(sample_resume, sample_jd):
    config = RecruiterConfig(criteria=("core skills", "soft skills"))
    llama = DummyChatLlama()
    model = LlamaRecruiterModel(config=config, llama_client=llama)

    result = model.score_resume(sample_resume, sample_jd)

    assert result.overall == pytest.approx(76)
    assert result.verdict.label == "consider"
    assert len(result.breakdown) == 2
    assert llama.messages[0]["role"] == "system"
    assert "core skills" in llama.messages[0]["content"]
    assert "<resume>" in llama.messages[1]["content"]
