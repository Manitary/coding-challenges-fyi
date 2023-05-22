"""Test fixtures."""

from __future__ import annotations
import shutil
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Generator
import glob
import pytest

ASSET_ROOT = Path(__file__).parent.resolve() / "assets"


class JSONTestFile:
    """Hold information about a JSON test file.

    Include:
    - file path (Path)
    - file name (str)
    - result (bool) expected from the test (True/False for pass/fail).

    The file name must match one of these formats:
    - failX, for failing tests
    - passX, for passing tests
    where X is any number of digits.
    """

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._file_name = file_path.stem
        if re.match(r"fail\d+", self._file_name):
            self.result = False
        elif re.match(r"pass\d+", self._file_name):
            self.result = True
        else:
            raise ValueError("The file name does not match the required format.")

    @property
    def path(self) -> Path:
        """Return the file path."""
        return self._file_path

    @property
    def name(self) -> str:
        """Return the file name."""
        return self._file_name

    @staticmethod
    def get_stem(json_test: JSONTestFile) -> str:
        """Return the file name from path."""
        return json_test.name


JSON_ASSETS = [
    JSONTestFile(Path(file_path))
    for file_path in glob.glob(f"{ASSET_ROOT / 'test_json'}/*.json")
]


@dataclass
class WCFixture:
    """Hold data used for testing wc."""

    name: str
    path: Path
    bytes: int
    lines: int
    words: int
    chars: int


@pytest.fixture
def wc_sample_txt(tmp_path: Path) -> Generator[WCFixture, None, None]:
    """Yield a text file data used to test wc."""
    file_name = "test.txt"
    copy_path = shutil.copy2(ASSET_ROOT / "test_wc" / file_name, tmp_path / file_name)
    fixture_data = WCFixture(
        name=file_name,
        path=copy_path,
        bytes=341836,
        lines=7137,
        words=58159,
        chars=331983,  # 339120 if \r\n are separate
    )
    yield fixture_data


@pytest.fixture(params=JSON_ASSETS, ids=JSONTestFile.get_stem)
def json_sample(request: pytest.FixtureRequest) -> Generator[JSONTestFile, None, None]:
    """Yield a sample JSON to test."""
    yield request.param


@pytest.fixture
def compression_sample_txt() -> Generator[tuple[Path, dict[str, int]], None, None]:
    """Yield a text file and associated data to test."""
    file_name = "test.txt"
    data = {"X": 333, "t": 223000}
    yield ASSET_ROOT / "test_compression" / file_name, data


@pytest.fixture
def compression_sample_binary() -> Generator[Path, None, None]:
    """Yield a binary file."""
    file_name = "test_invalid.bin"
    yield ASSET_ROOT / "test_compression" / file_name
