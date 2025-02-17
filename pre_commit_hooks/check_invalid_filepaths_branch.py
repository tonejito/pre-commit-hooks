#!/usr/bin/env python3
"""
Check that directory names match a pattern.
"""
from __future__ import annotations
from typing import Sequence

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output

import argparse
import os
import re
import sys
import locale


BRANCH_DATA = {
    "tarea": "tareas",
    "practica": "practicas",
    "examen": "examenes",
    "proyecto": "proyectos",
}


def get_branch_name() -> str:
    # try:
    #     ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    # except CalledProcessError:
    #     return False
    # chunks = ref_name.strip().split('/')
    # branch_name = '/'.join(chunks[2:])

    try:
        branch_name = cmd_output("git", "rev-parse", "--abbrev-ref", "HEAD")
        branch_name = branch_name.strip()
    except CalledProcessError:
        branch_name = None

    return branch_name


def check_file_path_branch(branch: str, file_name: str) -> bool:
    branch = branch.strip()
    file_name = file_name.strip()
    (my_path, my_name) = os.path.split(file_name)
    my_path = my_path.strip()
    my_name = my_name.strip()
    # TODO: Abort if 'None'
    my_branch = branch.split("-")[0]
    my_branch = my_branch.strip()
    ret = None

    if my_branch in BRANCH_DATA.keys():
        my_kind = BRANCH_DATA.get(my_branch, None)
        expected_path_name = f"docs/{my_kind}/{branch}"
        # if my_path.startswith(expected_path_name):
        # if file_name.startswith(expected_path_name):
        if expected_path_name in my_path:
            ret = True
        else:
            print("Path does not match branch name:", file=sys.stderr)
            print(f"	file_path:	{my_path}", file=sys.stderr)
            print(f"	expected:	{expected_path_name}", file=sys.stderr)
            ret = False
    else:
        ret = True

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    locale.setlocale(locale.LC_ALL, "C")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    # TODO: Abort if branch_name is not 'str' (None)
    branch_name = get_branch_name()

    ret = 0

    for file_name in args.filenames:
        if not check_file_path_branch(branch_name, file_name):
            # print(file_name, file=sys.stderr)
            ret = -1

    return ret


if __name__ == "__main__":
    raise SystemExit(main())
