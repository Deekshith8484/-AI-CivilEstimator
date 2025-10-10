"""Curated job descriptions and resume profiles for the recruiter CLI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence


@dataclass(frozen=True)
class JobProfile:
    key: str
    title: str
    summary: str
    responsibilities: Sequence[str]
    requirements: Sequence[str]
    preferred: Sequence[str]
    evaluation_criteria: Sequence[str]

    def render(self) -> str:
        """Render the job description as a multi-section plain text document."""
        lines: List[str] = [self.title, "", self.summary, ""]
        if self.responsibilities:
            lines.append("Core Responsibilities:")
            lines.extend(f"- {item}" for item in self.responsibilities)
            lines.append("")
        if self.requirements:
            lines.append("Minimum Requirements:")
            lines.extend(f"- {item}" for item in self.requirements)
            lines.append("")
        if self.preferred:
            lines.append("Preferred Experience:")
            lines.extend(f"- {item}" for item in self.preferred)
            lines.append("")
        lines.append(
            "Screening guidance: Assess depth of applied research, ability to harden LLM systems, "
            "and evidence of shipping enterprise-grade AI capabilities."
        )
        return "\n".join(lines).strip()


@dataclass(frozen=True)
class ResumeProfile:
    key: str
    name: str
    headline: str
    summary: str
    experience: Sequence[str]
    projects: Sequence[str]
    skills: Sequence[str]

    def render(self) -> str:
        sections: List[str] = [self.name, self.headline, "", self.summary, ""]
        if self.experience:
            sections.append("Experience:")
            sections.extend(f"- {item}" for item in self.experience)
            sections.append("")
        if self.projects:
            sections.append("Key Projects:")
            sections.extend(f"- {item}" for item in self.projects)
            sections.append("")
        if self.skills:
            sections.append("Skills:")
            sections.extend(f"- {item}" for item in self.skills)
        return "\n".join(sections).strip()


JOB_PROFILES: Dict[str, JobProfile] = {
    "principal_llm_platform_architect": JobProfile(
        key="principal_llm_platform_architect",
        title="Principal Generative AI Platform Architect",
        summary=(
            "We're seeking a principal-level leader to design, harden, and scale an end-to-end platform for "
            "enterprise generative AI. The role spans technical strategy, hands-on experimentation, and "
            "cross-functional stakeholder management to deliver dependable LLM-powered experiences."
        ),
        responsibilities=(
            "Define the north-star roadmap for retrieval-augmented generation (RAG), agentic workflows, and safety guardrails.",
            "Lead architecture reviews covering model selection, quantization, inference acceleration, and observability.",
            "Partner with security, legal, and product teams to operationalize responsible AI and compliance controls.",
            "Mentor senior engineers and applied scientists; establish bar-raising engineering practices for LLM deployments.",
            "Own production readiness metrics (latency, hallucination rate, user satisfaction) and drive iterative improvements.",
            "Represent the program in executive reviews with quantitative updates on OKRs and business impact.",
        ),
        requirements=(
            "12+ years building ML platforms with at least 3 years on large language models in production.",
            "Deep fluency with transformer architectures, tokenizer internals, quantization trade-offs, and fine-tuning pipelines.",
            "Hands-on experience orchestrating vector search, feature stores, and evaluation harnesses at scale (>10M queries/month).",
            "Ability to write production-quality Python and build CI/CD workflows around GPU and CPU inference services.",
            "Proven track record leading cross-functional programs with security, compliance, and data governance stakeholders.",
        ),
        preferred=(
            "Published research or patents in retrieval-augmented generation, controllable generation, or alignment.",
            "Experience negotiating vendor contracts for foundation models and accelerator hardware.",
            "Background in reliability engineering for ML systems (SLO design, chaos testing, incident response).",
            "Advanced degree in Computer Science, Machine Learning, or related technical discipline.",
            "Fluency communicating complex architectural trade-offs to C-level audiences.",
        ),
        evaluation_criteria=(
            "llm platform architecture",
            "production leadership",
            "ml systems engineering",
            "responsible ai and governance",
            "stakeholder communication",
        ),
    ),
}


RESUME_PROFILES: Dict[str, ResumeProfile] = {
    "mission_control_ml": ResumeProfile(
        key="mission_control_ml",
        name="Dr. Amara Chen",
        headline="Principal Machine Learning Architect | Platform Strategy",
        summary=(
            "Architect with 14 years of experience building ML platforms across finance and SaaS. Recently led a 40-person "
            "initiative to launch a retrieval-augmented assistant serving 60k monthly users with <1.5% hallucination rate."
        ),
        experience=(
            "Director of AI Platforms, HyperNova Cloud (2020-2024): built global RAG platform on top of multi-region vector DB; "
            "governed latency SLO of 350ms p95 and availability of 99.95%.",
            "Head of Applied ML, Celestial Bank (2016-2020): established model risk controls, automated compliance evidence, "
            "and oversaw deployment of credit-decisioning transformers.",
            "Staff Machine Learning Engineer, Orbit Labs (2012-2016): shipped large-scale feature store, mentored 12 engineers.",
        ),
        projects=(
            "Implemented hybrid retrieval pipeline combining BM25, dense embeddings, and human feedback loops; cut escalation tickets by 47%.",
            "Negotiated $4.8M annual contract for accelerator hardware, coordinating cost/throughput modeling with finance.",
            "Designed incident response runbooks and on-call rotations specifically for generative AI systems.",
        ),
        skills=(
            "Python, Rust, CUDA",
            "LangChain, LlamaIndex, Ray Serve",
            "LLM fine-tuning (LoRA, QLoRA), quantization (GGUF, TensorRT)",
            "Vector databases (Pinecone, Weaviate, FAISS)",
            "Risk management, SOC2, ISO27001",
        ),
    ),
    "data_pipeline_specialist": ResumeProfile(
        key="data_pipeline_specialist",
        name="Miguel Torres",
        headline="Senior Data Engineer | Streaming Analytics",
        summary=(
            "Data engineer with 9 years of experience delivering streaming data pipelines and BI dashboards for retail and media clients."
        ),
        experience=(
            "Lead Data Engineer, StreamForge (2019-2024): designed Kafka-based ingestion for 5 TB/day, enforced data contracts.",
            "Data Engineer, Insight Analytics (2015-2019): built ETL jobs in Spark/Scala, managed Airflow deployments.",
        ),
        projects=(
            "Launched dbt metrics layer powering executive dashboards for 200 stakeholders.",
            "Implemented GDPR-compliant data retention automation across Redshift and S3."
        ),
        skills=(
            "Python, Scala, SQL",
            "Kafka, Spark, dbt, Airflow",
            "AWS (Glue, Redshift, EMR)",
            "Data governance, schema evolution",
        ),
    ),
}


def list_job_profiles() -> List[str]:
    return sorted(JOB_PROFILES.keys())


def list_resume_profiles() -> List[str]:
    return sorted(RESUME_PROFILES.keys())


def get_job_profile(key: str) -> JobProfile:
    try:
        return JOB_PROFILES[key]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"Unknown job profile '{key}'. Available profiles: {', '.join(list_job_profiles())}") from exc


def get_resume_profile(key: str) -> ResumeProfile:
    try:
        return RESUME_PROFILES[key]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(
            f"Unknown resume profile '{key}'. Available profiles: {', '.join(list_resume_profiles())}"
        ) from exc


def render_job_profile(key: str | JobProfile) -> str:
    profile = get_job_profile(key) if isinstance(key, str) else key
    return profile.render()


def render_resume_profile(key: str | ResumeProfile) -> str:
    profile = get_resume_profile(key) if isinstance(key, str) else key
    return profile.render()


def default_criteria_for_job(key: str | JobProfile) -> Sequence[str]:
    profile = get_job_profile(key) if isinstance(key, str) else key
    return profile.evaluation_criteria
