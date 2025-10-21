"""Abstract base classes for the game.

Contains the abstract ``Character`` class which defines the contract for
all characters (player and enemies) in the game.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple


class Character(ABC):
    """Abstract character in the game.

    All characters must implement the following interface which allows the
    engine to update their state, perform attacks, take damage, and check
    whether they are alive.
    """

    name: str
    health: int
    position: Tuple[int, int]

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance internal state by ``dt`` seconds.

        Parameters
        ----------
        dt:
            Delta time in seconds (fixed tick in our engine).
        """

    @abstractmethod
    def attack(self) -> dict:
        """Perform an attack and return a description of the hitbox.

        Returns
        -------
        dict
            A dictionary that describes an axis-aligned box attack, e.g.::

                {"type": "aabb", "x": 10, "y": 10, "w": 20, "h": 10, "damage": 5}
        """

    @abstractmethod
    def take_damage(self, amount: int) -> None:
        """Apply incoming damage to this character.

        Parameters
        ----------
        amount:
            Damage to subtract from health. Minimum effective damage is 0.
        """

    @abstractmethod
    def is_alive(self) -> bool:
        """Whether the character's health is above zero."""

