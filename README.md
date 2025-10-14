# Solitaire (Python + HTML/CSS)

Proyecto de ejemplo de **Solitario (Klondike simplificado)** con backend en **Python (Flask)** y frontend en **HTML/CSS**.
Cumple con:
- Código documentado con **docstrings** y comentarios.
- **Modularización**: clases separadas en `models/` y otros módulos (`repo.py`, `services.py`, `utils.py`).
- Clase principal `SolitaireGame` con **5+ atributos** (uno encapsulado con `@property`), **CRUD completo** vía API REST.
- Una clase (`TableauPile`) que **hereda** de una clase **abstracta** (`PileBase`).
- **Mínimo 3 módulos** vistos en clase: `collections.deque`, `queue`, `requests`, `json`, `re` (usamos 5).
- **Interfaz gráfica / interactiva** en `templates/index.html` + `static/styles.css` (usa una pizca de JS para llamar la API).
- `main` en `app.py`.

## Ejecutar

1) Crear y activar venv (opcional, recomendado)
```bash
python -m venv .venv
source .venv/bin/activate   # en Windows: .venv\Scripts\activate
```

2) Instalar dependencias
```bash
pip install -r requirements.txt
```

3) Ejecutar la app
```bash
python app.py
```
Abrí http://127.0.0.1:5000 en el navegador.

## Estructura

```
solitaire_project/
  app.py
  repo.py
  services.py
  utils.py
  requirements.txt
  README.md
  models/
    base.py
    card.py
    pile.py
    game.py
  templates/
    index.html
  static/
    styles.css
```

## Notas didácticas

- **CRUD** de `SolitaireGame`:
  - Create: `POST /api/game`
  - Read: `GET /api/game/<game_id>`
  - Update (mover cartas): `PUT /api/game/<game_id>/move`
  - Delete: `DELETE /api/game/<game_id>`

- **Módulos**:
  - `collections.deque`: mazo/descartes y algunas pilas.
  - `queue.Queue`: cola de eventos de movimientos dentro del juego.
  - `requests`: obtiene un **tip** opcional para mostrar en la UI (con tolerancia a fallos).
  - `json`: serialización de estado.
  - `re`: validación de formato de movimientos (p. ej., `T1->F1`, `T2->T3`).

- **Clases & abstracción**:
  - `PileBase` (abstracta) -> `TableauPile`, `FoundationPile` (herencia, polimorfismo).
  - `SolitaireGame` (clase principal): 
    - Atributos: `deck`, `waste`, `tableaus`, `foundations`, `_seed` (encapsulado), `moves_log`, `event_queue`.
    - Encapsulación con `@property` para `seed`.
    - Métodos de juego y serialización.

- **Reglas (simplificadas)**:
  - Mazo (`deck`) boca abajo; `waste` (descartes) boca arriba al robar.
  - 7 pilas de `tableau` (T1..T7), 4 `foundation` (F1..F4) por palo, empezando en As hasta K.
  - Movimiento permitido básico: 
    - `T? -> T?` si la carta de origen es un rango uno menor y alterna color.
    - `T? -> F?` si es del mismo palo y rango siguiente exacto.
  - `DRAW` roba 1 carta del mazo al `waste`. Cuando el mazo termina, se recicla `waste`.
  - Para simplificar, se permiten solo movimientos de **1 carta** (no corrimientos múltiples).

## Mejoras opcionales
- Persistencia en JSON/SQLite.
- Arrastrar y soltar en frontend.
- Reportes de estadísticas (matplotlib, pandas).