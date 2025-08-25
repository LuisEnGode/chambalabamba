from django.db import migrations
from django.utils.text import slugify

def backfill_slugs(apps, schema_editor):
    TipoUsuario = apps.get_model('autenticacion', 'TipoUsuario')
    for tu in TipoUsuario.objects.all():
        # Si la columna existe pero está vacía, la rellenamos
        if not getattr(tu, 'slug', None):
            base = slugify(tu.nombre) or "tipo"
            slug = base
            i = 1
            while TipoUsuario.objects.filter(slug=slug).exclude(pk=tu.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            tu.slug = slug
            tu.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0001_initial'),  # que se ejecute después de la inicial
    ]

    operations = [
        # 1) Crear columna si no existe (PostgreSQL)
        migrations.RunSQL(
            sql=(
                "ALTER TABLE autenticacion_tipousuario "
                "ADD COLUMN IF NOT EXISTS slug varchar(30);"
            ),
            reverse_sql=(
                "ALTER TABLE autenticacion_tipousuario "
                "DROP COLUMN IF EXISTS slug;"
            ),
        ),
        # 2) Asegurar UNIQUE si no existe (PostgreSQL no tiene IF NOT EXISTS para constraints)
        migrations.RunSQL(
            sql=(
                "DO $$ BEGIN "
                "IF NOT EXISTS (SELECT 1 FROM pg_constraint "
                "WHERE conname = 'autenticacion_tipousuario_slug_key') THEN "
                "ALTER TABLE autenticacion_tipousuario "
                "ADD CONSTRAINT autenticacion_tipousuario_slug_key UNIQUE (slug); "
                "END IF; "
                "END $$;"
            ),
            reverse_sql=(
                "ALTER TABLE autenticacion_tipousuario "
                "DROP CONSTRAINT IF EXISTS autenticacion_tipousuario_slug_key;"
            ),
        ),
        # 3) Rellenar datos
        migrations.RunPython(backfill_slugs, migrations.RunPython.noop),
    ]
