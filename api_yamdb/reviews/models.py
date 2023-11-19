from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
USER_ROLES = [
    (ADMIN, 'Admin role'),
    (USER, 'User role'),
    (MODERATOR, 'Moderator role')]


class User(AbstractUser):

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        null=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        'Элетронная почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=USER_ROLES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    password = models.TextField(
        'Пароль',
        blank=True,
    )
    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator_or_admin(self):
        return self.role == MODERATOR or self.is_admin

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=50
    )
    year = models.IntegerField(
        'Год производства'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        'Рейтинг',
        null=True,
        default=None
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.category}'


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата пуликации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:10]

