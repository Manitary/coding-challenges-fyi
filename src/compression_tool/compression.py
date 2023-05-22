"""A text compression tool."""

from pathlib import Path


class Compress:
    """Compress text files."""

    def __init__(self, file_path: Path | str) -> None:
        self._path = file_path
        with open(file_path, encoding="utf8") as f:
            self._contents = f.read()
