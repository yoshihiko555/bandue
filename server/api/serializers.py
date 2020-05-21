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
            tweet_contents = TweetSerializer(mUser.objects.get(id=obj.id).tweet_set.all(), many=True).data
            return tweet_contents
        except:
            tweet_contents = None
            return tweet_contents

class ProfileSubSerializer(serializers.ModelSerializer):

    class Meta:
        model = mUser
        fields = [
            'id',
            'username',
        ]

class TweetSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    author_pk = serializers.CharField(required=False)
    hashTag = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'author',
            'author_pk',
            'content',
            'liked',
            'hashTag',
            'images',
            'created_at',
            'updated_at',
        ]

    def get_author(self, obj):
        author_contents = obj.author.username
        return author_contents

    def get_hashTag(self, obj):
        hashTag_contents = HashTagSerializer(obj.hashTag.all(), many=True).data
        return hashTag_contents

    def create(self, validated_data):
        user = mUser.objects.get(pk=validated_data['author_pk'])
        content = validated_data['content']
        return Tweet.objects.create(author=user, content=content)

class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = [
            'title',
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
