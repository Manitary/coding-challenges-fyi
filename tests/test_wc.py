"""Tests for wc."""

import os
from pathlib import Path
import wc


def test_entrypoint() -> None:
    """Test that the command runs."""
    exit_status = os.system("ccwc --help")
    assert exit_status == 0


def test_wc_bytes(sample_txt: Path) -> None:
    """Test that wc returns number of bytes in a file."""
    expected = 341836
    result = wc.wc(sample_txt)
    assert expected == result


def test_wc_bytes_cli(capfd, sample_txt: Path) -> None:
    """Test wc -c."""
    exit_status = os.system(f"ccwc -c {sample_txt}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.strip() == "341836"
