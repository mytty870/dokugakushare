from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Emailを入力してください')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

  email = models.EmailField('Eメールアドレス', unique=True)
  username = models.CharField('ユーザー名', max_length=30,)
  icon = models.ImageField('アイコン', blank=True, null=True)
  background_image = models.ImageField('ヘッダー画像', blank=True, null=True)
  is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
  )
  is_active = models.BooleanField(
        'active',
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
  )
  date_joined = models.DateTimeField('date joined', default=timezone.now)

  objects = CustomUserManager()

  EMAIL_FIELD = 'email'
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

