"""Storage utilities for JSON persistence of profiles and stats.

Uses ``json`` to store and load knight profiles at ``web/data/knights.json``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

DATA_DIR = Path("web/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
KNIGHTS_PATH = DATA_DIR / "knights.json"


def _read_all() -> Dict[str, Dict]:
    """Read and return all knight profiles from storage."""

    if not KNIGHTS_PATH.exists():
        return {}
    with KNIGHTS_PATH.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _write_all(data: Dict[str, Dict]) -> None:
    """Write all knight profiles to storage."""

    with KNIGHTS_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_knight(profile: Dict) -> None:
    """Create or update a knight profile in storage."""

    data = _read_all()
    data[profile["name"]] = profile
    _write_all(data)


def load_knight(name: str) -> Optional[Dict]:
    """Load a knight profile by name or return ``None`` if missing."""

    return _read_all().get(name)


def delete_knight(name: str) -> bool:
    """Delete a knight profile by name. Returns True if removed."""

    data = _read_all()
    if name in data:
        del data[name]
        _write_all(data)
        return True
    return False


def list_knights() -> Dict[str, Dict]:
    """Return a dict of all knights keyed by name."""

    return _read_all()

