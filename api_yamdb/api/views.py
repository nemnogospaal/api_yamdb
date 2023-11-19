from rest_framework.viewsets import ModelViewSet

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Comment, Review


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
