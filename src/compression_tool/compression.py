"""A text compression tool."""

from __future__ import annotations
from pathlib import Path
from collections import Counter, deque
from dataclasses import dataclass
from typing import Self, Sequence


class Compress:
    """Compress text files."""

    def __init__(self, file_path: Path | str) -> None:
        self._path = file_path
        with open(file_path, encoding="utf8") as f:
            self._contents = f.read()
        self._frequency = Counter(self._contents)

    def frequency(self, char: str) -> int:
        """Return the frequency of a character."""
        return self._frequency[char]


@dataclass
class HuffmanNode:
    """Generic node of a Huffman tree."""

    weight: int


@dataclass
class HuffmanLeafNode(HuffmanNode):
    """Leaf node of a Huffman tree."""

    value: str


@dataclass
class HuffmanInternalNode(HuffmanNode):
    """Non-leaf node of a Huffman tree."""

    left: HuffmanNode | None = None
    right: HuffmanNode | None = None


@dataclass
class HuffmanTree:
    """A Huffman tree."""

    root: HuffmanNode | None = None

    @property
    def weight(self) -> int:
        """Weight of the tree, stored in the root."""
        if self.root is None:
            return 0
        return self.root.weight

    @classmethod
    def from_frequency(cls, frequency: Counter[str]) -> Self:
        """Build a Huffman tree from a collection of character frequencies."""
        nodes = [
            HuffmanTree(HuffmanLeafNode(weight=count, value=character))
            for character, count in frequency.items()
        ]
        if not nodes:
            return HuffmanTree()
        while len(nodes) > 1:
            nodes = HuffmanTree.huffman_tree_step(nodes)
        return nodes[0]

    @staticmethod
    def huffman_tree_step(
        elements: Sequence[HuffmanTree],
    ) -> list[HuffmanTree]:
        """A single step of the Huffman tree construction.

        Take a list of nodes or partial Huffman trees, and combine
        the two with lowest weight."""
        elements = sorted(list(elements), key=lambda x: x.weight)
        new_element = HuffmanTree.huffman_merge(*elements[:2])
        elements = elements[2:] + [new_element]
        return elements

    @staticmethod
    def huffman_merge(
        element_left: HuffmanTree, element_right: HuffmanTree
    ) -> HuffmanTree:
        """Combine two Huffman trees."""
        combined_weight = element_left.weight + element_right.weight
        root = HuffmanInternalNode(
            weight=combined_weight, left=element_left.root, right=element_right.root
        )
        tree = HuffmanTree(root=root)
        return tree

    def generate_table(self) -> dict[str, str]:
        """Generate the prefix-code table from the tree."""
        table: dict[str, str] = {}
        if self.root is None:
            return table
        queue: deque[tuple[HuffmanNode | None, str]] = deque([(self.root, "")])
        while queue:
            node, prefix = queue.popleft()
            if isinstance(node, HuffmanLeafNode):
                table[node.value] = prefix
            elif isinstance(node, HuffmanInternalNode):
                queue.append((node.left, f"{prefix}0"))
                queue.append((node.right, f"{prefix}1"))
        return table

    def generate_header(self) -> bytes:
        """Generate the file header from the tree.

        Format:
        - 4 bytes for the length of the tree encoding
        - 4 bytes for the length of the characters encoding
        - tree encoding
        - characters encoding"""
        header = bytearray()
        tree, char = self.encode_tree()
        tree_encoded = encode_binary_string(tree)
        header.extend(len(tree_encoded).to_bytes(4))
        char_encoded = char.encode()
        header.extend(len(char_encoded).to_bytes(4))
        header.extend(tree_encoded)
        header.extend(char_encoded)
        return bytes(header)

    def encode_tree(self) -> tuple[str, str]:
        """Return a binary encoding of the tree.

        The tree is traversed BF, left-to-right;
        0 = leaf, 1 = internal node."""
        tree_encoding = ""
        char_encoding = ""
        queue: deque[HuffmanNode | None] = deque([self.root])
        while queue:
            node = queue.popleft()
            if isinstance(node, HuffmanInternalNode):
                queue.extend([node.left, node.right])
                tree_encoding += "1"
            elif isinstance(node, HuffmanLeafNode):
                tree_encoding += "0"
                char_encoding += node.value
        return tree_encoding, char_encoding

    @staticmethod
    def decode_header(header: bytes) -> dict[str, str]:
        """Return the prefix table obtained by decoding the header of a compressed file."""


def encode_binary_string(string: str) -> bytes:
    """Represent a string of 0/1 into bytes."""
    num = int(string, 2)
    return num.to_bytes((num.bit_length() + 7) // 8)
