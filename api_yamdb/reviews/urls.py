from django.urls import path

from api.views import signup, APIGetToken

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', APIGetToken.as_view(), name='token')
]
