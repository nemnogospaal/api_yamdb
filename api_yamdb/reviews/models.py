from django.db import models
from django.contrib.auth.models import AbstractUser

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        max_length=150,
        verbose_name='имя пользователя',
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль',
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.CharField(
        max_length=254,
        verbose_name='биография',
        blank=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=255,
        null=True,
        blank=False
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
