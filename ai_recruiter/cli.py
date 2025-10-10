"""Command line interface for the AI recruiter."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Sequence

from .library import (
    default_criteria_for_job,
    list_job_profiles,
    list_resume_profiles,
    render_job_profile,
    render_resume_profile,
)
from .model import LlamaRecruiterModel, RecruiterConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score resumes against a job description using a local LLaMA model.")
    parser.add_argument("--model-path", default=RecruiterConfig().model_path, help="Path to the GGUF model file for llama-cpp.")

    jd_group = parser.add_mutually_exclusive_group(required=True)
    jd_group.add_argument("--jd", dest="job_description", help="Path to the job description text file.")
    jd_group.add_argument(
        "--jd-profile",
        dest="jd_profile",
        choices=list_job_profiles(),
        help="Use a curated in-repo job description profile.",
    )

    parser.add_argument(
        "--cv",
        "--resume",
        dest="resumes",
        nargs="+",
        default=None,
        help="Path(s) to resume or CV text files.",
    )
    parser.add_argument(
        "--resume-profile",
        dest="resume_profiles",
        nargs="+",
        choices=list_resume_profiles(),
        help="Evaluate curated resume profiles from the in-repo library.",
    )
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format for the scores.")
    parser.add_argument("--temperature", type=float, default=RecruiterConfig().temperature, help="Sampling temperature for the model.")
    parser.add_argument("--max-tokens", type=int, default=RecruiterConfig().max_tokens, help="Maximum tokens to generate.")
    parser.add_argument("--threads", type=int, default=None, help="Number of CPU threads for llama-cpp.")
    parser.add_argument(
        "--criteria",
        nargs="*",
        default=None,
        help="Custom evaluation criteria to pass to the recruiter prompt.",
    )
    return parser


def load_text(path: str) -> str:
    content = Path(path).read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Input file {path} is empty")
    return content


def _format_text_output(filename: str, score) -> str:
    breakdown_lines = [
        f"  - {item.criterion}: {item.score:.1f} :: {item.evidence}" for item in score.breakdown
    ]
    breakdown = "\n".join(breakdown_lines) if breakdown_lines else "  (no breakdown available)"
    return (
        f"Results for {filename}:\n"
        f"Overall Match: {score.overall:.1f}\n"
        f"Verdict: {score.verdict.label} -> {score.verdict.rationale}\n"
        f"Summary: {score.summary}\n"
        f"Breakdown:\n{breakdown}\n"
    )


def evaluate_resumes(args: argparse.Namespace) -> List[dict]:
    resumes_from_files = args.resumes or []
    resumes_from_profiles = args.resume_profiles or []

    if not resumes_from_files and not resumes_from_profiles:
        raise ValueError("Provide at least one resume via --cv or --resume-profile.")

    job_profile = None
    if getattr(args, "jd_profile", None):
        job_profile = args.jd_profile
        jd_text = render_job_profile(job_profile)
    else:
        jd_text = load_text(args.job_description)

    criteria = tuple(args.criteria) if args.criteria else None
    if job_profile and criteria is None:
        criteria = tuple(default_criteria_for_job(job_profile))

    config = RecruiterConfig(
        model_path=args.model_path,
        criteria=criteria or RecruiterConfig().criteria,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        threads=args.threads,
    )
    recruiter = LlamaRecruiterModel(config=config)

    results = []
    for resume_path in resumes_from_files:
        resume_text = load_text(resume_path)
        match = recruiter.score_resume(resume_text, jd_text)
        results.append({"path": resume_path, "score": match})
    for resume_key in resumes_from_profiles:
        resume_text = render_resume_profile(resume_key)
        label = f"profile:{resume_key}"
        match = recruiter.score_resume(resume_text, jd_text)
        results.append({"path": label, "score": match})
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        results = evaluate_resumes(args)
    except Exception as exc:
        parser.error(str(exc))
        return 2

    if args.format == "json":
        payload = [
            {
                "resume": item["path"],
                "overall": item["score"].overall,
                "summary": item["score"].summary,
                "verdict": {
                    "label": item["score"].verdict.label,
                    "rationale": item["score"].verdict.rationale,
                },
                "breakdown": [
                    {
                        "criterion": breakdown.criterion,
                        "score": breakdown.score,
                        "evidence": breakdown.evidence,
                    }
                    for breakdown in item["score"].breakdown
                ],
            }
            for item in results
        ]
        print(json.dumps(payload, indent=2))
    else:
        for item in results:
            print(_format_text_output(item["path"], item["score"]))

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
