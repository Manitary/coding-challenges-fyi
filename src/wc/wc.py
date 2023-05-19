"""Imitate wc."""

import os
import argparse


def wc(file_path: str) -> int:
    return os.path.getsize(file_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", action="store", nargs="+")
    args = parser.parse_args()
    for file_path in args.file_path:
        print(wc(file_path))
