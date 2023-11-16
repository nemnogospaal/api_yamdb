from rest_framework import viewsets

from content.models import Title, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from .permissions import OwnerOrReadOnly

class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (OwnerOrReadOnly, )

    def get_gueryset(self):
        return Title.objects.select_related('category', 'author')


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (OwnerOrReadOnly, )

    def get_gueryset(self):
        return Title.objects.select_related('title')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (OwnerOrReadOnly, )
    queryset = Category.objects.all()