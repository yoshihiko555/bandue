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

    class Meta:
        model = mUser
        fields = [
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
        return len(self.get_followers(obj))

class ProfileSubSerializer(serializers.ModelSerializer):

    class Meta:
        model = mUser
        fields = [
            'username',
        ]

class TweetSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    hashTag = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'author',
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

class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = [
            'title',
        ]


class EntrySerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = [
            'title',
            'content',
            'author',
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

class MUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = mUser
        fields = [
            'username',
            'email',
            'password',
        ]

    def create(self, validated_data):
        return mUser.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
