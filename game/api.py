"""Flask API for the medieval boss-rush game.

Endpoints
---------
- ``GET /`` -> render main page
- CRUD Knight: ``POST /api/knight``, ``GET/PUT/DELETE /api/knight/<name>``
- Game: ``POST /api/start_boss/<boss_id>``, ``POST /api/action``, ``GET /api/state``
- Persistence: ``GET /api/save/<name>``, ``GET /api/load/<name>``

Modules from the cátedra used with purpose
-----------------------------------------
- ``collections.deque``: Input buffer in engine
- ``queue.Queue``: Event bus between API and engine
- ``json``: Persist profiles and assets
- ``re``: Validate knight names
"""

from __future__ import annotations

from typing import Dict, Optional

from flask import Flask, jsonify, render_template, request
from pathlib import Path

from .crud import create_knight, delete_knight_profile, read_knight, update_knight
from .engine import GameEngine
from .entities import Knight
from .level import create_enemy
from .storage import load_knight, save_knight
from .utils import clamp_position


def create_app() -> Flask:
    """Application factory that wires the engine and routes."""

    root = Path(__file__).resolve().parents[1]
    app = Flask(
        __name__,
        template_folder=str(root / "web/templates"),
        static_folder=str(root / "web/static"),
        static_url_path="/static",
    )

    # Global engine (simple single-session model for academic demo)
    engine: Optional[GameEngine] = None

    def get_engine() -> GameEngine:
        nonlocal engine
        if engine is None:
            # Default player stub; actual player is loaded on start
            engine = GameEngine(player=Knight(name="Player"))
        return engine

    @app.get("/")
    def index() -> str:
        """Render main page with forms and canvas."""

        return render_template("index.html")

    # CRUD endpoints
    @app.post("/api/knight")
    def api_create_knight():  # type: ignore[override]
        """Create a new knight profile from JSON payload {name}."""
        payload: Dict = request.get_json(force=True) or {}
        name: str = str(payload.get("name", "")).strip()
        profile = create_knight(name)
        return jsonify(profile), 201

    @app.get("/api/knight/<name>")
    def api_read_knight(name: str):  # type: ignore[override]
        """Read a knight profile by name."""
        profile = read_knight(name)
        if not profile:
            return jsonify({"error": "not found"}), 404
        return jsonify(profile)

    @app.put("/api/knight/<name>")
    def api_update_knight(name: str):  # type: ignore[override]
        """Update a knight profile with provided fields."""
        updates: Dict = request.get_json(force=True) or {}
        profile = update_knight(name, updates)
        return jsonify(profile)

    @app.delete("/api/knight/<name>")
    def api_delete_knight(name: str):  # type: ignore[override]
        """Delete a knight profile by name."""
        ok = delete_knight_profile(name)
        return ("", 204) if ok else (jsonify({"error": "not found"}), 404)

    # Game endpoints
    @app.post("/api/start_boss/<boss_id>")
    def api_start_boss(boss_id: str):  # type: ignore[override]
        """Start a fight with the specified boss for active player name."""
        payload: Dict = request.get_json(silent=True) or {}
        name = payload.get("name")
        if not name:
            return jsonify({"error": "name required"}), 400
        profile = load_knight(name)
        if not profile:
            return jsonify({"error": "profile not found"}), 404

        k = Knight(
            name=profile["name"],
            health=int(profile.get("health", 100)),
            stamina=float(profile.get("stamina", 100.0)),
            position=tuple(profile.get("position", [50, 50])),
        )
        k.gold = int(profile.get("gold", 0))

        eng = get_engine()
        eng.player = k
        eng.start_boss(create_enemy(boss_id))
        return jsonify({"ok": True, "boss": boss_id})

    @app.post("/api/action")
    def api_action():  # type: ignore[override]
        """Enqueue a player action and advance one engine step."""
        payload: Dict = request.get_json(force=True) or {}
        action: str = str(payload.get("action", "")).strip()
        eng = get_engine()
        eng.enqueue_action(action)
        eng.step()
        # Clamp position to arena each step
        eng.player.position = clamp_position(eng.player.position)
        return jsonify({"ok": True})

    @app.get("/api/state")
    def api_state():  # type: ignore[override]
        """Return a JSON snapshot of the current game state."""
        eng = get_engine()
        # Run a passive step to keep enemy patterns moving even without input
        eng.step()
        eng.player.position = clamp_position(eng.player.position)
        return jsonify(eng.snapshot())

    # Persistence helpers
    @app.get("/api/save/<name>")
    def api_save(name: str):  # type: ignore[override]
        """Save the active player's profile to storage."""
        eng = get_engine()
        if eng.player.name != name:
            return jsonify({"error": "active player mismatch"}), 400
        profile = {
            "name": eng.player.name,
            "health": eng.player.health,
            "stamina": eng.player.stamina,
            "position": list(eng.player.position),
            "gold": eng.player.gold,
            "skin": getattr(eng.player, "skin", "default"),
            "progress": {"defeated": []},
        }
        save_knight(profile)
        return jsonify({"ok": True})

    @app.get("/api/load/<name>")
    def api_load(name: str):  # type: ignore[override]
        """Load a player's profile by name from storage."""
        profile = load_knight(name)
        if not profile:
            return jsonify({"error": "not found"}), 404
        return jsonify(profile)

    return app
