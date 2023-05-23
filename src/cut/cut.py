"""Imitate cut."""

import sys
import argparse
import re
from pathlib import Path
from typing import Sequence


def cut_fields(
    file_path: str | Path, fields: Sequence[int], delimiter: str = "\t"
) -> str:
    """Cut the selected fields of the selected file."""
    with open(file_path, encoding="utf-8-sig") as f:
        ans = [
            delimiter.join(
                field for i, field in enumerate(line.split(delimiter), 1) if i in fields
            )
            for line in f.readlines()
        ]
    return "\n".join(ans)


def main() -> None:
    """Execute cut (via the cccut command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", action="store", nargs="*")
    parser.add_argument("-f", "--fields", action="store", type=str)
    parser.add_argument("-d", "--delimiter", action="store", type=str, default="\t")
    args = parser.parse_args()
    if not sys.stdin.isatty():
        args.FILE.extend(sys.stdin.read())
    if args.FILE is None:
        return
    for file_path in args.FILE:
        if args.fields:
            print(
                cut_fields(
                    file_path,
                    fields=list(map(int, re.split(r",|\s", args.fields))),
                    delimiter=args.delimiter,
                )
            )
