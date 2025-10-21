"""CRUD operations for the main Knight entity.

Integrates with :mod:`game.storage` to persist profiles in JSON.
"""

from __future__ import annotations

from typing import Dict, Optional

from .entities import Knight
from .storage import delete_knight, load_knight, save_knight
from .utils import valid_name


def create_knight(name: str) -> Dict:
    """Create a new knight profile if the name is valid and unique.

    Returns the profile dict. Raises ``ValueError`` if invalid.
    """

    if not valid_name(name):
        raise ValueError("Nombre inválido: use 3-16 letras (A-Z/a-z)")
    if load_knight(name):
        raise ValueError("Ya existe un caballero con ese nombre")

    k = Knight(name=name)
    profile = {
        "name": k.name,
        "health": k.health,
        "stamina": k.stamina,
        "position": list(k.position),
        "gold": k.gold,
        "skin": k.skin,
        "progress": {"defeated": []},
    }
    save_knight(profile)
    return profile


def read_knight(name: str) -> Optional[Dict]:
    """Return profile for ``name`` or ``None`` if not found."""

    return load_knight(name)


def update_knight(name: str, updates: Dict) -> Dict:
    """Update fields of an existing knight profile and save it."""

    profile = load_knight(name)
    if not profile:
        raise ValueError("Caballero no encontrado")
    profile.update(updates)
    save_knight(profile)
    return profile


def delete_knight_profile(name: str) -> bool:
    """Delete the profile by name. Returns True if deleted."""

    return delete_knight(name)

