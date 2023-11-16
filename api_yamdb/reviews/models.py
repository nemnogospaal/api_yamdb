from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model() #Поменям на кастомные модели
TEXT_LOMIT = 30


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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )
    raiting = models.IntegerField(
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
    created_at = models.DateTimeField(
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
    title = models.CharField(max_length=100) # Поменяет на модели Ромы
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'
