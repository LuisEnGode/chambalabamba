from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

SEED_TAG = "nosotros:v1"  # súbelo a v2 cuando quieras resembrar

def _seed_nosotros_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_nosotros] Ya corrido {SEED_TAG}, no se recarga")
            return

        # Ruta absoluta al fixture para evitar problemas de búsqueda
        fixture_path = Path(__file__).resolve().parent / "fixtures" / "nosotros.json"
        call_command("loaddata", str(fixture_path), verbosity=0)
        print(f"[seed_nosotros] Cargado fixture: {fixture_path.name}")

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_nosotros] Marcado {SEED_TAG}")
