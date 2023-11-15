from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import (UserSerializer,
                          SignUpSerializer,
                          GetTokenSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class Signup(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to']]
        )
#добавить mail конфигурации в settings

class GetToken(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        user = User.objects.get(username=data['username'])
        confirmation_code = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {'confirmation_code': ['Неверный код подтверждения']},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)


