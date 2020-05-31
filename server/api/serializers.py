from rest_framework import serializers
from .models import (
    mUser,
    Message,
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
            followees_contents = ProfileSubSerializer(mUser.objects.get(id=obj.id).followees.all(), many=True).data
            return followees_contents
        except:
            followees_contents = None
            return followees_contents

    def get_followers(self, obj):
        try:
            followers_contents = ProfileSubSerializer(mUser.objects.filter(followees=mUser.objects.get(id=obj.id)), many=True).data
            return followers_contents
        except:
            followers_contents = None
            return followers_contents

    def get_followees_count(self, obj):
        return obj.followees.count()

    def get_followers_count(self, obj):
        return len(self.get_followers(obj)) if self.get_followers(obj) != None else 0

    def get_tweet(self, obj):
        try:
            tweet_contents = TweetSerializer(mUser.objects.get(id=obj.id).author.all(), many=True).data
            return tweet_contents
        except:
            tweet_contents = None
            return tweet_contents

    def get_bbs(self, obj):
        try:
            bbs_contents = BbsSerializer(mUser.objects.get(id=obj.id).writer.all(), many=True).data
            return bbs_contents
        except:
            bbs_contents = None
            return bbs_contents

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

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['context']['view'].get_login_user()
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
        ]

    def get_author(self, obj):
        author_contents = obj.author.username
        return author_contents

    def get_hashTag(self, obj):
        hashTag_contents = HashTagSerializer(obj.hashTag.all(), many=True).data
        return hashTag_contents

    def get_liked(self, obj):
        try:
            liked_content = ProfileSubSerializer(Tweet.objects.get(id=obj.id).liked.all(), many=True).data
            return liked_content
        except:
            liked_content = None
            return liked_content

    def get_liked_count(self, obj):
        return obj.liked.count()

    def get_isLiked(self, obj):
        # self.target_user(username)が個々のツイートをいいねしているか判定しフラグを立てる
        # とりあえずの実装。ORMの理解が深まり次第リファクタリング予定
        isLiked = 0
        if self.login_user != None:
            tweet = Tweet.objects.get(id=obj.id)
            for u in tweet.liked.all():
                if u.username == self.login_user:
                    isLiked = 1
                    break

        return isLiked

    def create(self, validated_data):
        user = mUser.objects.get(pk=validated_data['author_pk'])
        content = validated_data['content']
        return Tweet.objects.create(author=user, content=content)

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance


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
