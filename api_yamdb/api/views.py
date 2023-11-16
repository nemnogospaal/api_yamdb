from rest_framework import viewsets

from content.models import Title, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer

    def get_gueryset(self):
        return Title.objects.select_related('category', 'author')


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer

    def get_gueryset(self):
        return Title.objects.select_related('title')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()