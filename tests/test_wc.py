"""Tests for wc."""

import os
import pytest
from conftest import WCFixture
import wc


def test_entrypoint() -> None:
    """Test that the command is recognised."""
    exit_status = os.system("ccwc --help")
    assert exit_status == 0


def test_wc_bytes(wc_sample_txt: WCFixture) -> None:
    """Test that wc returns number of bytes in a file."""
    result = wc.WCFile(wc_sample_txt.path).bytes
    assert result == wc_sample_txt.bytes


def test_wc_bytes_cli(
    capfd: pytest.CaptureFixture[str], wc_sample_txt: WCFixture
) -> None:
    """Test wc -c."""
    exit_status = os.system(f"ccwc -c {wc_sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{wc_sample_txt.bytes}\t{wc_sample_txt.path}"


def test_wc_lines(wc_sample_txt: WCFixture) -> None:
    """Test that wc returns the number of lines in a file."""
    result = wc.WCFile(wc_sample_txt.path).lines
    assert result == wc_sample_txt.lines


def test_wc_lines_cli(
    capfd: pytest.CaptureFixture[str], wc_sample_txt: WCFixture
) -> None:
    """Test wc -l."""
    exit_status = os.system(f"ccwc -l {wc_sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{wc_sample_txt.lines}\t{wc_sample_txt.path}"


def test_wc_words(wc_sample_txt: WCFixture) -> None:
    """Test that wc returns the number of words in a file."""
    result = wc.WCFile(wc_sample_txt.path).words
    assert result == wc_sample_txt.words


def test_wc_words_cli(
    capfd: pytest.CaptureFixture[str], wc_sample_txt: WCFixture
) -> None:
    """Test wc -w."""
    exit_status = os.system(f"ccwc -w {wc_sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{wc_sample_txt.words}\t{wc_sample_txt.path}"


def test_wc_chars(wc_sample_txt: WCFixture) -> None:
    """Test that wc returns the number of characters in a file."""
    result = wc.WCFile(wc_sample_txt.path).chars
    assert result == wc_sample_txt.chars


def test_wc_chars_cli(
    capfd: pytest.CaptureFixture[str], wc_sample_txt: WCFixture
) -> None:
    """Test wc -m."""
    exit_status = os.system(f"ccwc -m {wc_sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{wc_sample_txt.chars}\t{wc_sample_txt.path}"


def test_wc_no_args(
    capfd: pytest.CaptureFixture[str], wc_sample_txt: WCFixture
) -> None:
    """Test wc without additional arguments."""
    exit_status = os.system(f"ccwc {wc_sample_txt.path}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert (
        captured.out.rstrip()
        == f"{wc_sample_txt.lines}\t{wc_sample_txt.words}\t{wc_sample_txt.bytes}\t{wc_sample_txt.path}"
    )


def test_wc_stdin(capfd: pytest.CaptureFixture[str], wc_sample_txt: WCFixture) -> None:
    """Test wc reading from stdin."""
    exit_status = os.system(f"type {wc_sample_txt.path} | ccwc -l")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == f"{wc_sample_txt.lines}"
