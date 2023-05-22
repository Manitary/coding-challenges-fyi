"""A text compression tool."""

from pathlib import Path
from collections import Counter


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


class HuffmanTree:
    ...


class HuffmanLeafNode:
    ...


class HuffmanInternalNode:
    ...
