
"""
Módulo de repositorio en memoria para gestionar CRUD de partidas.
"""
from typing import Dict, Optional
from models.game import SolitaireGame
import uuid


class GameRepository:
    """Repositorio simple en memoria para almacenar partidas por ID."""

    def __init__(self) -> None:
        self._store: Dict[str, SolitaireGame] = {}

    def create(self, game: SolitaireGame) -> str:
        """Guarda un juego y devuelve su ID único."""
        game_id = str(uuid.uuid4())
        self._store[game_id] = game
        game.game_id = game_id
        return game_id

    def read(self, game_id: str) -> Optional[SolitaireGame]:
        """Devuelve el juego por ID, o None si no existe."""
        return self._store.get(game_id)

    def update(self, game: SolitaireGame) -> None:
        """Actualiza el juego existente en el store (no-op aquí)."""
        if game.game_id:
            self._store[game.game_id] = game

    def delete(self, game_id: str) -> bool:
        """Elimina el juego; True si existía."""
        return self._store.pop(game_id, None) is not None
