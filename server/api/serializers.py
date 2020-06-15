from rest_framework import serializers
from .models import (
    mUser,
    HashTag,
    Tweet,
    Reply,
    mSetting,
    hUserUpd,
    hTweetUpd,
    mAccessLog,
    Band,
    MemberShip,
    Entry,
    Bbs,
    Tag,
    Category,
    Room,
    Message,
    mUser_Room,
)
from rest_framework.renderers import JSONRenderer

import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '''%(levelname)s %(asctime)s %(pathname)s:%(funcName)s:%(lineno)s
    %(message)s''')


logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):

    followees = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followees_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    tweet = serializers.SerializerMethodField()
    bbs = serializers.SerializerMethodField()

    class Meta:
        model = mUser
        fields = [
            'id',
            'username',
            'email',
            'address',
            'created_at',
            'thumbnail',
            'introduction',
            'icon',
            'followees',
            'followers',
            'followees_count',
            'followers_count',
            'tweet',
            'bbs'
        ]

    def get_followees(self, obj):
        try:
            return ProfileSubSerializer(mUser.objects.get(id=obj.id).followees.all(), many=True).data
        except:
            return None

    def get_followers(self, obj):
        try:
            return ProfileSubSerializer(mUser.objects.filter(followees=mUser.objects.get(id=obj.id)), many=True).data
        except:
            return None

    def get_followees_count(self, obj):
        return obj.followees.count()

    def get_followers_count(self, obj):
        return len(self.get_followers(obj)) if self.get_followers(obj) != None else 0

    def get_tweet(self, obj):
        try:
            return TweetSerializer(mUser.objects.get(id=obj.id).author.all(), many=True).data
        except:
            return None

    def get_bbs(self, obj):
        try:
            return BbsSerializer(mUser.objects.get(id=obj.id).writer.all(), many=True).data
        except:
            return None

class ProfileSubSerializer(serializers.ModelSerializer):

    class Meta:
        model = mUser
        fields = [
            'id',
            'username',
            'email',
            'address',
            'created_at',
            'thumbnail',
            'introduction',
            'icon',
        ]


class TweetSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    author_pk = serializers.CharField(required=False)
    hashTag = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()
    isReplied = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    isRetweeted = serializers.SerializerMethodField()
    retweet = serializers.SerializerMethodField()
    retweet_user = serializers.SerializerMethodField()
    retweet_count = serializers.SerializerMethodField()


    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user() if 'context' in kwargs else None
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tweet
        fields = [
            'id',
            'author',
            'author_pk',
            'content',
            'liked',
            'liked_count',
            'hashTag',
            'images',
            'created_at',
            'updated_at',
            'isLiked',
            'reply',
            'isReplied',
            'reply_count',
            'isRetweet',
            'isRetweeted',
            'retweet',
            'retweet_user',
            'retweet_count',
        ]

    def get_author(self, obj):
        try:
            return obj.author.username
        except:
            return None

    def get_hashTag(self, obj):
        try:
            return HashTagSerializer(obj.hashTag.all(), many=True).data
        except:
            return None

    def get_liked(self, obj):
        try:
            return ProfileSubSerializer(Tweet.objects.get(id=obj.id).liked.all(), many=True).data
        except:
            return None

    def get_liked_count(self, obj):
        return obj.liked.count()

    def get_isLiked(self, obj):
        # とりあえずの実装。ORMの理解が深まり次第リファクタリング予定
        isLiked = False
        if self.login_user != None:
            try:
                tweet = Tweet.objects.get(id=obj.id)
                for u in tweet.liked.all():
                    if u.username == self.login_user:
                        isLiked = True
                        break
            except:
                pass
        return isLiked

    def get_reply(self, obj):
        try:
            return ReplySerializer(Tweet.objects.get(id=obj.id).reply_set.all(), many=True).data
        except:
            return None

    def get_isReplied(self, obj):
        try:
            tweet = Tweet.objects.get(id=obj.id)
            isReplied = True if len(tweet.reply_set.all()) != 0 else False
            return isReplied
        except:
            return None

    def get_reply_count(self, obj):
        try:
            return len(Tweet.objects.get(id=obj.id).reply_set.all())
        except:
            return None

    def get_isRetweeted(self, obj):
        # とりあえずの実装。ORMの理解が深まり次第リファクタリング予定
        isRetweeted = False
        if self.login_user != None:
            try:
                tweet = Tweet.objects.get(id=obj.id)
                for user in tweet.retweet_user.all():
                    if user.username == self.login_user:
                        isRetweeted = True
                        break
            except:
                pass
        return isRetweeted

    def get_retweet(self, obj):
        try:
            if len(Tweet.objects.get(pk=objid).retweet) >= 1:
                return TweetSerializer(Tweet.objects.get(pk=obj.id).retweet).data
        except:
            return None

    def get_retweet_user(self, obj):
        try:
            return TweetSerializer(Tweet.objects.get(pk=obj.id).retweet_user.all(), many=True).data
        except:
            return None

    def get_retweet_count(self, obj):
        try:
            tweet = Tweet.objects.get(id=obj.id)
            return len(tweet.retweet_user.all())
        except:
            return None

    def create(self, validated_data):
        user = mUser.objects.get(pk=validated_data['author_pk'])
        content = validated_data['content']
        return Tweet.objects.create(author=user, content=content)

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance


class ReplySerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    author_pk = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'id',
            'author',
            'author_pk',
            'target',
            'content',
            'created_at',
        ]

    def get_author(self, obj):
        author_contents = obj.author.username
        return author_contents

    def get_author_pk(self, obj):
        author_pk_contents = obj.author.pk
        return author_pk_contents

    def create(self, validated_data):
        user = mUser.objects.get(pk=validated_data['author_pk'])
        target = Tweet.objects.get(pk=validated_data['target_tweet'])
        content = validated_data['content']
        return Reply.objects.create(author=user, target=target, content=content)


class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = [
            'id',
            'title',
            'created_at',
            'slug',
        ]


class EntrySerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    author_pk = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = [
            'id',
            'title',
            'content',
            'author',
            'author_pk',
            'type',
            'prefecture',
            'area',
            'day_week',
            'direction',
            'part',
            'genre',
        ]

    def get_author(self, obj):
        author_contents = obj.author.username
        return author_contents

    def get_author_pk(self, obj):
        author_pk_contents = obj.author.pk
        return author_pk_contents


class MUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = mUser
        fields = [
            'pk',
            'username',
            'email',
            'password',
        ]

    def create(self, validated_data):
        return mUser.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])

class BbsSerializer(serializers.ModelSerializer):

    writer = serializers.SerializerMethodField()
    writer_pk = serializers.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user()
        super().__init__(*args, **kwargs)

    class Meta:
        model = Bbs
        fields = [
            'id',
            'writer',
            'writer_pk',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

    def get_writer(self, obj):
        writer_contents = obj.writer.username
        return writer_contents

    def create(self, validated_data):
        user = mUser.objects.get(pk=validated_data['writer_pk'])
        title = validated_data['title']
        content = validated_data['content']
        return Bbs.objects.create(writer=user, title=title, content=content)

class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    room_name = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user()
        super().__init__(*args, **kwargs)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'room_name',
            'users',
            'created_at',
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

    def create(self, validated_data):
        name = validated_data['name']
        room = Room.objects.create()
        room.users.add(mUser.objects.get(username=self.login_user))
        room.users.add(mUser.objects.get(username=name))
        return room

class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    isMe = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user()
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

    def get_receiver(self, obj):
        receiver_name = obj.receiver.username
        return receiver_name

    def get_isMe(self, obj):
        isMe = str(obj.sender.username) == str(self.login_user)
        return isMe
