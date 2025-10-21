"""Game entities: Knight (player) and enemies.

This module implements the concrete classes derived from :class:`game.abstracts.Character`.
It demonstrates encapsulation (private gold with property), inheritance, and
polymorphism across ``update``, ``attack``, and ``take_damage``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from .abstracts import Character


@dataclass
class Knight(Character):
    """Player-controlled knight and main CRUD entity.

    Attributes
    ----------
    name:
        Unique name for the profile.
    health:
        Current health points.
    stamina:
        Stamina resource for actions like dash or heavy attack.
    position:
        World position ``(x, y)`` in pixels (simple 2D plane).
    __gold:
        Encapsulated player gold, accessible through the ``gold`` property.
    skin:
        Cosmetic string identifier.
    """

    name: str
    health: int = 100
    stamina: float = 100.0
    position: Tuple[int, int] = (50, 50)
    _Knight__gold: int = field(default=0, repr=False)
    skin: str = "default"

    def update(self, dt: float) -> None:
        """Regenerate stamina slightly every tick.

        Parameters
        ----------
        dt:
            Delta time in seconds.
        """

        self.stamina = min(100.0, self.stamina + 10.0 * dt)

    def attack(self) -> Dict[str, int | float | str]:
        """Sword slash attack: small AABB in front of the knight."""

        x, y = self.position
        return {"type": "aabb", "x": x + 20, "y": y, "w": 20, "h": 10, "damage": 10}

    def take_damage(self, amount: int) -> None:
        """Reduce health by ``amount`` (non-negative)."""

        dmg = max(0, int(amount))
        self.health = max(0, self.health - dmg)

    def is_alive(self) -> bool:
        """Knight is alive if health > 0."""

        return self.health > 0

    @property
    def gold(self) -> int:
        """Get current gold value."""

        return self._Knight__gold

    @gold.setter
    def gold(self, value: int) -> None:
        """Set gold with non-negative constraint."""

        self._Knight__gold = max(0, int(value))


@dataclass
class Enemy(Character):
    """Base enemy with simple behavior.

    Subclasses should override movement and attack patterns.
    """

    name: str
    health: int
    position: Tuple[int, int]
    attack_damage: int = 8

    def update(self, dt: float) -> None:  # pragma: no cover - base noop
        """Default enemy update: no movement in base class."""

    def attack(self) -> Dict[str, int | float | str]:
        """Default melee AABB around current position."""

        x, y = self.position
        return {"type": "aabb", "x": x - 10, "y": y, "w": 20, "h": 10, "damage": self.attack_damage}

    def take_damage(self, amount: int) -> None:
        """Reduce health by ``amount`` (non-negative)."""

        dmg = max(0, int(amount))
        self.health = max(0, self.health - dmg)

    def is_alive(self) -> bool:
        """Alive if health > 0."""

        return self.health > 0


class Goblin(Enemy):
    """Goblin: quick pokes, small HP, erratic horizontal movement."""

    def update(self, dt: float) -> None:
        x, y = self.position
        self.position = (x - 15, y)

    def attack(self) -> Dict[str, int | float | str]:
        hb = super().attack()
        hb["damage"] = 6
        return hb


class Ogre(Enemy):
    """Ogre: slow, heavy slam, higher HP."""

    slam_cooldown: float = 0.0

    def update(self, dt: float) -> None:
        x, y = self.position
        self.position = (x - 5, y)
        self.slam_cooldown = max(0.0, self.slam_cooldown - dt)

    def attack(self) -> Dict[str, int | float | str]:
        if self.slam_cooldown <= 0:
            self.slam_cooldown = 2.5
            x, y = self.position
            return {"type": "aabb", "x": x - 30, "y": y - 5, "w": 60, "h": 20, "damage": 14}
        return super().attack()


class Dragon(Enemy):
    """Dragon: breathes bursts of fire; faster horizontal drift."""

    breath_phase: float = 0.0

    def update(self, dt: float) -> None:
        x, y = self.position
        self.position = (x - 20, y)
        self.breath_phase += dt

    def attack(self) -> Dict[str, int | float | str]:
        x, y = self.position
        wide = 40 if int(self.breath_phase) % 2 == 0 else 20
        return {"type": "aabb", "x": x - 50, "y": y - 5, "w": 100, "h": wide, "damage": 8}

