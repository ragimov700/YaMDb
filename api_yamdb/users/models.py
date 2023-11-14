from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Кастомная модель `User`."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    email = models.EmailField(_('почта'), max_length=254)
    bio = models.TextField(_('биография'), blank=True)
    role = models.CharField(
        _('роль'),
        max_length=11,
        choices=ROLES_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Код для регистрации',
        max_length=200,
        editable=False,
        blank=True,
        unique=True,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
