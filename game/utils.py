"""Utility helpers for validation and small helpers.

Demonstrates usage of ``re`` for player name validation.
"""

from __future__ import annotations

import re
from typing import Tuple

NAME_RE = re.compile(r"^[A-Za-z]{3,16}$")


def valid_name(name: str) -> bool:
    """Return True if the provided name is valid.

    Rules
    -----
    - Only ASCII letters
    - Length between 3 and 16
    """

    return bool(NAME_RE.fullmatch(name))


def clamp_position(pos: Tuple[int, int], min_x: int = 0, max_x: int = 300) -> Tuple[int, int]:
    """Clamp x coordinate to a simple arena bounds for demo purposes."""

    x, y = pos
    x = max(min_x, min(max_x, x))
    return (x, y)

