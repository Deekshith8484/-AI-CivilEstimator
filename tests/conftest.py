import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_resume():
    return """Jane Doe\nSenior Data Scientist\n- 8 years building NLP products\n- Led LLaMA model evaluations\n- Experience with Python, PyTorch, ML Ops"""


@pytest.fixture
def sample_jd():
    return """Looking for a Data Scientist with strong NLP background, experience deploying LLMs, and leadership skills."""
