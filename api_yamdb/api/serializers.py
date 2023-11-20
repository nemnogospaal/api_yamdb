import re

from rest_framework import serializers
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


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254,
                                   required=True)
    username = serializers.CharField(max_length=150,
                                     required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Невозможно использовать такой логин'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Данный логин уже занят'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Данный email уже занят'
            )
        username = data.get('username')
        if re.search(r'^[\w.@+-]+\Z', str(username)) is None:
            raise serializers.ValidationError('Недопустимые символы в логине')
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
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


class ReviewSerializer(serializers.ModelField):
    """Сериализатор модели отзывов."""

    class Meta:
        model = Review
        fields = ('_all__', )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""

    class Meta:
        model = Comment
        fields = ('_all__',)


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
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class GetOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
