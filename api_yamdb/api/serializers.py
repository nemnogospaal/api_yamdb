from rest_framework import serializers

from reviews.models import User, Comment, Review


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'bio', 'first_name', 'last_name', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Невозможно использовать такой логин'
            )
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelField):
    """Сериализатор модели отзывов."""

    class Meta:
        model = Review
        fields = ('_all__', )


class CommentSerializer(serializers.ModelField):
    """Сериализатор модели комментариев."""

    class Meta:
        model = Comment
        fields = ('_all__', )