from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import os, uuid, logging


def content_file_name(instance, filename):
    return 'upload/{0}/{1}/{2}'.format(instance.author, instance.title, filename)

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('ユーザーネームは必須項目です。')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class mUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('Username'), max_length=70, unique=True)
    email = models.EmailField(_('Email'), max_length=70, unique=True)

    address = models.CharField(_('Address'), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    deleted = models.BooleanField(
        _('Delete Flag'),
        default=False,
        help_text=_(
            'Designates whether the user was deleted or not'
        )
    )

    thumbnail = models.ImageField(_('Thumbnail'), upload_to=content_file_name, blank=True, null=True)

    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('Active Flag'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_limited = models.BooleanField(
        _('Limited Flag'),
        default=False,
        help_text=_(
            'Designates whether this user limit the view of the tweet'
        ),
    )

    introduction = models.TextField(_('Introduction'), blank=True, null=True)

    icon = models.ImageField(_('Icon'), upload_to=content_file_name, blank=True, null=True)

    followees = models.ManyToManyField('self', blank=True, symmetrical=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Message(models.Model):

    content = models.TextField(_('Content'))
    sender = models.ForeignKey('api.mUser', related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey('api.mUser', related_name='receiver', on_delete=models.CASCADE)
    images = models.ImageField(_('Image'), upload_to=content_file_name, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_opened = models.BooleanField(
        _('Is Opened'),
        default=False,
        help_text=_(
            'Designates whether this message was opened by reveiver'
        ),
    )

    deleted = models.BooleanField(_('Delete Flag'), default=False)

    def __str__(self):
        return self.content


class HashTag(models.Model):

    title = models.CharField(_('Title'), max_length=30)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)
    slug = models.SlugField(_('Slug'), blank=True, null=True)

    def __str__(self):
        return self.title


class Tweet(models.Model):

    author = models.ForeignKey(mUser, on_delete=models.CASCADE)
    content = models.TextField(_('Content'))
    liked = models.PositiveIntegerField(_('Liked'), default=0)
    hashTag = models.ManyToManyField(HashTag, blank=True)
    images = models.ImageField(_('Images'), upload_to=content_file_name, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upadate Date'), auto_now=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)

    def __str__(self):
        return self.content


class Reply(models.Model):

    content = models.TextField(_('Content'))
    author = models.ForeignKey(mUser, on_delete=models.CASCADE)
    target = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)

    def __str__(self):
        return self.content


class mSetting(models.Model):

    TWEET_LIMIT_LEVEL_CHOICES = (
        (1, _('Public')),
        (2, _('Follower')),
        (3, _('Follower Who Follow Each Other')),
    )
    LANGUAGE_CHOICES = (
        ('JA', _('Japanese')),
        ('EN', _('English')),
        ('FR', _('French')),
        ('GE', _('German')),
    )
    tweet_limit_level = models.IntegerField(choices=TWEET_LIMIT_LEVEL_CHOICES)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    target = models.ForeignKey(mUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.target.username


class hUserUpd(models.Model):

    username = models.CharField(_('Username'), max_length=70, unique=True)
    email = models.EmailField(_('Email'), max_length=70, unique=True)
    password = models.CharField(_('Password'), max_length=128)
    address = models.CharField(_('Address'), max_length=100, blank=True)
    updated_at = models.DateTimeField(_('Upadate Date'), auto_now=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)

    def __str__(self):
        return self.username


class hTweetUpd(models.Model):

    content = models.TextField(_('Content'))
    hashTag = models.ManyToManyField(HashTag, blank=True)
    images = models.ImageField(_('Images'), upload_to=content_file_name, blank=True, null=True)
    updated_at = models.DateTimeField(_('Upadate Date'), auto_now=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)

    def __str__(self):
        return self.content


class mAccessLog(models.Model):

    uuid = models.UUIDField(_('Uuid'), editable=False, blank=True, null=True)
    ip = models.GenericIPAddressField(_('IP Address'), unpack_ipv4=True, blank=True, null=True)
    device = models.CharField(_('Device'), max_length=50)
    page = models.URLField(_('Page'), max_length=500)
    browser = models.CharField(_('Browser'), max_length=50)
    time = models.DateTimeField(_('Access Time'), auto_now_add=True)
    language = models.CharField(_('Language'), max_length=30)


class Group(models.Model):

    name = models.CharField(_('Community Name'), max_length=100)
    members = models.ManyToManyField(
        mUser,
        through='MemberShip',
        through_fields=('group', 'muser'),
    )


class MemberShip(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    muser = models.ForeignKey(mUser, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        mUser,
        on_delete=models.CASCADE,
        related_name='membership_invites',
    )
    invite_reason = models.CharField(_('Invites Reason'), max_length=100)
