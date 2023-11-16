from django.urls import include, path
from rest_framework import routers
from .views import TitleViewSet, CategoryViewSet, GenreViewSet


router = routers.DefaultRouter()
router.register(r'title', TitleViewSet, basename='title')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'genre', GenreViewSet, basename='genre')


urlpatterns = [
    path('v1/', include(router.urls)),
]