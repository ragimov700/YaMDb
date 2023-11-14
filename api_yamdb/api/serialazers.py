from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для действий по жанрам."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для действий по категориям."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""

    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), many=False,
    )
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = SlugRelatedField(slug_field='name', read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Вы можете оставить только '
                '1 отзыв на одно и то же произведение!',
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review = SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `User`."""

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]

    def create(self, validated_data):
        return create_or_get(validated_data)


class CreationUserSerializer(serializers.Serializer):
    """Сериализатор для модели `User` для создания пользователя."""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator()],
    )

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError('Имя `me` нельзя использовать!')
        return username

    def create(self, validated_data):
        return create_or_get(validated_data)


class TokenSerializer(TokenObtainSerializer):
    """Сериализатор для выдачи токена."""

    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField(required=True)
        del self.fields["password"]

    def validate(self, data):
        try:
            user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            raise Http404(
                "Не найден пользователь или неправильный код подтверждения!",
            )
        if user.confirmation_code != data["confirmation_code"]:
            raise serializers.ValidationError("Неверный код!")
        return {'token': str(self.get_token(user))}


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор Профиля."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


def create_or_get(validated_data):
    """Функция для создания или получения пользователя."""
    try:
        user, created = User.objects.get_or_create(**validated_data)
    except IntegrityError:
        raise serializers.ValidationError(
            'Используйте другую почту или имя пользователя!',
        )
    return user
