"""Level and wave definitions.

Loads enemy and level configs from JSON assets and exposes helpers to create
enemies for the requested boss id.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

from .entities import Dragon, Enemy, Goblin, Ogre

ASSETS_DIR = Path(__file__).parent / "assets"


def load_json(path: Path) -> Dict:
    """Load and return JSON from a file path."""

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_enemy(boss_id: str) -> Enemy:
    """Create an enemy instance from asset configs.

    Parameters
    ----------
    boss_id:
        One of ``"goblin"``, ``"ogre"``, ``"dragon"``.
    """

    enemies = load_json(ASSETS_DIR / "enemies.json")
    cfg = enemies.get(boss_id)
    if not cfg:
        raise ValueError(f"Unknown boss_id: {boss_id}")

    pos: Tuple[int, int] = tuple(cfg.get("start_pos", [220, 50]))  # type: ignore[assignment]
    hp: int = int(cfg.get("health", 80))
    if boss_id == "goblin":
        return Goblin(name="Goblin", health=hp, position=pos, attack_damage=6)
    if boss_id == "ogre":
        return Ogre(name="Ogre", health=hp, position=pos, attack_damage=12)
    if boss_id == "dragon":
        return Dragon(name="Dragon", health=hp, position=pos, attack_damage=8)

    raise ValueError(f"Unsupported boss: {boss_id}")

