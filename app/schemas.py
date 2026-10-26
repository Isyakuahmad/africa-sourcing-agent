from __future__ import annotations

from typing import Any


def as_display(value: Any, default: str = "Unknown") -> str:
    if value is None or value == "":
        return default
    return str(value)
