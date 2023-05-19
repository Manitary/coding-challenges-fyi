"""Imitate wc."""

from pathlib import Path
import os
import argparse


def wc(file_path: str | Path) -> int:
    return os.path.getsize(file_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", action="store", nargs="+")
    parser.add_argument("-c", "--bytes", action="store_true")
    args = parser.parse_args()
    for file_path in args.file_path:
        if args.bytes:
            print(f"{wc(file_path)} {file_path}")
