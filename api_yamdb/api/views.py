from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetOnlyTitleSerializer,
                             GetTokenSerializer, ReviewSerializer,
                             SignUpSerializer, TitleSerializer,
                             UserPatchSerializer, UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReading, IsAdminModAuthorOrReading


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModAuthorOrReading,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModAuthorOrReading, )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                review=self.get_review()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    """Вьюсет для пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsAdmin,)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    #try:
    user, _ = User.objects.get_or_create(
        username=username,
        email=email)
    #except IntegrityError:
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(
        subject='YaMDB - Код подтверждения',
                message=f'Код подтверждения - {confirmation_code}',
                from_email='YaMDB@mail.com',
                recipient_list=[user.email,],
                fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    """Получение токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'Токен': str(token)},
                            status=status.HTTP_200_OK)
        return Response(
            {'Токен': 'Неверный токен'},
            status=status.HTTP_400_BAD_REQUEST)



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
        if self.request.method == 'GET':
            return GetOnlyTitleSerializer
        return TitleSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)