import re

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'bio', 'first_name', 'last_name')

    def validate(self, data):
        username = data.get('username')
        if re.search(r'^[\w.@+-]+\Z', str(username)) is None:
            raise serializers.ValidationError(
                'Недопустимые символы в логине'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254,
                                   required=True)
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Невозможно использовать такой логин'
            )
        username = data.get('username')
        email = data.get('email')
        #try:
        #    user, _ = User.objects.get_or_create(username=username,
        #                                         email=email)
        #except IntegrityError:
        #    raise serializers.ValidationError('Этот логин или email уже занят')
            
        if re.search(r'^[\w.@+-]+\Z', str(username)) is None:
            raise serializers.ValidationError('Недопустимые символы в логине')
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserPatchSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+\Z',
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role',
            'bio', 'first_name', 'last_name'
        )
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""

    author = serializers.StringRelatedField(
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class GetOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
