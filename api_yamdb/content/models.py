from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.DateTimeField('Год выпуска', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='title'
    )
    #review = models.OneToOneField(
       # Review, on_delete=models.CASCADE, related_name='titles'
    #)

    def __str__(self):
        return self.name


