import json, datetime, pathlib
p = pathlib.Path("proyectos/fixtures/proyectos_all.json")
data = json.loads(p.read_text(encoding="utf-8"))
now = datetime.datetime.now().isoformat(timespec="seconds")
changed = 0

for obj in data:
    mdl = obj.get("model","")
    if mdl in ("proyectos.project", "proyectos.projectphoto"):
        f = obj.setdefault("fields", {})
        if "creado" not in f or not f["creado"]:
            f["creado"] = now
            changed += 1
        if "actualizado" not in f or not f["actualizado"]:
            f["actualizado"] = now
            changed += 1

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: timestamps añadidos/normalizados en {changed} campos.")
PY
