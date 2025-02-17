#!/usr/bin/env python3
"""
Like /bin/true for pre-commit
"""
from __future__ import annotations
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
