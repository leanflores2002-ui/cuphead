"""Minimal game engine: tick, inputs, collisions, and events.

This engine uses:
- collections.deque for the input buffer
- queue.Queue for a simple event bus between API and engine
- basic AABB collision for attacks
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from queue import Queue
from typing import Deque, Dict, Iterable, List, Optional, Tuple

from .entities import Enemy, Knight


def aabb_overlap(ax: int, ay: int, aw: int, ah: int, bx: int, by: int, bw: int, bh: int) -> bool:
    """Return True if two AABBs overlap."""

    return (ax < bx + bw) and (bx < ax + aw) and (ay < by + bh) and (by < ay + ah)


@dataclass
class GameEngine:
    """Simple discrete-time engine to drive a single boss fight.

    Attributes
    ----------
    player:
        Current player (Knight) instance.
    enemy:
        Current enemy instance.
    inputs:
        Buffer of queued actions, fed from API.
    events:
        Queue for outbound events (e.g., damage numbers) the API could consume.
    frame:
        Frame counter; increases at each ``step`` invocation.
    """

    player: Knight
    enemy: Optional[Enemy] = None
    inputs: Deque[str] = field(default_factory=lambda: deque(maxlen=64))
    events: Queue = field(default_factory=Queue)
    frame: int = 0

    def enqueue_action(self, action: str) -> None:
        """Push an input action into the buffer."""

        self.inputs.append(action)

    def start_boss(self, enemy: Enemy) -> None:
        """Start a new boss fight with the provided enemy."""

        self.enemy = enemy
        self.frame = 0
        self.inputs.clear()

    def step(self, dt: float = 0.016) -> None:
        """Advance the simulation by one fixed tick.

        Notes
        -----
        This method consumes at most one input per tick to keep the game pace
        stable and predictable for the basic implementation.
        """

        self.frame += 1

        # Consume one input per frame (if available)
        if self.inputs:
            action = self.inputs.popleft()
            self._apply_action(action)

        # Update entities
        self.player.update(dt)
        if self.enemy:
            self.enemy.update(dt)
            self._resolve_enemy_attack()

    def _apply_action(self, action: str) -> None:
        """Apply a single action to update the game state.

        Parameters
        ----------
        action:
            One of ``move_left``, ``move_right``, ``jump`` (visual only),
            ``attack``, ``dash`` (visual only).
        """

        x, y = self.player.position
        if action == "move_left":
            self.player.position = (x - 10, y)
        elif action == "move_right":
            self.player.position = (x + 10, y)
        elif action == "attack":
            self._resolve_player_attack()
        # jump/dash are placeholders for visuals; no physics implemented

    def _resolve_player_attack(self) -> None:
        """Resolve the player's attack hitbox against the enemy."""

        if not self.enemy:
            return
        hb = self.player.attack()
        ex, ey = self.enemy.position
        if aabb_overlap(hb["x"], hb["y"], hb["w"], hb["h"], ex - 10, ey - 10, 20, 20):
            self.enemy.take_damage(int(hb["damage"]))
            self.events.put({"type": "hit", "amount": hb["damage"], "frame": self.frame})

    def _resolve_enemy_attack(self) -> None:
        """Resolve the enemy attack hitbox against the player."""

        if not self.enemy:
            return
        hb = self.enemy.attack()
        px, py = self.player.position
        if aabb_overlap(hb["x"], hb["y"], hb["w"], hb["h"], px - 10, py - 10, 20, 20):
            self.player.take_damage(int(hb["damage"]))
            self.events.put({"type": "player_hit", "amount": hb["damage"], "frame": self.frame})

    def snapshot(self) -> Dict[str, object]:
        """Return an immutable snapshot of the current state for the API."""

        enemy_state: Optional[Dict[str, object]]
        if self.enemy:
            enemy_state = {
                "name": self.enemy.name,
                "health": self.enemy.health,
                "position": self.enemy.position,
                "alive": self.enemy.is_alive(),
            }
        else:
            enemy_state = None

        return {
            "frame": self.frame,
            "player": {
                "name": self.player.name,
                "health": self.player.health,
                "stamina": self.player.stamina,
                "position": self.player.position,
                "gold": self.player.gold,
                "alive": self.player.is_alive(),
            },
            "enemy": enemy_state,
        }

