from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from backend.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    USER_GENDER_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        ('', '-----')

    )
    username = models.CharField(verbose_name='Nickname', max_length=30, validators=[username_validator], unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(verbose_name='Имя', max_length=60, null=True)
    about_me = models.CharField(verbose_name='Обо мне', max_length=100, null=True)
    user_gender = models.CharField(verbose_name='Тип пользователя', choices=USER_GENDER_CHOICES,
                                   max_length=6, default='')
    birthday = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('email',)

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    text = models.TextField(verbose_name='Текст статьи', max_length=100)
    created_dt = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    user = models.ForeignKey(User, verbose_name='Автор', related_name='user_posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, verbose_name='Likes', related_name='user_likes')

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ('created_dt',)

    def __str__(self):
        return self.title
