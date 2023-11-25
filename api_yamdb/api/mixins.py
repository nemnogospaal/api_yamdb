from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReading


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    '''Кастомный класс для моделей Category и Genre:
    получение списка, создание и удаление элемента.'''

    permission_classes = (IsAdminOrReading,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
