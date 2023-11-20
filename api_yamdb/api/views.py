from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import CreateListDestroyViewSet
from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminModAuthorOrReading, IsAdminOrReading
from reviews.models import (User, Comment, Review,
                            Category, Genre, Title)

from api.serializers import (GetTokenSerializer, SignUpSerializer,
                             UserSerializer, CommentSerializer,
                             ReviewSerializer, GenreSerializer,
                             TitleSerializer, GetOnlyTitleSerializer,
                             CategorySerializer)


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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


class APIGetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
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


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReading,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetOnlyTitleSerializer
        return TitleSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)