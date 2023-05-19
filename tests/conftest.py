"""Test fixtures."""

import shutil
from pathlib import Path
from typing import Generator
import pytest

ASSET_ROOT = Path(__file__).parent.resolve() / "assets"


@pytest.fixture
def sample_txt(
    tmp_path: Path, file_name: str = "test.txt"
) -> Generator[Path, None, None]:
    """Yield the path to a test txt file."""
    copy_path = shutil.copy2(ASSET_ROOT / file_name, tmp_path / file_name)
    yield copy_path
