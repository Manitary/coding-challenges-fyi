"""Imitate cut."""

import sys
import argparse


def main() -> None:
    """Execute cut (via the cccut command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", action="store", nargs="*")
    args = parser.parse_args()
    if not sys.stdin.isatty():
        args.FILE.extend(sys.stdin.read())
    if args.FILE is None:
        return
