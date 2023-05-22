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

    @property
    def contents(self) -> str:
        """Return the contents of the file."""
        return self._contents

    def frequency(self, char: str) -> int:
        """Return the frequency of a character."""
        return self._frequency[char]

    def compress(self, path: str | Path) -> None:
        """Compress the contents into a file."""
        tree = HuffmanTree.from_frequency(self._frequency)
        encoding_table = tree.generate_table()
        header = tree.generate_header()
        encoded_contents = "".join(encoding_table[char] for char in self._contents)
        if pad_length := len(encoded_contents) % 8:
            encoded_contents += "0" * pad_length
        with open(path, "wb") as f:
            f.write(header)
            for i in range(0, len(encoded_contents), 8):
                f.write(int(encoded_contents[i : i + 8], 2).to_bytes())


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


class HuffmanDecodeError(ValueError):
    """Raised when the header data cannot be decoded into a valid Huffman tree."""


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
            HuffmanTree(root=HuffmanLeafNode(weight=count, value=character))
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

    @classmethod
    def decoded_from_header(cls, encoded_tree: str, characters: str) -> Self:
        """Return an Huffman tree with no weights from encoded data."""
        if len(encoded_tree) != 2 * len(characters) - 1:
            raise HuffmanDecodeError("The number of characters don't fit the tree.")
        if not encoded_tree:
            return HuffmanTree()
        if len(encoded_tree) == 1:
            if encoded_tree == "1":
                raise HuffmanDecodeError(
                    "The root of the tree is an intermediate node has no children."
                )
            return HuffmanTree(root=HuffmanLeafNode(weight=0, value=characters))
        if encoded_tree[0] == "0":
            raise HuffmanDecodeError(
                "The root of the tree is a leaf node with children."
            )
        root = HuffmanInternalNode(weight=0)
        tree = HuffmanTree(root=root)
        nodes_to_process: deque[HuffmanInternalNode] = deque([root])
        i = 0
        for char in encoded_tree[1:]:
            if char == "0":
                new_node = HuffmanLeafNode(weight=0, value=characters[i])
                i += 1
            else:
                new_node = HuffmanInternalNode(weight=0)
            if nodes_to_process[0].left is None:
                nodes_to_process[0].left = new_node
            else:
                nodes_to_process.popleft().right = new_node
            if isinstance(new_node, HuffmanInternalNode):
                nodes_to_process.append(new_node)
        if nodes_to_process:
            raise HuffmanDecodeError("There are intermediate nodes with no children.")
        return tree

    @staticmethod
    def decode_header(file_contents: bytes) -> tuple[dict[str, str], int]:
        """Return the prefix table obtained by decoding the header of a compressed file."""
        tree_length = int.from_bytes(file_contents[:4])
        encoding_length = int.from_bytes(file_contents[4:8])
        contents_index = 8 + tree_length + encoding_length
        tree_data = bin(int.from_bytes(file_contents[8 : 8 + tree_length]))[2:]
        characters = file_contents[8 + tree_length : contents_index].decode()
        tree = HuffmanTree.decoded_from_header(
            encoded_tree=tree_data, characters=characters
        )
        return tree.generate_table(), contents_index

    @staticmethod
    def decode_file_contents(file_contents: bytes) -> str:
        """Decode a file."""
        prefix_table, idx = HuffmanTree.decode_header(file_contents)
        prefix_table = {value: key for key, value in prefix_table.items()}
        encoded_text = "".join(
            bin(byte)[2:].rjust(8, "0") for byte in file_contents[idx:]
        )
        decoded_text = ""
        char = ""
        for bit in encoded_text:
            char += bit
            if char in prefix_table:
                decoded_text += prefix_table[char]
                char = ""
        return decoded_text


def encode_binary_string(string: str) -> bytes:
    """Represent a string of 0/1 into bytes."""
    num = int(string, 2)
    return num.to_bytes((num.bit_length() + 7) // 8)


def decompress_file(file_path: str | Path) -> str:
    """Return the contents of a file that was compressed with Huffman encoding."""
    with open(file_path, "rb") as f:
        contents = f.read()
    return HuffmanTree.decode_file_contents(contents)
