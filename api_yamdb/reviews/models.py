from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


USER = 'user'

MODERATOR = 'moderator'

ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]
TEXT_LOMIT = 30


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


class Review(models.Model):
    """Модель отзывов."""

    text = models.CharField(
        max_length=100,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )
    score = models.IntegerField(
        blank=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.text[:TEXT_LOMIT]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Модель комментариев."""

    text = models.CharField(
        max_length=100,
        verbose_name='Текст комментария',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    def __str__(self):
        return self.text[:TEXT_LOMIT]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


class Raiting(models.Model):
    raiting = models.IntegerField(
        blank=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'
