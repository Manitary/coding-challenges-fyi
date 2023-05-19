"""Imitate wc."""

import sys
import abc
from dataclasses import dataclass
from pathlib import Path
import os
import re
import argparse


class WCObject(abc.ABC):
    """Collection of methods to display wc command output."""

    @property
    @abc.abstractmethod
    def bytes(self) -> int:
        """Return the size in bytes."""

    @property
    @abc.abstractmethod
    def lines(self) -> int:
        """Return the line count."""

    @property
    @abc.abstractmethod
    def words(self) -> int:
        """Return the word count."""

    @property
    @abc.abstractmethod
    def chars(self) -> int:
        """Return the character count."""

    @abc.abstractmethod
    def output_func(self, property_name: str) -> str:
        """Return the string printed when calling wc with the appropriate flag."""

    @property
    @abc.abstractmethod
    def output_no_args(self) -> str:
        """Return the string printed when calling wc without arguments."""


@dataclass
class WCFile(WCObject):
    """WCObject when wc is called against a file path."""

    file_path: str | Path

    @property
    def bytes(self) -> int:
        return os.path.getsize(self.file_path)

    @property
    def lines(self) -> int:
        with open(self.file_path, "rb") as f:
            num_lines = sum(1 for _ in f)
        return num_lines

    @property
    def words(self) -> int:
        with open(self.file_path, encoding="utf8") as f:
            num_words = len(re.findall(r"[^\s]+", f.read()))
        return num_words

    @property
    def chars(self) -> int:
        with open(self.file_path, encoding="utf8") as f:
            num_chars = len(f.read())
        return num_chars

    def output_func(self, property_name: str) -> str:
        return f"{getattr(self, property_name)}\t{self.file_path}"

    @property
    def output_no_args(self) -> str:
        return f"{self.lines}\t{self.words}\t{self.bytes}\t{self.file_path}"


@dataclass
class WCText(WCObject):
    """WCObject when wc is called against stdin."""

    text: str

    @property
    def bytes(self) -> int:
        return len(self.text.encode("utf-8"))

    @property
    def lines(self) -> int:
        return self.text.count("\n")

    @property
    def words(self) -> int:
        return len(re.findall(r"[^\s]+", self.text))

    @property
    def chars(self) -> int:
        return len(self.text)

    def output_func(self, property_name: str) -> str:
        return f"{getattr(self, property_name)}"

    @property
    def output_no_args(self) -> str:
        return f"{self.lines}\t{self.words}\t{self.bytes}"


def main() -> None:
    """Execute wc (via the ccwc command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", action="store", nargs="*")
    parser.add_argument("-c", "--bytes", action="store_true")
    parser.add_argument("-l", "--lines", action="store_true")
    parser.add_argument("-w", "--words", action="store_true")
    parser.add_argument("-m", "--chars", action="store_true")
    args = parser.parse_args()
    if not sys.stdin.isatty():
        args.FILE.extend(sys.stdin.read())
    if args.FILE is None:
        return
    if all(Path(FILE).is_file() for FILE in args.FILE):
        objects = [WCFile(FILE) for FILE in args.FILE]
    else:
        objects = [WCText("".join(args.FILE))]
    for wc_file in objects:
        if args.bytes:
            print(wc_file.output_func("bytes"))
        elif args.lines:
            print(wc_file.output_func("lines"))
        elif args.words:
            print(wc_file.output_func("words"))
        elif args.chars:
            print(wc_file.output_func("chars"))
        else:
            print(wc_file.output_no_args)
