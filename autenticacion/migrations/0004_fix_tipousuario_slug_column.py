from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('autenticacion', '0001_initial'),
    ]
    operations = [
        migrations.RunSQL(
            sql=("ALTER TABLE autenticacion_tipousuario "
                 "ADD COLUMN IF NOT EXISTS slug varchar(30);"),
            reverse_sql=("ALTER TABLE autenticacion_tipousuario "
                         "DROP COLUMN IF EXISTS slug;"),
        ),
        migrations.RunSQL(
            sql=("DO $$ BEGIN "
                 "IF NOT EXISTS (SELECT 1 FROM pg_constraint "
                 "WHERE conname = 'autenticacion_tipousuario_slug_key') THEN "
                 "ALTER TABLE autenticacion_tipousuario "
                 "ADD CONSTRAINT autenticacion_tipousuario_slug_key UNIQUE (slug); "
                 "END IF; END $$;"),
            reverse_sql=("ALTER TABLE autenticacion_tipousuario "
                         "DROP CONSTRAINT IF EXISTS autenticacion_tipousuario_slug_key;"),
        ),
    ]
