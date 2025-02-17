#!/usr/bin/env python3
"""
Check that files are not binary executables.
"""
from __future__ import annotations
from typing import Sequence

import argparse
import locale
import magic
import re
import sys

mime_blacklist = [
    "application/octet-stream",
    "application/x-pie-executable",
    "application/x-mach-binary",
    "application/vnd.microsoft.portable-executable",
    "application/x-dosexec",
    "application/x-ms-dos-executable",
    "application/x-ms-ne-executable",
    "application/x-msdos-program",
]


def check_file_type(file_name: str) -> bool:
    mime_type = magic.from_file(file_name, mime=True)

    ret = None
    if mime_type in mime_blacklist:
        ret = False
    else:
        ret = True

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    locale.setlocale(locale.LC_ALL, "C")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    ret = 0

    for file_name in args.filenames:
        if not check_file_type(file_name):
            print("File is a binary executable:", file=sys.stderr)
            print(f"	{file_name}", file=sys.stderr)
            ret = -1

    return ret


if __name__ == "__main__":
    raise SystemExit(main())
