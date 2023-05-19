"""Tests for wc."""

from pathlib import Path
import wc


def test_wc_bytes(sample_txt: Path) -> None:
    """Test that wc returns number of bytes in a file."""
    expected = 341836
    result = wc.wc(sample_txt)
    assert expected == result
