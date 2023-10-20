from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="session")
def schema_dir(test_dir) -> Path:
    return test_dir / ".." / "schemas"
