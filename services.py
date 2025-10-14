
"""
Servicios de aplicación: orquestan reglas del juego y repositorio.
"""
from typing import Optional, Tuple, Dict, Any
from models.game import SolitaireGame
from repo import GameRepository
from utils import fetch_tip


class GameService:
    """Capa de servicios que aplica reglas y coordina con el repositorio."""

    def __init__(self, repo: GameRepository) -> None:
        self.repo = repo

    def create_game(self, seed: Optional[int] = None) -> SolitaireGame:
        """Crea nueva partida, la persiste y devuelve la instancia."""
        game = SolitaireGame(seed=seed)
        self.repo.create(game)
        # Intentar traer un tip opcional (requests) para la UI.
        tip = fetch_tip()
        if tip:
            game.meta["tip"] = tip
        return game

    def get_game(self, game_id: str) -> Optional[SolitaireGame]:
        """Obtiene una partida por ID."""
        return self.repo.read(game_id)

    def apply_move(self, game: SolitaireGame, parsed_move: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Aplica un movimiento validado.
        Retorna (ok, mensaje).
        """
        kind = parsed_move["kind"]
        if kind == "DRAW":
            ok, msg = game.draw()
        elif kind == "MOVE":
            src_type = parsed_move["src_type"]
            src_idx = parsed_move["src_idx"]
            dst_type = parsed_move["dst_type"]
            dst_idx = parsed_move["dst_idx"]
            ok, msg = game.move(src_type, src_idx, dst_type, dst_idx)
        else:
            return False, "Unknown move kind"

        # Persistir cambio (no-op real en este repo)
        self.repo.update(game)
        return ok, msg

    def delete_game(self, game_id: str) -> bool:
        """Elimina una partida."""
        return self.repo.delete(game_id)
