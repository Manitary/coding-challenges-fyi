"""Imitate wc."""

from pathlib import Path
import os
import argparse


def wc_bytes(file_path: str | Path) -> int:
    return os.path.getsize(file_path)


def wc_lines(file_path: str | Path) -> int:
    with open(file_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", action="store", nargs="+")
    parser.add_argument("-c", "--bytes", action="store_true")
    parser.add_argument("-l", "--lines", action="store_true")
    args = parser.parse_args()
    for file_path in args.file_path:
        if args.bytes:
            print(f"{wc_bytes(file_path)} {file_path}")
        if args.lines:
            print(f"{wc_lines(file_path)} {file_path}")
