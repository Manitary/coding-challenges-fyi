"""Tests for wc."""

from pathlib import Path
from collections import Counter
import pytest
import compression_tool


def test_invalid_file(compression_sample_binary: Path) -> None:
    """Raise an exception when trying to open an invalid file."""
    with pytest.raises(UnicodeDecodeError):
        compression_tool.Compress(compression_sample_binary)


def test_frequency(compression_sample_txt: tuple[Path, dict[str, int]]) -> None:
    """Test the frequency of given characters."""
    file_path, data = compression_sample_txt
    compress = compression_tool.Compress(file_path)
    for character, frequency in data.items():
        assert compress.frequency(character) == frequency


def test_tree_huffman(
    compression_sample_frequency: tuple[Counter[str], compression_tool.HuffmanTree]
) -> None:
    """Test the construction of a Huffman encoding tree from given frequency data."""
    data, expected_tree = compression_sample_frequency
    calculated_tree = compression_tool.HuffmanTree.from_frequency(data)
    assert calculated_tree == expected_tree
