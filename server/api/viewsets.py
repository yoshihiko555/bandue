from django.http import Http404
from django.views import generic
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.db import transaction
import logging
import re
from rest_framework import generics, permissions, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .serializers import (
    ProfileSerializer,
    TweetSerializer,
    EntrySerializer,
    MUserSerializer,
    ReplySerializer,
    RoomSerializer,
    MessageSerializer,
)
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
    Room,
    Message,
    mUser_Room,
)
from .permissions import IsMyselfOrReadOnly

logger = logging.getLogger(__name__)
from .filters import (
    TweetFilter,
    MUserFilter,
)

from .mixins import (
    GetLoginUserMixin,
)

from .utils import (
    analyzeMethod
)


class BaseModelViewSet(viewsets.ModelViewSet, GetLoginUserMixin):

    pass


class TweetViewSet(BaseModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_class = TweetFilter
    parser_class = (FileUploadParser)

    def list(self, request, *args, **kwargs):

        self.login_user = request.query_params['loginUser'] if 'loginUser' in request.query_params else None
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        logger.info(serializer.data)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):

        logger.debug('viewsetのcreate')
        logger.debug(request.data)
        request.data.update({
            'author_pk': str(request.user.pk)
        })
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            # とりあえずの処置
            queryset = Tweet.objects.filter(author=request.user)
            logger.debug(queryset)
            return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):

        logger.debug('★★★★★Tweet更新★★★★★')
        queryset = self.queryset.get(pk=pk)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        logger.info('Tweet削除')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
        except Http404:
            pass
        return Response(serializer.data)


    @action(methods=['post'], detail=False)
    def liked(self, request):

        logger.debug('likedメソッド')
        login_user = request.user
        tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        target_tweet = tweet.retweet if tweet.isRetweet == True else tweet
        return self.set_tweet_liked_info(target_tweet, login_user)

    def set_tweet_liked_info(self, tweet, login_user):
        try:
            tweet.liked.all().get(username=login_user.username)
            tweet.liked.remove(login_user)
            return Response({'status': 'success', 'isLiked': 0}, status=status.HTTP_200_OK)
        except mUser.DoesNotExist:
            tweet.liked.add(login_user)
            return Response({'status': 'success', 'isLiked': 1}, status=status.HTTP_200_OK)


    @transaction.atomic
    @action(methods=['post'], detail=False)
    def retweet(self, request):
        logger.debug('retweetメソッド')
        login_user = request.user
        tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        return self.set_tweet_relation(login_user, tweet)


    def set_tweet_relation(self, login_user, tweet):
        tweet = tweet.retweet if tweet.isRetweet == True else tweet
        return self.set_tweet_relation_info(login_user, tweet)


    def set_tweet_relation_info(self, login_user, tweet):


        for retweet in Tweet.objects.filter(retweet=tweet):
            if retweet.retweet_user == login_user.username:
                logger.debug('紐づくリツイートが存在するため削除')
                retweet.delete()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)

        logger.debug('リツイートを新規作成')
        retweet = Tweet.objects.create(
            author=tweet.author,
            content=tweet.content,
            images=tweet.images,
            isRetweet=True,
            retweet=tweet,
            retweet_user=login_user.username
        )
        retweet.liked.add(*list(tweet.liked.all()))
        retweet.hashTag.add(*list(tweet.hashTag.all()))
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)



class ReplyViewSet(BaseModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def create(self, request, *args, **kwargs):

        logger.debug('reply_create')
        logger.debug(request.data)
        request.data.update({
            'author_pk': str(request.user.pk),
            'target': str(request.data['target'])
        })
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class mUserViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = mUser.objects.all()
    serializer_class = MUserSerializer

    @action(methods=['post'], detail=False)
    def isFollow(self, request):
        login_user = request.user
        target_user = request.data['target_user']
        isFollow = 0
        for followed_user in login_user.followees.all():
            if followed_user.username == target_user:
                isFollow = 1
                break
        return Response({'status': 'success', 'isFollow': isFollow}, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=False)
    def follow(self, request):

        logger.debug(str(request.user) + 'が' + request.data['target_user'] + 'をフォロー')

        login_user = request.user
        followed_username = request.data['target_user']
        followed_user = mUser.objects.get(username=followed_username)
        login_user.followees.add(followed_user)
        logger.debug('成功')
        logger.debug(login_user.followees.all())
        return Response({'status': 'success', 'isFollow': 1}, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=False)
    def unfollow(self, request):

        logger.debug(str(request.user) + 'が' + request.data['target_user'] + 'をアンフォロー')

        login_user = request.user
        unfollowed_username = request.data['target_user']
        unfollowed_user = mUser.objects.get(username=unfollowed_username)
        login_user.followees.remove(unfollowed_user)
        logger.debug('成功')
        logger.debug(login_user.followees.all())
        return Response({'status': 'success', 'isFollow': 0}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def checkUserDuplication(self, request):
        username = request.query_params['username']
        try:
            mUser.objects.get(username=username)
        except mUser.DoesNotExist:
            return Response({'status': 'success', 'result': True}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'success', 'result': False}, status=status.HTTP_200_OK)


class RoomViewSet(BaseModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        self.login_user = request.query_params['loginUser'] if 'loginUser' in request.query_params else None
        login_user = mUser.objects.get(username=self.login_user)
        rooms = mUser_Room.objects.filter(user_id=login_user.id)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.login_user = request.data['loginUser'] if 'loginUser' in request.data else None
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(BaseModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        logger.info('メッセージ一覧取得')
        self.login_user = request.query_params['loginUser'] if 'loginUser' in request.query_params else None
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EntryViewSet(BaseModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def create(self, request, *args, **kwargs):
        request.data.update({
            'author_pk': str(request.user.pk)
        })
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
        except Http404:
            pass
        return Response(serializer.data)
