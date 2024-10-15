from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.contrib.auth.models import Group as OriginalGroup
from django.db.models.signals import pre_delete, post_save
from django.contrib.auth.validators import UnicodeUsernameValidator
# from auditlog.registry import auditlog
from .managers import CustomUserManager

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(
        "username",
        max_length=150,
        help_text="Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_",
        validators=[username_validator],
        error_messages={
            "unique": "Ya existe un usuario con ese nombre de usuario.",
        },
    )

    # Sobrescribimos los campos para añadir un related_name
    groups = models.ManyToManyField(
        OriginalGroup,
        related_name='custom_user_groups',  # Cambia esto por un nombre único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Cambia esto por un nombre único
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    @property
    def nombre_completo(self):
        try:
            return self.nombre_completo
        except:
            return self.email

    def __str__(self):
        return self.nombre_completo

    @staticmethod
    @receiver(pre_delete, sender='users.User')
    def safe_delete_usuario(sender, instance, **kwargs):
        instance.safe_delete = True
        instance.save()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Group(OriginalGroup):
    class Meta:
        proxy = True
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

