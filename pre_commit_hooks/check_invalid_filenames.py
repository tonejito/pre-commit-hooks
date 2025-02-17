#!/usr/bin/env python3
"""
Check that filenames do not have invalid characters.
"""
from __future__ import annotations
from typing import Sequence

import argparse
import os
import re
import sys
import locale


def check_file_name(file_name: str) -> bool:
    my_regex = ".*[^-_.a-zA-Z0-9].*"
    pattern = re.compile(my_regex)
    # file_name = os.path.basename(file_name)
    ret = True

    for path_component in file_name.split(os.sep):
        match = pattern.match(path_component)

        # MatchObject if found
        if isinstance(match, re.Match):
            ret = False

        # # None if not found
        # if match is None:
        #     ret = True

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    locale.setlocale(locale.LC_ALL, "C")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    ret = 0

    for file_name in args.filenames:
        if not check_file_name(file_name):
            print("Path contains spaces or accents:", file=sys.stderr)
            print(f"	{file_name}", file=sys.stderr)
            ret = -1

    return ret


if __name__ == "__main__":
    raise SystemExit(main())
