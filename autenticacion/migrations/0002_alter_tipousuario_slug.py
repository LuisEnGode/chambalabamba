from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(  # <-- AddField, no AlterField
            model_name='tipousuario',
            name='slug',
            field=models.SlugField(
                max_length=30,
                unique=True,
                blank=True,
                null=True,  # facilita migrar si hay datos previos
                help_text="Identificador único (ej. 'externo', 'residente').",
            ),
        ),
    ]
