from rest_framework import serializers
from .models import (
    mUser,
    HashTag,
    Tweet,
    mSetting,
    hUserUpd,
    hTweetUpd,
    mAccessLog,
    Entry,
    Room,
    Message,
    Age,
    ReadManagement,
    FollowRelationShip,
    RetweetRelationShip,
    Notification,
    MessageNotification,
    ReplyRelationShip,
    FollowRequest,
)
from rest_framework.renderers import JSONRenderer

import logging
from datetime import (
    timezone,
    datetime,
    timedelta
)
import pytz
from django.templatetags.i18n import language
from idlelib.idle_test.test_colorizer import source
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .utils import (
    search_retweet_target,
    search_reply_target,
    search_retweet_reply_target,
    search_reply_target_base,
    search_retweet_reply_target_base,
    is_base_tweet,
)

logging.basicConfig(
    level = logging.DEBUG,
    format = '''%(levelname)s %(asctime)s %(pathname)s:%(funcName)s:%(lineno)s
    %(message)s''')


logger = logging.getLogger(__name__)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):

        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProfileSubSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = mUser
        fields = [
            'pk',
            'username',
            'email',
            'address',
            'created_at',
            'header',
            'introduction',
            'icon',
        ]



class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = [
            'id',
            'title',
            'created_at',
            'slug',
        ]



class ProfileSerializer(DynamicFieldsModelSerializer):
    """
    プロフィールのシリアライザー

        Fields
        -------------------------------------
        followees : フォローしているユーザー一覧
        followers : フォローされているユーザー一覧
        isBlocked : ブロックされているか
        isBlock : ブロックしたユーザーか
        isSendFollowRequest : フォロー申請を送っている状態か
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)

    followees = ProfileSubSerializer(many=True)
    followers = serializers.SerializerMethodField()
    followees_count = serializers.IntegerField(source='followees.count')
    followers_count = serializers.SerializerMethodField()
    tweet = serializers.SerializerMethodField()
    entry = serializers.SerializerMethodField()
    setting = serializers.SerializerMethodField()
    tweet_limit_level = serializers.SerializerMethodField(read_only=True)
    isBlocked = serializers.SerializerMethodField(read_only=True)
    isPrivate = serializers.SerializerMethodField(read_only=True)
    isMute = serializers.SerializerMethodField(read_only=True)
    isBlock = serializers.SerializerMethodField(read_only=True)
    isFollow = serializers.SerializerMethodField(read_only=True)
    isSendFollowRequest = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user() if 'context' in kwargs else None
        super().__init__(*args, **kwargs)

    class Meta:
        model = mUser
        fields = [
            'pk',
            'username',
            'email',
            'password',
            'address',
            'created_at',
            'header',
            'introduction',
            'icon',
            'followees',
            'followers',
            'followees_count',
            'followers_count',
            'tweet',
            'entry',
            'setting',
            'tweet_limit_level',
            'isBlocked',
            'isPrivate',
            'isMute',
            'isBlock',
            'isFollow',
            'isSendFollowRequest',
        ]

    def get_followers(self, obj):
        return ProfileSubSerializer(mUser.objects.filter(followees=obj), many=True).data

    def get_followers_count(self, obj):
        return len(self.get_followers(obj)) if self.get_followers(obj) != None else 0

    def get_tweet(self, obj):
        return TweetSerializer(Tweet.objects.filter(author=obj), many=True).data

    def get_entry(self, obj):
        return EntrySerializer(Entry.objects.filter(author=obj), many=True).data

    def get_setting(self, obj):
        try:
            return MSettingSerializer(mSetting.objects.get(target=obj)).data
        except mSetting.DoesNotExist:
            return None


    def get_tweet_limit_level(self, obj):
        """
        ツイート公開レベルを取得するメソッド
            0: 公開
            1: ブロックモーダル表示
            2: 非公開
            3: ブロックモーダル表示（block & private)
        """

        if self.login_user == None or obj.username == self.login_user:
            return 0

        isBlocked = obj.msetting.block_list.filter(username=self.login_user).exists()
        isPrivate = obj.msetting.isPrivate

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return 0

        isFollow = login_user.followees.filter(username=obj.username).exists()

        if isPrivate:
            if isFollow:
                return 0
            if isBlocked:
                return 3
            return 2

        if isBlocked:
            return 1

        return 0


    def get_isBlocked(self, obj):

        if self.login_user == None:
            return False

        return obj.msetting.block_list.filter(username=self.login_user).exists()


    def get_isPrivate(self, obj):

        if self.login_user == None:
            return False

        return obj.msetting.isPrivate

    def get_isMute(self, obj):

        if self.login_user == None:
            return False

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return False

        return login_user.msetting.mute_list.filter(username=obj.username).exists()


    def get_isBlock(self, obj):

        if self.login_user == None:
            return False

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return False

        return login_user.msetting.block_list.filter(username=obj.username).exists()


    def get_isFollow(self, obj):

        if self.login_user == None:
            return False

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return False

        return login_user.followees.filter(username=obj.username).exists()

    def get_isSendFollowRequest(self, obj):

        if self.login_user == None:
            return False

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return False

        return FollowRequest.objects.filter(
            follow_request_user=login_user,
            follow_response_user=obj,
            isAccepted=False,
        ).exists()


    def create(self, validated_data):
        return mUser.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])


class TweetSerializer(DynamicFieldsModelSerializer):
    """
    ツイートのシリアライザー

        Fields
        --------------------------------------------------
        isLiked : 表示したユーザーが既にいいねしているかどうか
        isRetweet : リツイートかどうか
        isRetweeted : 表示したユーザーが既にリツイートしているかどうか
        followees_in_retweet_users : フォローしている人がリツイートユーザーにいたら取得
        followees_in_liked : フォローしている人がいいねしたユーザーにいたら取得
        isSendFollowRequest : フォロー申請を送っている状態か
    """

    author = serializers.ReadOnlyField(source='author.username')
    author_pk = serializers.CharField(required=False)
    hashTag = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    isFollow = serializers.SerializerMethodField()
    isMyself = serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    isRetweeted = serializers.SerializerMethodField()
    retweet = serializers.SerializerMethodField()
    retweet_count = serializers.SerializerMethodField()
    retweet_user = serializers.SerializerMethodField()
    retweet_users = serializers.SerializerMethodField()
    followees_in_retweet_users = serializers.SerializerMethodField()
    followees_in_liked = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    userIcon = serializers.SerializerMethodField()
    isBlocked = serializers.SerializerMethodField(read_only=True)
    isSendFollowRequest = serializers.SerializerMethodField(read_only=True)


    def __init__(self, *args, **kwargs):
        if 'context' in kwargs:
            self.login_user = kwargs['context']['view'].get_login_user()
            self.v = kwargs['context']['view']
        else:
            self.login_user = None

        super().__init__(*args, **kwargs)

    class Meta:
        model = Tweet
        fields = [
            'pk',
            'author',
            'author_pk',
            'content',
            'liked',
            'liked_count',
            'isLiked',
            'isFollow',
            'isMyself',
            'hashTag',
            'images',
            'created_at',
            'updated_at',
            'reply',
            'isReply',
            'reply_count',
            'isRetweet',
            'isRetweeted',
            'retweet',
            'retweet_user',
            'retweet_users',
            'retweet_count',
            'userIcon',
            'followees_in_retweet_users',
            'followees_in_liked',
            'created_time',
            'isBlocked',
            'isSendFollowRequest',
        ]

    def get_hashTag(self, obj):

        return HashTagSerializer(obj.hashTag.all(), many=True).data


    def get_liked(self, obj):

        return ProfileSubSerializer(obj.liked.all(), many=True).data


    def get_liked_count(self, obj):

        if obj.isRetweet == False:
            return obj.liked.count()

        try:
            return RetweetRelationShip.objects.get(retweet=obj).target_tweet.liked.all().count()
        except:
            return None


    def get_isLiked(self, obj):

        if self.login_user == None:
            return False

        target_tweet = obj
        if obj.isRetweet == True:
            target_tweet = search_retweet_target(target_tweet)
        return target_tweet.liked.filter(username=self.login_user).exists()

    def get_isFollow(self, obj):

        if self.login_user == None:
            return False

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return False

        return login_user.followees.filter(username=obj.author.username).exists()

    def get_isMyself(self, obj):

        if self.login_user == None:
            return False

        return obj.author.username == self.login_user


    def get_isRetweeted(self, obj):

        if self.login_user == None:
            return False

        if obj.isRetweet == True:
            target_tweet = search_retweet_target(obj)
            pk_list = RetweetRelationShip.objects.filter(target_tweet=target_tweet).values('retweet_user')
            return mUser.objects.filter(pk__in=pk_list).filter(username=self.login_user).exists()

        pk_list = RetweetRelationShip.objects.filter(target_tweet=obj).values('retweet_user')
        return mUser.objects.filter(pk__in=pk_list).filter(username=self.login_user).exists()

    def get_reply(self, obj):

        fields = [
            'pk',
            'author',
            'author_pk',
            'content',
            'reply_count',
            'liked_count',
            'retweet_count',
            'hashTag',
            'created_at',
            'created_time',
            'userIcon',
        ]

        # ログインしているユーザーならこれらのフィールドも
        if self.login_user != None:
            fields += ['isRetweeted', 'isLiked', 'isBlocked']

        target_tweet = obj
        if obj.isRetweet == True:
            try:
                target_tweet = search_retweet_target(obj)
            except ObjectDoesNotExist:
                logger.error('エラー')
                return None

        # 元ツイートじゃなければ元のツイート取得し、それに関連するリプライを取得
        if is_base_tweet(target_tweet) is False:
            target_tweet = search_reply_target_base(target_tweet)

        res = Tweet.objects.filter(pk__in=ReplyRelationShip.objects.filter(reply_target_base=target_tweet).values('reply'))

        # login_userの取得メソッドを渡すため、viewをセット
        if hasattr(self, 'v'):
            context = {
                'view': self.v
            }
            return TweetSerializer(res, fields=fields, many=True, context=context).data

        return TweetSerializer(res, fields=fields, many=True).data


    def get_reply_count(self, obj):

        target_tweet = obj

        if obj.isRetweet == True:
            try:
                target_tweet = RetweetRelationShip.objects.get(retweet=obj).target_tweet
            except RetweetRelationShip.DoesNotExist:
                return 0

        if is_base_tweet(target_tweet) == False:
            return target_tweet.replys.all().count()

        return ReplyRelationShip.objects.filter(reply_target_base=target_tweet).count()


    def get_retweet(self, obj):
        pk_list = RetweetRelationShip.objects.filter(target_tweet=obj).values('retweet')
        return TweetSerializer(Tweet.objects.filter(pk__in=pk_list), many=True).data


    def get_retweet_count(self, obj):

        if obj.isRetweet == False:
            return RetweetRelationShip.objects.filter(target_tweet=obj).count()
        return search_retweet_target(obj).retweets.all().count()


    def get_retweet_user(self, obj):
        if obj.isRetweet == False:
            return None

        try:
            return ProfileSubSerializer(RetweetRelationShip.objects.get(retweet=obj).retweet_user).data
        except RetweetRelationShip.DoesNotExist:
            return None
        except RetweetRelationShip.MultipleObjectsReturned:
            return None


    def get_retweet_users(self, obj):
        if obj.isRetweet == False:
            pk_list = RetweetRelationShip.objects.filter(target_tweet=obj).values('retweet_user')
            return ProfileSubSerializer(mUser.objects.filter(pk__in=pk_list), many=True).data

        target_tweet = search_retweet_target(obj)
        pk_list = RetweetRelationShip.objects.filter(target_tweet=target_tweet).values('retweet_user')
        return ProfileSubSerializer(mUser.objects.filter(pk__in=pk_list), many=True).data


    def get_followees_in_retweet_users(self, obj):

        if self.login_user == None:
            return []

        try:
            loginUser = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return []

        if obj.isRetweet == False:
            pk_list = RetweetRelationShip.objects.filter(target_tweet=obj).values('retweet_user')
            followees = mUser.objects.filter(pk__in=pk_list).filter(pk__in=loginUser.followees.all().values('pk'))
            return ProfileSubSerializer(followees, many=True, fields=['username']).data
        try:
            target_tweet = RetweetRelationShip.objects.get(retweet=obj).target_tweet
        except RetweetRelationShip.DoesNotExist:
            return []
        except RetweetRelationShip.MultipleObjectsReturned:
            return []

        pk_list = RetweetRelationShip.objects.filter(target_tweet=target_tweet).values('retweet_user')
        followees = mUser.objects.filter(pk__in=pk_list).filter(pk__in=loginUser.followees.all().values('pk'))
        return ProfileSubSerializer(followees, many=True, fields=['username']).data



    def get_followees_in_liked(self, obj):

        if self.login_user == None:
            return []

        try:
            loginUser = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return []

        if obj.isRetweet == False:
            followees = obj.liked.all().filter(pk__in=loginUser.followees.all().values('pk'))
            return ProfileSubSerializer(followees, many=True, fields=['username']).data
        try:
            target_tweet = RetweetRelationShip.objects.get(retweet=obj).target_tweet
        except RetweetRelationShip.DoesNotExist:
            return []
        except RetweetRelationShip.MultipleObjectsReturned:
            return []

        followees = target_tweet.liked.all().filter(pk__in=loginUser.followees.all().values('pk'))
        return ProfileSubSerializer(followees, many=True, fields=['username']).data

    def get_created_time(self, obj):

        timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz=timezone)
        created_at = obj.created_at
        diff = now - created_at

        if diff.days >= 30:
            return (now - timedelta(days=diff.days)).strftime('%Y/%m/%d')

        if diff.days != 0:
            return str(diff.days) + '日'

        if diff.seconds // 60 == 0:
            return str(diff.seconds) + '秒'

        if diff.seconds // 60 // 60 == 0:
            return str(diff.seconds // 60) + '分'

        return str(diff.seconds // 60 // 60) + '時間'


    def get_userIcon(self, obj):
        return '/media/' + str(obj.author.icon)

    def get_isBlocked(self, obj):

        if self.login_user == None:
            return False

        return obj.author.msetting.block_list.filter(username=self.login_user).exists()

    def get_isSendFollowRequest(self, obj):

        if self.login_user == None:
            return False

        try:
            login_user = mUser.objects.get(username=self.login_user)
        except mUser.DoesNotExist:
            return False

        return FollowRequest.objects.filter(
            follow_request_user=login_user,
            follow_response_user=obj.author,
            isAccepted=False
        ).exists()


    def create(self, validated_data):
        user = mUser.objects.get(pk=validated_data['author_pk'])
        content = validated_data['content']
        images = validated_data['images'] if 'images' in validated_data else None
        return Tweet.objects.create(author=user, content=content, images=images)


    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance


# カスタムフィールド参考用
class SelectSerializer(serializers.Field):

    def to_internal_value(self, data):
        return data

    def get_attribute(self, instance):
        method = 'get_%s_display' % (self.field_name)
        disp_name = getattr(instance, method)()
        return disp_name

    def to_representation(self, value):
        return value


class EntrySerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    author_pk = serializers.CharField(required=False)
    # type = SelectSerializer()
    # prefecture = SelectSerializer()
    # day_week = SelectSerializer()
    # direction = SelectSerializer()
    # sex = SelectSerializer()
    # age = SelectSerializer()
    type_disp = serializers.SerializerMethodField()
    prefecture_disp = serializers.SerializerMethodField()
    day_week_disp = serializers.SerializerMethodField()
    direction_disp = serializers.SerializerMethodField()
    sex_disp = serializers.SerializerMethodField()
    age_disp = serializers.SerializerMethodField()
    age = serializers.ListField(write_only=True, required=False, child=serializers.IntegerField())
    is_read = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user() if 'context' in kwargs else None
        super().__init__(*args, **kwargs)

    class Meta:
        model = Entry
        fields = [
            'id',
            'title',
            'content',
            'author',
            'author_pk',
            'type',
            'type_disp',
            'prefecture',
            'prefecture_disp',
            'area',
            'day_week',
            'day_week_disp',
            'direction',
            'direction_disp',
            'part',
            'genre',
            'sex',
            'sex_disp',
            'age',
            'age_disp',
            'is_read',
        ]

    def get_type_disp(self, obj):
        return obj.get_type_display()

    def get_prefecture_disp(self, obj):
        return obj.get_prefecture_display()

    def get_day_week_disp(self, obj):
        return obj.get_day_week_display()

    def get_direction_disp(self, obj):
        return obj.get_direction_display()

    def get_sex_disp(self, obj):
        return obj.get_sex_display()

    def get_age_disp(self, obj):
        if len(obj.age.all()) != 0:
            age_list = [age.get_age_display() for age in obj.age.all()]
            return age_list
        else:
            return None

    def get_is_read(self, obj):
        if self.login_user == None:
            return False

        target = mUser.objects.get(username=self.login_user)
        read_manage_cnt = ReadManagement.objects.filter(Q(entry=obj) & Q(target=target)).count()
        return False if read_manage_cnt == 0 else True # 既読されていたらTrueを返却

    def create(self, validated_data):
        entry = Entry.objects.create(
            author = mUser.objects.get(pk=validated_data['author_pk']),
            title = validated_data['title'],
            content = validated_data['content'],
            type = validated_data['type'],
            prefecture = validated_data['prefecture'],
            area = validated_data['area'],
            day_week = validated_data['day_week'],
            direction = validated_data['direction'],
            part = validated_data['part'],
            genre = validated_data['genre'],
            sex = validated_data['sex'],
        )
        if len(validated_data['age']) != 0:
            age_list = [Age.objects.get(age=age) for age in validated_data['age']]
            for age in age_list:
                entry.age.add(age)

        return entry


class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    room_name = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    msg_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user() if 'context' in kwargs else None
        super().__init__(*args, **kwargs)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'room_name',
            'users',
            'created_at',
            'msg_count',
        ]

    def get_room_name(self, obj):
        room_name = ''
        target_user = Room.objects.get(id=obj.id).users.exclude(username=self.login_user)
        for i in target_user:
            room_name += i.username
        return room_name

    def get_users(self, obj):
        users = Room.objects.get(id=obj.id).users.exclude(username=self.login_user)
        user_contents = ProfileSubSerializer(users, many=True).data
        return user_contents

    def get_msg_count(self, obj):
        msg = obj.room.all()
        count = []
        for m in msg:
            if (m.sender.username != self.login_user and not m.readed):
                count.append(m)
        return len(count)

    def create(self, validated_data):
        name = validated_data['name']
        room = Room.objects.create()
        room.users.add(mUser.objects.get(username=self.login_user))
        room.users.add(mUser.objects.get(username=name))
        return room

class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()
    isMe = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user() if 'context' in kwargs else None
        super().__init__(*args, **kwargs)

    class Meta:
        model = Message
        fields = [
            'id',
            'content',
            'sender',
            'receiver',
            'image',
            'readed',
            'deleted',
            'isMe',
            'created_at',
        ]

    def get_sender(self, obj):
        sender_name = obj.sender.username
        return sender_name

    def get_isMe(self, obj):
        isMe = str(obj.sender.username) == str(self.login_user)
        return isMe


class MessageSubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'readed',
            'deleted',
        ]


class MSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = mSetting
        fields = [
            'id',
            'target',
            'isPrivate',
            'language',
            'isDark'
        ]


class NotificationSerializer(serializers.ModelSerializer):
    """
    通知のシリアライザー
        isAccepted : 申請が許可された。
        isRejected : 申請が拒否された。
    """

    event = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    receive_user = serializers.SerializerMethodField()
    send_user = serializers.SerializerMethodField()
    target_tweet_info = serializers.SerializerMethodField()
    isAccepted = serializers.SerializerMethodField()
    isRejected = serializers.BooleanField(default=False)

    class Meta:
        model = Notification
        fields = [
            'pk',
            'event',
            'receive_user',
            'send_user',
            'target_tweet_info',
            'infomation',
            'created_at',
            'created_time',
            'readed',
            'isAccepted',
            'isRejected',
        ]


    def get_event(self, obj):
        return obj.get_event_display()


    def get_receive_user(self, obj):
        return ProfileSubSerializer(obj.receive_user).data


    def get_send_user(self, obj):
        return ProfileSubSerializer(obj.send_user).data


    def get_target_tweet_info(self, obj):
        if obj.target_tweet_info == None:
            return None

        fields = [
            'pk',
            'author',
            'author_pk',
            'content',
            'reply_count',
            'liked_count',
            'retweet_count',
            'created_at',
            'created_time',
            'isLiked',
            'isRetweeted'
        ]
        return TweetSerializer(obj.target_tweet_info, fields=fields).data


    def get_created_time(self, obj):

        timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz=timezone)
        created_at = obj.created_at
        diff = now - created_at

        if diff.days >= 30:
            return (now - timedelta(days=diff.days)).strftime('%Y/%m/%d')

        if diff.days != 0:
            return str(diff.days) + '日'

        if diff.seconds // 60 == 0:
            return str(diff.seconds) + '秒'

        if diff.seconds // 60 // 60 == 0:
            return str(diff.seconds // 60) + '分'

        return str(diff.seconds // 60 // 60) + '時間'

    def get_isAccepted(self, obj):

        if obj.event != 4:
            return False

        try:
            return FollowRequest.objects.get(
                follow_request_user=obj.send_user,
                follow_response_user=obj.receive_user
            ).isAccepted
        except FollowRequest.DoesNotExist:
            return False


class NotificationCountSerializer(serializers.ModelSerializer):
    """
    通知の数を取得するシリアライザー
    """

    info_count = serializers.SerializerMethodField()
    msg_count = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'info_count',
            'msg_count'
        ]

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user()
        super().__init__(*args, **kwargs)

    def get_info_count(self, obj):
        event_list = [0, 1, 2, 3, 4]
        return self.get_infomation_count(obj, event_list)

    def get_msg_count(self, obj):
        return self.get_message_notice_count(obj)


    def get_infomation_count(self, obj, event_list):
        if self.login_user == None:
            return 0
        try:
            login_user = mUser.objects.get(username=self.login_user)
            return Notification.objects.filter(
                event__in=event_list,
                receive_user=login_user,
                readed=False).count()
        except mUser.DoesNotExist:
            logger.error('mUserが存在しません')
            return 0


    def get_message_notice_count(self, obj):
        if self.login_user == None:
            return 0

        try:
            login_user = mUser.objects.get(username=self.login_user)
            return MessageNotification.objects.filter(
                receiver=login_user,
                readed=False
            ).count()
        except mUser.DoesNotExist:
            logger.info('mUserが存在しません')
            return 0


class MessageNotificationSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = MessageNotification
        fields = [
            'pk',
            'receiver',
            'sender',
            'room',
            'message',
            'created_at',
            'created_time',
            'readed',
        ]


    def get_receiver(self, obj):
        return ProfileSubSerializer(obj.receiver).data


    def get_sender(self, obj):
        return ProfileSubSerializer(obj.sender).data


    def get_room(self, obj):
        return RoomSerializer(obj.room).data

    def get_message(self, obj):
        return MessageSerializer(obj.message).data


    def get_created_time(self, obj):

        timezone = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz=timezone)
        created_at = obj.created_at
        diff = now - created_at

        if diff.days >= 30:
            return (now - timedelta(days=diff.days)).strftime('%Y/%m/%d')

        if diff.days != 0:
            return str(diff.days) + '日'

        if diff.seconds // 60 == 0:
            return str(diff.seconds) + '秒'

        if diff.seconds // 60 // 60 == 0:
            return str(diff.seconds // 60) + '分'

        return str(diff.seconds // 60 // 60) + '時間'
