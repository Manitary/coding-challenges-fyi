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


def test_wc_words(sample_txt: WCFixture) -> None:
    """Test that wc returns the number of words in a file."""
    result = wc.wc_words(sample_txt.path)
    assert result == sample_txt.words


def test_wc_words_cli(capfd: pytest.CaptureFixture[str], sample_txt: WCFixture) -> None:
    """Test wc -w."""
    exit_status = os.system(f"ccwc -w {sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{sample_txt.words} {sample_txt.path}"


def test_wc_chars(sample_txt: WCFixture) -> None:
    """Test that wc returns the number of characters in a file."""
    result = wc.wc_chars(sample_txt.path)
    assert result == sample_txt.chars


def test_wc_chars_cli(capfd: pytest.CaptureFixture[str], sample_txt: WCFixture) -> None:
    """Test wc -m."""
    exit_status = os.system(f"ccwc -m {sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{sample_txt.chars} {sample_txt.path}"


def test_wc_no_args(capfd: pytest.CaptureFixture[str], sample_txt: WCFixture) -> None:
    """Test wc without additional arguments."""
    exit_status = os.system(f"ccwc {sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert (
        captured.out.rstrip()
        == f"{sample_txt.lines}\t{sample_txt.words}\t{sample_txt.bytes}\t{sample_txt.path}"
    )


def test_wc_stdin(capfd: pytest.CaptureFixture[str], sample_txt: WCFixture) -> None:
    """Test wc reading from stdin."""
    exit_status = os.system(f"type {sample_txt.path} | ccwc -l")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{sample_txt.lines}"
