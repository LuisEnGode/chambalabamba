import os
from pathlib import Path
from django.core.management import call_command
from django.db import connection, transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver

SEED_TAG = "donaciones:v1"   # súbelo a v2 cuando quieras resembrar

@receiver(post_migrate)
def _seed_donaciones_once(sender, **kwargs):
    # Solo cuando migra esta app
    if sender.name != "donaciones":
        return

    # Permite saltar fixtures en prod si lo necesitas
    if os.getenv("SKIP_FIXTURES", "0") == "1":
        print(f"[seed_donaciones] SKIP_FIXTURES=1 -> omitido {SEED_TAG}")
        return

    fixture_path = Path(__file__).resolve().parent / "fixtures" / "donaciones_home_callout.json"

    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_donaciones] Ya corrido {SEED_TAG}, no se recarga")
            return

        if not fixture_path.exists():
            print(f"[seed_donaciones] Fixture no encontrado: {fixture_path}")
            return

        call_command("loaddata", str(fixture_path), verbosity=0)
        print(f"[seed_donaciones] Cargado fixture: {fixture_path.name}")

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_donaciones] Marcado {SEED_TAG}")
