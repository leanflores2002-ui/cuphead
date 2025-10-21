Boss-Rush Medieval (Cuphead‑inspirado)

Descripción
-----------
Proyecto académico de juego estilo boss‑rush con temática medieval (caballero vs. goblin/ogro/dragón). Backend en Python + Flask y frontend HTML/CSS/JS minimal (Canvas 2D). Implementa POO (ABC, herencia, polimorfismo), modularización y persistencia JSON de perfiles.

Instalación
-----------
Requisitos: Python 3.10+

1) Crear y activar un entorno virtual (opcional pero recomendado)
   - Windows PowerShell:
     python -m venv .venv
     .venv\\Scripts\\Activate.ps1

2) Instalar dependencias
   pip install -r requirements.txt

Ejecución
--------
python main.py

Abrir en el navegador:
http://localhost:5000

Estructura de módulos
---------------------
- game/abstracts.py: ABC `Character` (update, attack, take_damage, is_alive)
- game/entities.py: `Knight` (principal, con __gold encapsulado), `Enemy` base y `Goblin`/`Ogre`/`Dragon`
- game/level.py: carga de assets y construcción de enemigos por id
- game/engine.py: loop/tick simple, deque de inputs, Queue de eventos, colisiones AABB
- game/crud.py: CRUD completo de `Knight` usando `storage`
- game/utils.py: utilidades; validación de nombre con `re`
- game/storage.py: persistencia JSON de perfiles (web/data/knights.json)
- game/api.py: servidor Flask + endpoints REST y del juego
- game/assets/: `enemies.json`, `levels.json`
- web/templates/index.html: interfaz (menú, juego, resultados)
- web/static/css/style.css: estilos
- web/static/js/game.js: Canvas 2D, fetch de acciones y polling de estado
- main.py: punto de entrada Flask

Endoints principales
--------------------
- GET `/` → index.html
- POST `/api/knight` | GET/PUT/DELETE `/api/knight/<name>`
- POST `/api/start_boss/<boss_id>` (goblin/ogre/dragon)
- POST `/api/action` (move_left, move_right, attack, jump, dash)
- GET `/api/state` (snapshot JSON)
- GET `/api/save/<name>` | GET `/api/load/<name>`

Módulos de la cátedra utilizados
--------------------------------
- collections.deque → buffer de inputs en `engine`
- queue.Queue → bus de eventos entre engine y API
- json → persistencia de perfiles y assets
- re → validación de nombres de jugador

Buenas prácticas y documentación
--------------------------------
- Docstrings y comentarios en todas las clases y funciones claves
- Tipado con `typing` y PEP8 razonable
- Separación de responsabilidades por módulos

Créditos y licencias
--------------------
Código de ejemplo para fines académicos. No incluye assets con copyright.
