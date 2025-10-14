
"""
Aplicación Flask: backend del juego de Solitario (Klondike simplificado).

- Expone API REST para CRUD del juego.
- Sirve plantilla HTML y CSS para interfaz básica.
"""

from flask import Flask, render_template, request, jsonify
from services import GameService
from repo import GameRepository
from utils import parse_move_string
import json

app = Flask(__name__)

# Repositorio en memoria (se podría cambiar a persistencia en archivo/DB)
repo = GameRepository()
service = GameService(repo)


@app.route("/")
def index():
    """Página principal con la UI mínima del juego."""
    return render_template("index.html")


# ------------------ API CRUD ------------------

@app.post("/api/game")
def create_game():
    """Crea una nueva partida (Create)."""
    seed = request.json.get("seed") if request.is_json else None
    game = service.create_game(seed=seed)
    return jsonify(game.to_dict()), 201


@app.get("/api/game/<game_id>")
def read_game(game_id: str):
    """Lee el estado de una partida (Read)."""
    game = service.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(game.to_dict())


@app.put("/api/game/<game_id>/move")
def update_game(game_id: str):
    """
    Aplica un movimiento (Update).
    Body JSON esperado:
    {
      "move": "T1->F1" | "T2->T3" | "DRAW"
    }
    """
    if not request.is_json:
        return jsonify({"error": "Expected JSON body"}), 400

    move_str = request.json.get("move", "").strip().upper()
    game = service.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    # Validar formato de movimiento con utils (re + parseo)
    parsed = parse_move_string(move_str)
    if not parsed:
        return jsonify({"error": "Invalid move format"}), 400

    ok, msg = service.apply_move(game, parsed)
    if not ok:
        return jsonify({"error": msg}), 400

    return jsonify(game.to_dict())


@app.delete("/api/game/<game_id>")
def delete_game(game_id: str):
    """Elimina (borra) la partida (Delete)."""
    deleted = service.delete_game(game_id)
    if not deleted:
        return jsonify({"error": "Game not found"}), 404
    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    # Punto de entrada principal
    app.run(debug=True)
