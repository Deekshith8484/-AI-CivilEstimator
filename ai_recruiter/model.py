"""Interfaces with a local LLaMA model to score resumes against job descriptions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

from .scoring import MatchScore, ScoreBreakdown, ScoreVerdict, parse_llm_json


DEFAULT_MODEL_PATH = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"


@dataclass
class RecruiterConfig:
    """Configuration describing how to evaluate candidates."""

    model_path: str = DEFAULT_MODEL_PATH
    criteria: Sequence[str] = field(
        default_factory=lambda: (
            "core skills",
            "experience alignment",
            "domain knowledge",
            "soft skills",
            "impact and achievements",
        )
    )
    temperature: float = 0.05
    max_tokens: int = 512
    context_window: int = 4096
    threads: Optional[int] = None


class LlamaRecruiterModel:
    """Wrapper around `llama_cpp.Llama` that produces structured match scores."""

    def __init__(self, config: RecruiterConfig | None = None, *, llama_client=None):
        self.config = config or RecruiterConfig()
        self._llama = llama_client or self._load_llama()

    def _load_llama(self):
        try:
            from llama_cpp import Llama  # type: ignore
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise ImportError(
                "llama_cpp is required to use LlamaRecruiterModel. Install llama-cpp-python."
            ) from exc

        kwargs = {
            "model_path": self.config.model_path,
            "n_ctx": self.config.context_window,
            "temperature": self.config.temperature,
        }
        if self.config.threads is not None:
            kwargs["n_threads"] = self.config.threads

        return Llama(**kwargs)

    def _build_system_prompt(self) -> str:
        criteria_lines = "\n".join(f"- {criterion}" for criterion in self.config.criteria)
        return (
            "You are an expert technical recruiter."
            " Evaluate how well a candidate matches the provided job description."
            " Always respond with JSON using this schema:\n"
            "{\n"
            "  \"overall_match\": number (0-100),\n"
            "  \"summary\": short plain text,\n"
            "  \"verdict\": {\n"
            "    \"label\": one of ['reject','consider','strong'],\n"
            "    \"rationale\": plain text explanation\n"
            "  },\n"
            "  \"breakdown\": [\n"
            "    {\n"
            "      \"criterion\": string from the configured criteria list,\n"
            "      \"score\": number (0-100),\n"
            "      \"evidence\": plain text citing resume snippets\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "If information is missing, explain the uncertainty rather than hallucinating."
            " The criteria to consider are:\n"
            f"{criteria_lines}\n"
            "Ensure JSON is valid and parsable without extra commentary."
        )

    def _build_user_prompt(self, resume_text: str, job_description: str) -> str:
        return (
            "<job_description>\n"
            f"{job_description.strip()}\n"
            "</job_description>\n"
            "<resume>\n"
            f"{resume_text.strip()}\n"
            "</resume>\n"
            "Assess the match focusing on the configured criteria."
        )

    def score_resume(self, resume_text: str, job_description: str) -> MatchScore:
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": self._build_user_prompt(resume_text, job_description)},
        ]

        response_text = self._invoke_llm(messages)
        parsed = parse_llm_json(response_text)

        breakdown = [
            ScoreBreakdown(
                criterion=item["criterion"],
                score=float(item["score"]),
                evidence=item.get("evidence", ""),
            )
            for item in parsed.get("breakdown", [])
        ]

        verdict_data = parsed.get("verdict", {})
        verdict = ScoreVerdict(
            label=verdict_data.get("label", "consider"),
            rationale=verdict_data.get("rationale", ""),
        )

        return MatchScore(
            overall=float(parsed.get("overall_match", 0.0)),
            summary=parsed.get("summary", ""),
            verdict=verdict,
            breakdown=breakdown,
            raw_response=response_text,
        )

    def _invoke_llm(self, messages: Iterable[dict]) -> str:
        llama = self._llama
        if hasattr(llama, "create_chat_completion"):
            output = llama.create_chat_completion(  # type: ignore[attr-defined]
                messages=list(messages),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            return self._extract_message(output)

        if callable(llama):  # fallback for completion style APIs
            output = llama(
                prompt=self._format_legacy_prompt(messages),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            return self._extract_legacy(output)

        raise TypeError("Unsupported llama client provided; must implement chat completion or be callable.")

    def _format_legacy_prompt(self, messages: Sequence[dict]) -> str:
        return "\n".join(f"[{m['role'].upper()}]\n{m['content']}" for m in messages)

    @staticmethod
    def _extract_message(output: dict) -> str:
        try:
            return output["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:  # pragma: no cover - defensive path
            raise ValueError(f"Unexpected chat completion payload: {output!r}") from exc

    @staticmethod
    def _extract_legacy(output: dict) -> str:
        try:
            text = output["choices"][0]["text"].strip()
        except (KeyError, IndexError, TypeError) as exc:  # pragma: no cover - defensive path
            raise ValueError(f"Unexpected completion payload: {output!r}") from exc
        return text
