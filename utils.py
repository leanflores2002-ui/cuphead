
"""
Utilidades (requests, regex parsing, etc.).
"""
import re
import requests


MOVE_RE = re.compile(r"^(T|F)(\d)\s*->\s*(T|F)(\d)$", re.IGNORECASE)


def parse_move_string(move_str: str):
    """
    Parsea cadenas tipo:
      - "T1->F1"  (mover de Tableau 1 a Foundation 1)
      - "T2->T3"  (mover de Tableau 2 a Tableau 3)
      - "DRAW"
    Devuelve dict con estructura, o None si no matchea.
    """
    s = move_str.strip().upper()
    if s == "DRAW":
        return {"kind": "DRAW"}
    m = MOVE_RE.match(s)
    if not m:
        return None
    src_type, src_idx, dst_type, dst_idx = m.groups()
    return {
        "kind": "MOVE",
        "src_type": "T" if src_type.upper() == "T" else "F",
        "src_idx": int(src_idx) - 1,  # index base 0
        "dst_type": "T" if dst_type.upper() == "T" else "F",
        "dst_idx": int(dst_idx) - 1,
    }


def fetch_tip(timeout: float = 2.5):
    """
    Obtiene un tip/texto corto desde una API pública.
    Maneja fallos silenciosamente (la app no depende de esto).
    """
    url = "https://api.adviceslip.com/advice"
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            return data.get("slip", {}).get("advice")
    except Exception:
        return None
    return None
