from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
# from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
# from rest_framework.permissions import AllowAny
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


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #username = serializer.validated_data.get('username')
            #email = serializer.validated_data.get('email')
            #user = get_object_or_404(User, username=username, email=email)
            #confirmation_code = default_token_generator.make_token(user)
            user = serializer.save()
            send_mail(
                subject='YaMDB - Код подтверждения',
                message=f'Код подтверждения - {user.confirmation_code}',
                from_email='YaMDB@mail.com',
                recipient_list=(user.email,),
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        #if serializer.is_valid():
        #    username = serializer.validated_data.get('username')
        #    email = serializer.validated_data.get('email')
        #    user = get_object_or_404(User, username=username, email=email)
        #    confirmation_code = default_token_generator.make_token(user)
            #send_mail(
            #    subject='YaMDB - Код подтверждения',
            #    message=f'Код подтверждения - {confirmation_code}',
            #    from_email='YaMDB@mail.com',
            #    recipient_list=(email,),
            #    fail_silently=False
           #)
        #    user.save()
        #    return Response(serializer.data, status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        


# не рабочий?
        #serializer = SignUpSerializer(data=request.data)
        #serializer.is_valid()
        #username = serializer.validated_data.get('username')
        #email = serializer.validated_data.get('email')
        #user = get_object_or_404(User, username=username, email=email)
        #confirmation_code = default_token_generator.make_token(user)
        #send_mail(
        #    subject='YaMDB confirmation',
        #    message=f'Ваш код подтверждения - {confirmation_code}',
        #    from_email='YaMDB@mail.com',
        #    recipient_list=(email,)
        #)
        #return Response(serializer.data, status=status.HTTP_200_OK)

# вариант работает только на валиадацию
        #serializer = SignUpSerializer(data=request.data)
        #if not serializer.is_valid():
        #    return Response(serializer.errors,
        #                    status=status.HTTP_400_BAD_REQUEST)
        #username = serializer.validated_data.get('username')
        #email = serializer.validated_data.get('email')
        #user = User.objects.get_or_create(
        #    username=username,
        #    email=email)
        #confirmation_code = default_token_generator.make_token(user)
        #send_mail(
        #    subject='YaMDB - код для подтверждения',
        #    message=f'Ваш код подтверждения - {confirmation_code}',
        #    from_email='YaMDB@yandex.ru',
        #    recipient_list=(email,),
        #    fail_silently=True,
        #)
        #return Response(serializer.data, status=status.HTTP_200_OK)
      

class APIGetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except ValueError:
            return Response(serializer.errors,
                            status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неправильный код'},
            status=status.HTTP_400_BAD_REQUEST
        )
        #username = serializer.validated_data.get('username')
        #confirmation_code = serializer.validated_data.get(
        #    'confirmation_code')
        #user = get_object_or_404(User, username=username)
        #if default_token_generator.check_token(
        #    user, confirmation_code
        #):
        #    token = str(RefreshToken.for_user(user).access_token)
        #    return Response({'token': token},
        #                    status=status.HTTP_201_CREATED)
        #return Response(
        #    {'error': 'Код подтверждения'},
        #    status=status.HTTP_400_BAD_REQUEST
        #)



    #def post(self, request):
    #    serializer = GetTokenSerializer(data=request.data)
    #    serializer.is_valid()
    #    username = serializer.validated_data.get('username')
    #    confirmation_code = serializer.validated_data.get('confirmation_code')
    #    user = get_object_or_404(User, username=username)
    #    if confirmation_code == user.confirmation_code:
    #        token = str(AccessToken.for_user(user))
    #        return Response({'token': token}, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


        #if not serializer.is_valid():
         #   return Response(serializer.errors,
          #                  status=status.HTTP_400_BAD_REQUEST)
        #data = serializer.validated_data
        #user = User.objects.get(username=data['username'])
        #confirmation_code = data.get('username')
        #user = get_object_or_404(User, username=username)
        #if user.confirmation_code != confirmation_code:
         #   return Response(
          #      {'confirmation_code': ['Неверный код подтверждения']},
           #     status=status.HTTP_400_BAD_REQUEST
            #)
        #else:
         #   token = str(RefreshToken.for_user(user).access_token)
          #  return Response({'token': str(token)},
           #                 status=status.HTTP_201_CREATED)


