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


def test_huffman_frequency_to_tree(
    compression_sample_frequency_to_tree: tuple[
        Counter[str], compression_tool.HuffmanTree
    ]
) -> None:
    """Test the construction of a Huffman encoding tree from given frequency data."""
    data, expected_tree = compression_sample_frequency_to_tree
    calculated_tree = compression_tool.HuffmanTree.from_frequency(data)
    assert calculated_tree == expected_tree


def test_huffman_tree_to_prefix_table(
    compression_sample_tree_to_prefix_table: tuple[
        compression_tool.HuffmanTree, dict[str, int]
    ]
) -> None:
    """Test the construction of the prefix table from a given Huffman tree."""
    tree, expected_table = compression_sample_tree_to_prefix_table
    calculated_table = tree.generate_table()
    assert calculated_table == expected_table


def test_huffman_tree_to_header(
    compression_sample_tree_to_header: tuple[compression_tool.HuffmanTree, bytes]
) -> None:
    """Test the construction of the file header for compression."""
    tree, expected_header = compression_sample_tree_to_header
    calculated_header = tree.generate_header()
    assert calculated_header == expected_header


def test_huffman_header_to_prefix_table(
    compression_sample_header_to_prefix_table: tuple[bytes, dict[str, str]]
) -> None:
    """Test the reconstruction of the prefix table from the file header."""
    header, expected_table = compression_sample_header_to_prefix_table
    calculated_table, _ = compression_tool.HuffmanTree.decode_header(header)
    assert calculated_table == expected_table


def test_huffman_encoding(
    compression_sample_txt: tuple[Path, dict[str, int]], tmp_path: Path
) -> None:
    """Test that encoding and decoding a text file results in the same contents."""
    sample_path, _ = compression_sample_txt
    file_path = tmp_path / "compressed.bin"
    contents = compression_tool.Compress(sample_path)
    contents.compress(file_path)
    decompressed_contents = compression_tool.decompress_file(file_path)
    assert decompressed_contents == contents.contents
