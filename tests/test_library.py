from ai_recruiter import library


def test_render_job_profile_contains_sections():
    text = library.render_job_profile("principal_llm_platform_architect")
    assert "Core Responsibilities" in text
    assert "Minimum Requirements" in text
    assert "Preferred Experience" in text
    assert "Principal Generative AI Platform Architect" in text


def test_render_resume_profile_includes_name():
    text = library.render_resume_profile("mission_control_ml")
    assert "Dr. Amara Chen" in text
    assert "Experience:" in text


def test_default_criteria_matches_job():
    criteria = library.default_criteria_for_job("principal_llm_platform_architect")
    assert "llm platform architecture" in criteria
    assert len(criteria) == 5
