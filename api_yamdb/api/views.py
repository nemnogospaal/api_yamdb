from django.core.mail import EmailMessage
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import ADMIN, Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdmin, IsAdminModAuthorOrReading, IsAdminOrReading
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationSerializer, GenreSerializer,
                          GetOnlyTitleSerializer, ReviewSerializer,
                          SignupSerializer, TitleSerializer, UserSerializer)
from .tokens import account_activation_token

CONFIRMATION_CODE = 'Код регистрации аккаунта'
WRONG_CODE = 'Неверный код активации'
USERNAME_EXISTS = 'Username уже есть в базе'
EMAIL_EXISTS = 'Email уже есть в базе'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def users_profile(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username)
        if request.method != 'PATCH':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.user.role == ADMIN or self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email').lower()
        if User.objects.filter(username=username).exists():
            return Response(
                USERNAME_EXISTS,
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                EMAIL_EXISTS,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(username=username, email=email)
        user.is_active = False
        user.save()
        message = account_activation_token.make_token(user)
        email = EmailMessage(
            CONFIRMATION_CODE,
            message,
            to=[serializer.validated_data.get('email')]
        )
        email.send()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserValidationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'))
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if (not account_activation_token.check_token(
                user,
                confirmation_code)):
            return Response(
                WRONG_CODE,
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response(
            {
                'token': f'{token}'
            },
            status=status.HTTP_200_OK
        )


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModAuthorOrReading,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


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


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModAuthorOrReading,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )