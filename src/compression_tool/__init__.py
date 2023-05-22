"""A text compression tool."""

from .compression import (
    Compress,
    HuffmanTree,
    HuffmanInternalNode,
    HuffmanLeafNode,
    decompress_file,
)

__all__ = [
    "Compress",
    "HuffmanTree",
    "HuffmanInternalNode",
    "HuffmanLeafNode",
    "decompress_file",
]
