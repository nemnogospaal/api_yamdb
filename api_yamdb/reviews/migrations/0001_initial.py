# Generated by Django 3.2 on 2023-11-19 04:28

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='имя пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('role', models.CharField(blank=True, choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=20, verbose_name='роль')),
                ('bio', models.CharField(blank=True, max_length=254, verbose_name='биография')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='имя')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='фамилия')),
                ('confirmation_code', models.CharField(max_length=255, null=True, verbose_name='Код подтверждения')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Hазвание')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Слаг категории содержит недопустимый символ', regex='^[-a-zA-Z0-9_]+$')], verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=75, verbose_name='Hазвание')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Слаг жанра содержит недопустимый символ', regex='^[-a-zA-Z0-9_]+$')], verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Соответствие жанра и произведения',
                'verbose_name_plural': 'Таблица соответствия жанров и произведений',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='Hазвание')),
                ('year', models.PositiveIntegerField(db_index=True, validators=[django.core.validators.MinValueValidator(0, message='Значение года не может быть отрицательным'), django.core.validators.MaxValueValidator(2023, message='Значение года не может быть больше текущего')], verbose_name='год выпуска')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='категория')),
                ('genre', models.ManyToManyField(related_name='titles', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('-year', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100, verbose_name='Текст отзыва')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')),
                ('score', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title', verbose_name='произведение'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=100, verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Коментарии',
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_author_title'),
        ),
    ]
