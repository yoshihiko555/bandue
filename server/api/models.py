from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import os, uuid, logging


logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('ユーザーネームは必須項目です')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.serdefault('is_staff', False)
        extra_fields.serdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)

class mUser(AbstractBaseUser, PermissionsMixin):
    '''カスタムユーザーモデル'''

    username = models.CharField(_('Username'), max_length=70, unique=True)
    email = models.EmailField(_('Email'), unique=True)
    # address = models.CharField(_('Address'), max_length=100)
    # favorite = models.ManyToManyField(Tweet, blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('actice'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
