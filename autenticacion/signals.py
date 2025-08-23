# apps/autenticacion/signals.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_migrate, pre_save
from django.dispatch import receiver

from .models import TipoUsuario, PerfilUsuario

User = get_user_model()

ROLE_PREFIX = "role:"


def role_group_name(slug: str) -> str:
    return f"{ROLE_PREFIX}{slug}"


# ────────────────────────────────────────────────────────────────────────────────
# 1) Sembrar tipos base y sus grupos al migrar (externo / residente)
# ────────────────────────────────────────────────────────────────────────────────
@receiver(post_migrate)
def seed_tipos_and_groups(sender, **kwargs):
    # Evita correr para otras apps
    if getattr(sender, "name", "") != "autenticacion":
        return

    # Asegura tipos base
    externo, _ = TipoUsuario.objects.get_or_create(
        slug="externo",
        defaults={"nombre": "Externo", "descripcion": "Usuario externo por defecto"},
    )
    residente, _ = TipoUsuario.objects.get_or_create(
        slug="residente",
        defaults={"nombre": "Residente", "descripcion": "Usuario residente"},
    )

    # Asegura grupos por rol
    for tipo in (externo, residente):
        if not tipo.role_group:
            g, _ = Group.objects.get_or_create(name=role_group_name(tipo.slug))
            tipo.role_group = g
            tipo.save(update_fields=["role_group"])


# ────────────────────────────────────────────────────────────────────────────────
# 2) Asegurar que cada TipoUsuario tenga su Group (al crear/editar)
#    y renombrar el Group si cambia el slug
# ────────────────────────────────────────────────────────────────────────────────
@receiver(pre_save, sender=TipoUsuario)
def rename_group_if_slug_changes(sender, instance: TipoUsuario, **kwargs):
    if not instance.pk:
        return
    try:
        old = TipoUsuario.objects.get(pk=instance.pk)
    except TipoUsuario.DoesNotExist:
        return
    if old.slug != instance.slug and instance.role_group:
        # Renombra el grupo para reflejar el nuevo slug
        instance.role_group.name = role_group_name(instance.slug)
        instance.role_group.save(update_fields=["name"])


@receiver(post_save, sender=TipoUsuario)
def ensure_group_for_tipo(sender, instance: TipoUsuario, created, **kwargs):
    if not instance.role_group:
        g, _ = Group.objects.get_or_create(name=role_group_name(instance.slug))
        instance.role_group = g
        instance.save(update_fields=["role_group"])


# ────────────────────────────────────────────────────────────────────────────────
# 3) Crear PerfilUsuario automáticamente al crear un User
#    (queda por defecto con tipo 'externo' vía default del modelo)
# ────────────────────────────────────────────────────────────────────────────────
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance: User, created, **kwargs):
    if created:
        # El default del FK pone 'externo'
        PerfilUsuario.objects.get_or_create(user=instance)


# ────────────────────────────────────────────────────────────────────────────────
# 4) Sincronizar grupos del usuario cuando se guarda su Perfil
#    (quita cualquier "role:*" previo y añade el grupo del tipo actual)
# ────────────────────────────────────────────────────────────────────────────────
def _sync_user_role_group(user: User):
    # Quita todos los grupos de rol previos
    role_groups = Group.objects.filter(name__startswith=ROLE_PREFIX)
    if role_groups.exists():
        user.groups.remove(*role_groups)

    # Añade el grupo del tipo actual (si existe)
    try:
        perfil = user.perfilusuario  # related_name que tú mantuviste
    except PerfilUsuario.DoesNotExist:
        return
    if perfil.tipo_usuario and perfil.tipo_usuario.role_group:
        user.groups.add(perfil.tipo_usuario.role_group)


@receiver(post_save, sender=PerfilUsuario)
def sync_role_group_on_profile_save(sender, instance: PerfilUsuario, **kwargs):
    if instance.user_id:
        _sync_user_role_group(instance.user)
