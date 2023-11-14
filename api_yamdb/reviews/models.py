from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True,
                                       verbose_name='Год выпуска',
                                       validators=(validate_year,))
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='Категория',
                                 null=True, blank=True)

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    pub_date = models.DateTimeField(default=datetime.now)
    score = models.IntegerField(validators=(MinValueValidator(1),
                                            MaxValueValidator(10)))

    class Meta:
        constraints = [UniqueConstraint(fields=['author', 'title'],
                                        name='unique_review')]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
