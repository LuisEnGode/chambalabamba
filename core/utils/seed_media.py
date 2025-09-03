# core/utils/seed_media.py
from pathlib import Path
from shutil import copy2
from django.conf import settings

DEFAULT_PAIRS = [
    (Path("eventos/static/images"), Path("images")),
    (Path("nosotros/static/nosotros/images"), Path("nosotros")),
]

def copy_seed_media(pairs=DEFAULT_PAIRS, force=False) -> int:
    base = Path(settings.BASE_DIR)
    media = Path(settings.MEDIA_ROOT)
    media.mkdir(parents=True, exist_ok=True)

    total = 0
    for src_rel, dst_rel in pairs:
        src = base / src_rel
        dst = media / dst_rel
        if not src.exists():
            continue
        dst.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*"):
            if f.is_file():
                target = dst / f.name
                if target.exists() and not force:
                    continue
                copy2(f, target)
                total += 1
    return total

