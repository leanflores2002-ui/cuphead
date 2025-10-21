"""Main entry point for the medieval boss-rush game.

Runs the Flask development server and initializes the game engine.

Usage:
    python main.py

Then open http://localhost:5000 in your browser.
"""

from __future__ import annotations

from game.api import create_app


def main() -> None:
    """Start the Flask dev server.

    This function creates the Flask application via ``create_app`` and runs it
    in development mode on port 5000.
    """

    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()

