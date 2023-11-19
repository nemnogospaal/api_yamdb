from rest_framework import serializers
from reviews.models import Comment, Review


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
