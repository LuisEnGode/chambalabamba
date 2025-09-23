# participa/seeds/seed_visitas_guiadas.py
from django.core.management import call_command, CommandError
from django.db import connection, transaction
from django.conf import settings
from pathlib import Path

# Sube la versión (v2, v3, …) cuando cambies datos para que vuelva a cargar
SEED_TAG = "visitas_guiadas:v5"

# Nombre del fixture
# - FIXTURE_BASENAME: nombre sin extensión (Django buscará en app/fixtures y FIXTURE_DIRS)
# - FIXTURE_FILENAME: nombre exacto con .json (fallback por rutas)
FIXTURE_BASENAME = "visitas_guiadas"

FIXTURE_FILENAME = "visitas_guiadas.json"

def _try_loaddata(arg) -> tuple[bool, str | None]:
    try:
        call_command("loaddata", arg, verbosity=0)
        return True, None
    except CommandError as e:
        return False, str(e)

def _seed_visitas_guiadas_once(sender, **kwargs):
    """
    Carga una única vez la fixture de Visitas guiadas.
    - Marca en tabla seed_run con el tag SEED_TAG.
    - Busca por nombre y por rutas conocidas (participa/fixtures, participa/seeds/fixtures, FIXTURE_DIRS).
    """
    with connection.cursor() as cur, transaction.atomic():
        # 0) Tabla de control (si no existe)
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        # 1) ¿Ya corrimos esta versión?
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_visitas] Ya corrido {SEED_TAG}, no se recarga")
            return

        loaded = False
        err = None

        # 2) Intento estándar por nombre (Django resolverá rutas de fixtures)
        ok, err = _try_loaddata(FIXTURE_BASENAME)
        if ok:
            print(f"[seed_visitas] Cargado por nombre: {FIXTURE_BASENAME}")
            loaded = True
        else:
            print(f"[seed_visitas] No se encontró por nombre ({FIXTURE_BASENAME}). Probando rutas…")

            # 3) Fallback: buscar en rutas conocidas
            seeds_dir = Path(__file__).resolve().parent           # participa/seeds
            app_dir   = seeds_dir.parent                          # participa
            candidate_dirs = [
                app_dir / "fixtures",                             # participa/fixtures
                seeds_dir / "fixtures",                           # participa/seeds/fixtures
            ]

            # FIXTURE_DIRS del settings (si existen)
            try:
                for p in getattr(settings, "FIXTURE_DIRS", []):
                    candidate_dirs.append(Path(p))
            except Exception:
                pass

            # Evitar duplicados manteniendo orden
            seen = set()
            ordered_candidates = []
            for d in candidate_dirs:
                if d not in seen:
                    ordered_candidates.append(d)
                    seen.add(d)

            for d in ordered_candidates:
                path = d / FIXTURE_FILENAME
                if path.exists():
                    ok, err = _try_loaddata(str(path))
                    if ok:
                        print(f"[seed_visitas] Cargado fixture: {path}")
                        loaded = True
                        break
                    else:
                        print(f"[seed_visitas] ERROR cargando {path.name}: {err}")

            if not loaded:
                print("[seed_visitas] No encontré la fixture en:")
                for d in ordered_candidates:
                    print(f"  - {d}")
                if err:
                    print(f"[seed_visitas] Último error: {err}")

        # 4) Marca solo si cargó
        if loaded:
            cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
            print(f"[seed_visitas] Marcado {SEED_TAG}")
        else:
            print("[seed_visitas] No se cargó nada. NO marco el SEED_TAG.")
