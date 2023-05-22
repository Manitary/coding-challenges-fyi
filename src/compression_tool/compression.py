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
    def huffman_merge(element_1: HuffmanTree, element_2: HuffmanTree) -> HuffmanTree:
        """Combine two Huffman trees."""
        combined_weight = element_1.weight + element_2.weight
        tree = HuffmanTree()
        tree.root = HuffmanInternalNode(weight=combined_weight)
        tree.root.left, tree.root.right = element_1.root, element_2.root
        return tree

    def generate_table(self) -> dict[str, int]:
        """Generate the prefix-code table from the tree."""
        table: dict[str, int] = {}
        if self.root is None:
            return table
        queue: deque[tuple[HuffmanNode | None, int]] = deque([(self.root, 0)])
        while queue:
            node, prefix = queue.popleft()
            if isinstance(node, HuffmanLeafNode):
                table[node.value] = prefix
            elif isinstance(node, HuffmanInternalNode):
                queue.append((node.left, prefix << 1))
                queue.append((node.right, prefix << 1 | 1))
        return table
