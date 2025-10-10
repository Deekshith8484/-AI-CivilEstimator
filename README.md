# AI Recruiter Scoring Toolkit

This project transforms resumes into actionable hiring insights using a local
LLaMA small model (TinyLlama or another compact GGUF build). Provide a job
description and one or more CVs, and the tool will prompt the LLM to produce a
structured JSON score that captures overall fit, a short summary, a verdict, and
criterion-by-criterion evidence. The repository now ships with a polished
"Principal Generative AI Platform Architect" job description plus two
contrasting resume profiles so you can demo the pipeline with a demanding JD
immediately.

The code is intentionally lightweight so it can run entirely offline with a
small model – perfect for HR teams or consultancies that want private screening
without sending data to third-party APIs.

## Features

- 🤖 **LLaMA-powered analysis** – run against a TinyLlama/Tinyllama GGUF model
  via [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python).
- 📊 **Structured scoring** – get normalized 0-100 scores with verdicts and
  textual evidence you can share with hiring managers.
- 🧩 **Custom criteria** – tailor the evaluation dimensions (skills, domain
  knowledge, leadership, etc.) for each hiring pipeline.
- 🛠️ **CLI ready** – score a batch of resumes against one JD from the command
  line and export JSON or human-readable text.

## Installation

1. Install dependencies (only `llama-cpp-python` is required at runtime):

   ```bash
   pip install llama-cpp-python
   ```

2. Download a small LLaMA-family GGUF model (for example the
   [`TinyLlama-1.1B-Chat-v1.0`](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
   Q4_K_M variant) and place it at `models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`,
   or pass the path explicitly to the CLI.
3. (Optional) Explore the built-in job description and resumes exposed via
   `ai_recruiter.library` to understand the expected input fidelity.

## Usage

Put your job description and resume(s) in plain-text files. Then run:

```bash
python -m ai_recruiter.cli \
  --jd path/to/job_description.txt \
  --cv path/to/resume1.txt path/to/resume2.txt \
  --model-path models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --format text
```

To produce JSON output (ideal for integrations):

```bash
python -m ai_recruiter.cli \
  --jd job.txt \
  --cv resume.txt \
  --format json
```

### Instant demo with curated profiles

Want to kick the tires without writing your own documents? Use the bundled job
description and curated resumes:

```bash
python -m ai_recruiter.cli \
  --jd-profile principal_llm_platform_architect \
  --resume-profile mission_control_ml data_pipeline_specialist \
  --format text
```

The first resume (`mission_control_ml`) is a tight match for the hard
requirements, while the second (`data_pipeline_specialist`) intentionally
focuses on adjacent data engineering skills to highlight contrasting scores and
rationales.

### Custom criteria

Override the default scoring dimensions by passing `--criteria`:

```bash
python -m ai_recruiter.cli \
  --jd data_scientist_jd.txt \
  --cv candidate.txt \
  --criteria "machine learning expertise" "llm deployment" "team leadership"
```

When a curated job profile is selected, the CLI automatically injects that
profile's evaluation criteria (`llm platform architecture`, `production
leadership`, etc.). Supplying `--criteria` overrides both the defaults and the
profile-specific guidance, giving you full control.

## Testing

Run the unit tests (which stub the llama backend) with:

```bash
pytest
```

## Notes on models

- This toolkit expects a small LLaMA-compatible GGUF model so it can run on
  commodity hardware.
- If you use a different model name or quantization, update `--model-path` or
  the `RecruiterConfig` default.
- The prompt instructs the LLM to return valid JSON. If the chosen model fails
  to comply, tighten the temperature or add sampling constraints.
