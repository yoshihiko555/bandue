from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import os, uuid, logging

logger = logging.getLogger(__name__)

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

        return user

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


# class Message(models.Model):
#
#     content = models.TextField(_('Content'))
#     sender = models.ForeignKey('api.mUser', related_name='sender', on_delete=models.CASCADE)
#     receiver = models.ForeignKey('api.mUser', related_name='receiver', on_delete=models.CASCADE)
#     images = models.ImageField(_('Image'), upload_to=content_file_name, blank=True, null=True)
#     created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
#     is_opened = models.BooleanField(
#         _('Is Opened'),
#         default=False,
#         help_text=_(
#             'Designates whether this message was opened by reveiver'
#         ),
#     )
#
#     deleted = models.BooleanField(_('Delete Flag'), default=False)
#
#     def __str__(self):
#         return self.content


class HashTag(models.Model):

    title = models.CharField(_('Title'), max_length=30)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)
    slug = models.SlugField(_('Slug'), blank=True, null=True)

    def __str__(self):
        return self.title


class Tweet(models.Model):

    author = models.ForeignKey(mUser, on_delete=models.CASCADE, related_name='author')
    content = models.TextField(_('Content'))
    liked = models.ManyToManyField(mUser, blank=True, related_name='liked')
    hashTag = models.ManyToManyField(HashTag, blank=True)
    images = models.ImageField(_('Images'), upload_to=content_file_name, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upadate Date'), auto_now=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)
    retweet_user = models.ManyToManyField(mUser, related_name='tweet_retweet_user', blank=True)
    relation = models.OneToOneField('api.Retweet', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.content


class Retweet(models.Model):

    author = models.ForeignKey(mUser, on_delete=models.CASCADE, related_name='retweet_author')
    content = models.TextField(_('Content'))
    liked = models.ManyToManyField(mUser, blank=True, related_name='retweet_liked')
    hashTag = models.ManyToManyField(HashTag, blank=True)
    images = models.ImageField(_('Images'), upload_to=content_file_name, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upadate Date'), auto_now=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)
    retweet_user = models.ManyToManyField(mUser, related_name='retweet_retweet_user', blank=True)
    relation = models.OneToOneField('api.Tweet', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.content


class Reply(models.Model):

    author = models.ForeignKey(mUser, on_delete=models.CASCADE)
    target = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    content = models.TextField(_('Content'))
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


class Band(models.Model):

    name = models.CharField(_('Community Name'), max_length=100)
    members = models.ManyToManyField(
        mUser,
        through='MemberShip',
        through_fields=('band', 'muser'),
    )

    def __str__(self):
        return self.name


class MemberShip(models.Model):

    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    muser = models.ForeignKey(mUser, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        mUser,
        on_delete=models.CASCADE,
        related_name='membership_invites',
    )
    invite_reason = models.CharField(_('Invites Reason'), max_length=100)

    def __str__(self):
        return self.inviter.username + ' が ' + self.band.name + ' に ' + self.muser.username + ' を招待'

class Entry(models.Model):

    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField(_('Content'))
    author = models.ForeignKey(mUser, on_delete=models.CASCADE)
    ENTRY_TYPE_CHOICES = (
        ('RE', _('Recruitment Member')),
        ('JO', _('Join a Group')),
        ('SU', _('Support')),
    )
    type = models.CharField(choices=ENTRY_TYPE_CHOICES, max_length=30)
    PREFECTURE_CHOICES = (
        (1, _('Hokkaido')),
        (2, _('Aomori Prefecture')),
        (3, _('Iwate Prefecture')),
        (4, _('Miyagi Prefecture')),
        (5, _('Akita Prefecture')),
        (6, _('Yamagata Prefecture')),
        (7, _('Fukushima Prefecture')),
        (8, _('Ibaraki Prefecture')),
        (9, _('Tochigi Prefecture')),
        (10, _('Gunma Prefecture')),
        (11, _('Saitama Prefecture')),
        (12, _('Chiba Prefecture')),
        (13, _('Tokyo Prefecture')),
        (14, _('Kanagawa Prefecture')),
        (15, _('Niigata Prefecture')),
        (16, _('Toyama Prefecture')),
        (17, _('Ishikawa Prefecture')),
        (18, _('Fukui Prefecture')),
        (19, _('Yamanashi Prefecture')),
        (20, _('Nagano Prefecture')),
        (21, _('Gifu Prefecture')),
        (22, _('Shizuoka Prefecture')),
        (23, _('Aichi Prefecture')),
        (24, _('Mie Prefecture')),
        (25, _('Shiga Prefecture')),
        (26, _('Kyoto Prefecture')),
        (27, _('Osaka Prefecture')),
        (28, _('Hyogo Prefecture')),
        (29, _('Nara Prefecture')),
        (30, _('Wakayama Prefecture')),
        (31, _('Tottori Prefecture')),
        (32, _('Shimane Prefecture')),
        (33, _('Okayama Prefecture')),
        (34, _('Hiroshima Prefecture')),
        (35, _('Yamaguchi Prefecture')),
        (36, _('Tokushima Prefecture')),
        (37, _('Kagawa Prefecture')),
        (38, _('Ehime Prefecture')),
        (39, _('Kochi Prefecture')),
        (40, _('Fukuoka Prefecture')),
        (41, _('Saga Prefecture')),
        (42, _('Nagasaki Prefecture')),
        (43, _('Kumamoto Prefecture')),
        (44, _('Oita Prefecture')),
        (45, _('Miyazaki Prefecture')),
        (46, _('Kagoshima Prefecture')),
        (47, _('Okinawa Prefecture')),
    )
    prefecture = models.IntegerField(choices=PREFECTURE_CHOICES, null=True, blank=True)
    area = models.CharField(_('Area'), max_length=20 , null=True, blank=True)
    DAY_WEEK_CHOICES = (
        ('WD', _('Weekdays')),
        ('WE', _('Weekends')),
        ('AL', _('Always')),
    )
    day_week = models.CharField(choices=DAY_WEEK_CHOICES, max_length=20, null=True, blank=True)
    DIRECTION_CHOICES = (
        ('OR', _('Original')),
        ('CO', _('Copy')),
        ('AL', _('All')),
    )
    direction = models.CharField(choices=DIRECTION_CHOICES, max_length=20, null=True, blank=True)
    part = models.TextField(_('Part'), null=True, blank=True)
    genre = models.TextField(_('Genre'), null=True, blank=True)

    def __str__(self):
        return self.title

class Category(models.Model):

    name = models.CharField(_('Category'), max_length=50, default='未分類')
    created_by = models.ForeignKey(mUser, on_delete=models.CASCADE)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    slug = models.SlugField(default=name)

    def __str__(self):
        return self.name

class Tag(models.Model):

    name = models.CharField(_('Tag'), max_length=50)
    created_by = models.ForeignKey(mUser, on_delete=models.CASCADE)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    slug = models.SlugField(default=name)

    def __str__(self):
        return self.name

class Bbs(models.Model):

    writer = models.ForeignKey(mUser, on_delete=models.CASCADE, related_name='writer')
    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField(_('Content'))
    tag = models.ManyToManyField(Tag, blank=True)
    images = models.ImageField(_('Images'), upload_to=content_file_name, blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upadate Date'), auto_now=True)
    deleted = models.BooleanField(_('Delete Flag'), default=False)

    def __str__(self):
        return self.title

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    users = models.ManyToManyField(mUser)
    created_at = models.DateTimeField(_('Created At'), default=timezone.now)

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    sender = models.ForeignKey(mUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(mUser, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Image'), upload_to=content_file_name, blank=True, null=True)
    readed = models.BooleanField(_('Readed'), default=False)
    deleted = models.BooleanField(_('Deleted'), default=False)
    created_at = models.DateTimeField(_('Created At'), default=timezone.now)

    def __str__(self):
        return self.content

# 多分使わない(後で削除予定)
class mUser_Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(mUser, related_name='user_id', on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, related_name='room_id', on_delete=models.CASCADE)
