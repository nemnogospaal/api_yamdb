from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import (CategoryViewSet, CommentViewSet, CreateUserViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet,
                    UserValidationViewSet, UserViewSet)

router = DefaultRouter()


router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'auth/signup', CreateUserViewSet, basename='signup')
router.register(r'auth/token', UserValidationViewSet, basename='activate')
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path(
        'v1/token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path('v1/', include(router.urls))
]