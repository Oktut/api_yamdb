from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_correct_username, validate_year

USER_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

validate_username = UnicodeUsernameValidator()


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнэйм пользователя',
        validators=[validate_correct_username, validate_username],
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        verbose_name='Почта пользователя',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=16,
        choices=USER_ROLES,
        default='user',
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=255,
        null=True,
        blank=False
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.IntegerField(verbose_name='Год выпуска',
                               validators=[validate_year])
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        default_related_name = 'titles'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='text')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарии',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )
