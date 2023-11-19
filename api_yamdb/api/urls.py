from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import APIGetToken, APISignup, UserViewSet, ReviewViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='token')
]