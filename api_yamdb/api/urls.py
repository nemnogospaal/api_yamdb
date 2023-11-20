from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (APIGetToken, APISignup, UserViewSet, ReviewViewSet,
                       CommentViewSet, GenreViewSet, TitleViewSet,
                       CategoryViewSet)
                       

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='token')
]