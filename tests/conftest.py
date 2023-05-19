"""Test fixtures."""

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Generator
import pytest

ASSET_ROOT = Path(__file__).parent.resolve() / "assets"


@dataclass
class WCFixture:
    """Hold data used for testing wc."""

    name: str
    path: Path
    bytes: int
    lines: int
    words: int


@pytest.fixture
def sample_txt(tmp_path: Path) -> Generator[WCFixture, None, None]:
    """Yield a text file data used to test wc."""
    file_name = "test.txt"
    copy_path = shutil.copy2(ASSET_ROOT / file_name, tmp_path / file_name)
    fixture_data = WCFixture(
        name=file_name, path=copy_path, bytes=341836, lines=7137, words=58159
    )
    yield fixture_data
