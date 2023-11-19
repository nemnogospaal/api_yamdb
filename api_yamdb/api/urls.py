from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import APIGetToken, APISignup, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='token')
]
