"""Tests for wc."""

import os
import pytest
from conftest import WCFixture
import wc


def test_entrypoint() -> None:
    """Test that the command runs."""
    exit_status = os.system("ccwc --help")
    assert exit_status == 0


def test_wc_bytes(sample_txt: WCFixture) -> None:
    """Test that wc returns number of bytes in a file."""
    result = wc.wc_bytes(sample_txt.path)
    assert result == sample_txt.bytes


def test_wc_bytes_cli(capfd: pytest.CaptureFixture[str], sample_txt: WCFixture) -> None:
    """Test wc -c."""
    exit_status = os.system(f"ccwc -c {sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{sample_txt.bytes} {sample_txt.path}"


def test_wc_lines(sample_txt: WCFixture) -> None:
    """Test that wc returns the number of lines in a file."""
    result = wc.wc_lines(sample_txt.path)
    assert result == sample_txt.lines


def test_wc_lines_cli(capfd: pytest.CaptureFixture[str], sample_txt: WCFixture) -> None:
    """Test wc -l."""
    exit_status = os.system(f"ccwc -l {sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{sample_txt.lines} {sample_txt.path}"
