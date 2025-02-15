from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from api.validators import (USERNAME_ME_REGEX, USERNAME_SYMBOLS_REGEX,
                            username_me_validator, username_validator)

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


TEXT_LOMIT = 30


class User(AbstractUser):
    """Модель пользователя."""

    ROLE_CHOICES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )

    username = models.CharField(
        max_length=150,
        verbose_name='имя пользователя',
        validators=(USERNAME_ME_REGEX, USERNAME_SYMBOLS_REGEX,
                    username_me_validator, username_validator),
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль',
        blank=True,
        choices=ROLE_CHOICES,
        default=USER
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
        max_length=254,
        verbose_name='код подтверждения',
        blank=True
    )

    @property
    def is_moderator(self):
        return (self.role == MODERATOR
                or self.is_staff)

    @property
    def is_admin(self):
        return (self.role == ADMIN
                or self.is_superuser or self.is_staff)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    """Класс категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категории содержит недопустимый символ'
        )]
    )

    def __str__(self):
        return self.name[:TEXT_LOMIT]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    """Класс жанров."""

    name = models.CharField(
        max_length=75,
        verbose_name='Hазвание',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

    def __str__(self):
        return self.name[:TEXT_LOMIT]

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=150,
        verbose_name='Hазвание',
        db_index=True
    )
    year = models.PositiveIntegerField(
        verbose_name='год выпуска',
        validators=[
            MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
        db_index=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='жанр'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True
    )
    rating = models.IntegerField(
        'Рейтинг',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name[:TEXT_LOMIT]

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class GenreTitle(models.Model):
    """Вспомогательный класс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'
        ordering = ('id',)


class Review(models.Model):
    """Модель отзывов."""

    text = models.TextField(
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
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )

    def __str__(self):
        return self.text[:TEXT_LOMIT]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(models.Model):
    """Модель комментариев."""

    text = models.TextField(
        max_length=100,
        verbose_name='Текст комментария'
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
    review = models.ForeignKey(
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
