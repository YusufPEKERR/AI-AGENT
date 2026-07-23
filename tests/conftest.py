import os
import sys
from pathlib import Path
import pytest

# Ensure src/ is in sys.path for testing
src_path = Path(__file__).resolve().parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_workspace(tmp_path):
    d = tmp_path / "workspace"
    d.mkdir()
    return d
