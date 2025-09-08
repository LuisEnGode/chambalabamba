from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

SEED_TAG = "estancias:v6"  # súbelo (v2, v3, …) cuando quieras resembrar

def _seed_estancias_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        # Tabla que recuerda qué semillas ya corrieron
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        # ¿Ya corrimos esta versión?
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_estancias] Ya corrido {SEED_TAG}, no se recarga")
            return

        # Ruta absoluta a los fixtures de la app estancias
        fixtures_dir = Path(__file__).resolve().parent / "fixtures"
        fixtures = [
            "estancias.json",         # Estancia (cabecera)
            "estancias_fotos.json",   # EstanciaFoto
            "estancias_specs.json",   # EstanciaSpec
        ]

        # Carga en orden (omite silenciosamente si falta alguno)
        for fx in fixtures:
            path = fixtures_dir / fx
            if path.exists():
                call_command("loaddata", str(path), verbosity=0)
                print(f"[seed_estancias] Cargado fixture: {path.name}")
            else:
                print(f"[seed_estancias] Omitido (no existe): {path.name}")

        # Marca como ejecutado
        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_estancias] Marcado {SEED_TAG}")
