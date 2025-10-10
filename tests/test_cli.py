import json

import pytest

from ai_recruiter import cli
from ai_recruiter.scoring import MatchScore, ScoreBreakdown, ScoreVerdict


class StubMatch(MatchScore):
    def __init__(self, overall=88.0):
        super().__init__(
            overall=overall,
            summary="Strong overlap",
            verdict=ScoreVerdict(label="strong", rationale="Matches most requirements"),
            breakdown=[
                ScoreBreakdown(criterion="core skills", score=90, evidence="Python, NLP"),
                ScoreBreakdown(criterion="soft skills", score=85, evidence="Led teams"),
            ],
            raw_response="{}",
        )


class DummyModel:
    instances = []

    def __init__(self, *_, **__):
        self.calls = []
        DummyModel.instances.append(self)

    def score_resume(self, resume_text, jd_text):
        self.calls.append((resume_text, jd_text))
        return StubMatch()


@pytest.fixture(autouse=True)
def patch_model(monkeypatch):
    DummyModel.instances.clear()
    monkeypatch.setattr(cli, "LlamaRecruiterModel", DummyModel)
    return DummyModel


def test_cli_outputs_text(tmp_path, sample_resume, sample_jd, capsys):
    cv_path = tmp_path / "cv.txt"
    jd_path = tmp_path / "jd.txt"
    cv_path.write_text(sample_resume)
    jd_path.write_text(sample_jd)

    exit_code = cli.main([
        "--cv",
        str(cv_path),
        "--jd",
        str(jd_path),
        "--model-path",
        "dummy.gguf",
        "--format",
        "text",
    ])

    captured = capsys.readouterr().out
    assert exit_code == 0
    assert "Overall Match" in captured
    assert "Strong overlap" in captured


def test_cli_outputs_json(tmp_path, sample_resume, sample_jd, capsys):
    cv_path = tmp_path / "cv.txt"
    jd_path = tmp_path / "jd.txt"
    cv_path.write_text(sample_resume)
    jd_path.write_text(sample_jd)

    exit_code = cli.main([
        "--cv",
        str(cv_path),
        "--jd",
        str(jd_path),
        "--model-path",
        "dummy.gguf",
        "--format",
        "json",
    ])

    captured = capsys.readouterr().out
    payload = json.loads(captured)
    assert exit_code == 0
    assert payload[0]["overall"] == pytest.approx(88.0)
    assert payload[0]["verdict"]["label"] == "strong"


def test_cli_supports_curated_profiles(capsys):
    exit_code = cli.main(
        [
            "--jd-profile",
            "principal_llm_platform_architect",
            "--resume-profile",
            "mission_control_ml",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr().out
    payload = json.loads(captured)

    assert exit_code == 0
    assert payload[0]["resume"] == "profile:mission_control_ml"
    # Ensure the curated content made it into the model call for stronger prompts
    resume_prompt, jd_prompt = DummyModel.instances[-1].calls[-1]
    assert "Amara Chen" in resume_prompt
    assert "Principal Generative AI Platform Architect" in jd_prompt


def test_cli_requires_at_least_one_resume(tmp_path, sample_jd):
    jd_path = tmp_path / "jd.txt"
    jd_path.write_text(sample_jd)

    with pytest.raises(SystemExit):
        cli.main(["--jd", str(jd_path)])
