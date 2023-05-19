"""Imitate wc."""

from pathlib import Path
import os
import re
import argparse


def wc_bytes(file_path: str | Path) -> int:
    """Return the file size."""
    return os.path.getsize(file_path)


def wc_lines(file_path: str | Path) -> int:
    """Return the line count."""
    with open(file_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines


def wc_words(file_path: str | Path) -> int:
    """Return the word count."""
    with open(file_path, encoding="utf8") as f:
        num_words = len(re.findall(r"[^\s]+", f.read()))
    return num_words


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", action="store", nargs="+")
    parser.add_argument("-c", "--bytes", action="store_true")
    parser.add_argument("-l", "--lines", action="store_true")
    parser.add_argument("-w", "--words", action="store_true")
    args = parser.parse_args()
    for file_path in args.file_path:
        if args.bytes:
            print(f"{wc_bytes(file_path)} {file_path}")
        if args.lines:
            print(f"{wc_lines(file_path)} {file_path}")
        if args.words:
            print(f"{wc_words(file_path)} {file_path}")
