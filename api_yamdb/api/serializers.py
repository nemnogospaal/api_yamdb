import re

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User
from api.validators import username_me_validator, username_validator


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


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254,
                                   required=True)
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[username_validator,
                                                 username_me_validator])

    def validate(self, data):
        username = data.get('username')
        if not User.objects.filter(
            username=(data.get('username')), email=(data.get('email'))
        ).exists():
            if User.objects.filter(username=(data.get('username'))):
                raise serializers.ValidationError('Данный username уже занят')
            if User.objects.filter(email=data.get('email')):
                raise serializers.ValidationError('Данный email уже занят')
            if re.search(r'^[\w.@+-]+\Z', str(username)) is None:
                raise serializers.ValidationError(
                    'Недопустимые символы в логине')
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[username_validator,
                                                 username_me_validator])
    confirmation_code = serializers.CharField(required=True,
                                              max_length=254)


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
