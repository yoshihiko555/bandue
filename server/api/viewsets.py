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
    ReplySerializer,
    RoomSerializer,
    MessageSerializer,
    NotificationSerializer,
    NotificationCountSerializer
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
    ReadManagement,
    FollowRelationShip,
    RetweetRelationShip,
    Notification
)
from .permissions import IsMyselfOrReadOnly
from django.template.context_processors import request
from django.core.serializers import serialize

logger = logging.getLogger(__name__)
from .filters import (
    TweetFilter,
    MUserFilter,
    EntryFilter,
)

from .mixins import (
    GetLoginUserMixin,
)

from .utils import (
    analyzeMethod,
)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class BaseModelViewSet(viewsets.ModelViewSet, GetLoginUserMixin):
    """
    ModelViewSetのBaseクラス
        ModelViewSetでloginUserを取得する事が多いので
        GetLoginUserMixinを継承し、このクラスの継承先で使用
    """

    def list(self, request, *args, **kwargs):
        """
        getでリクエストが来たらlogin_userをセット
        response=Trueだったらレスポンスも返す
        paginate=Trueだったらページネーションありのレスポンスを返す
        """
        self.set_login_user(request)

        if 'response' in kwargs and kwargs['response'] == True:
            return self.send_response(**kwargs)

    def send_response(self, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        """
        paginate=Trueだったらページネーションありのレスポンスを返す
        """
        if 'paginate' in kwargs and kwargs['paginate'] == True:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TweetViewSet(BaseModelViewSet):
    """
    ツイート関連のViewSet

        Methods
        ---------------------------------------
        list : ページ毎にツイートを返す

        create : ツイートする時

        update : ツイートを編集する時

        delete : ツイートを削除する時

        liked : いいねボタン押下時

        retweet : リツイートボタン押下時
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_class = TweetFilter
    parser_class = (FileUploadParser)

    def list(self, request, *args, **kwargs):
        return super().list(request, paginate=True,
                            response=True, *args, **kwargs)

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
            return Response(self.get_serializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)

        logger.debug(serializer.errors)
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
        logger.debug(request.data)
        login_user = request.user
        tweet = Tweet.objects.get(pk=request.data['target_tweet_pk'])
        target_tweet = tweet
        if tweet.isRetweet == True:
            try:
                target_tweet = RetweetRelationShip.objects.get(retweet=tweet).target_tweet
            except Tweet.DoesNotExist:
                logger.debug('target_tweet取得できてない')
                pass

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
        tweet = Tweet.objects.get(pk=request.data['target_tweet_pk'])
        return self.set_tweet_relation(login_user, tweet)


    def set_tweet_relation(self, login_user, tweet):

        target_tweet = tweet
        if tweet.isRetweet == True:
            try:
                target_tweet = RetweetRelationShip.objects.get(retweet=tweet).target_tweet
            except Tweet.DoesNotExist:
                logger.debug('target_tweet取得できてない')
                pass

        isExists = mUser.objects.filter(pk__in=RetweetRelationShip.objects.filter(target_tweet=target_tweet).values('retweet_user')).filter(username=login_user.username).exists()
        if isExists:
            try:
                retweet = RetweetRelationShip.objects.get(target_tweet=target_tweet, retweet_user=login_user).retweet
                retweet.delete()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            except RetweetRelationShip.DoesNotExist:
                return Response({'status': 'success'}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug('リツイートを新規作成')
        retweet = Tweet.objects.create(
            author=target_tweet.author,
            content=target_tweet.content,
            images=target_tweet.images,
            isRetweet=True,
            retweet_username=login_user.username
        )
        retweet.liked.add(*list(tweet.liked.all()))
        retweet.hashTag.add(*list(tweet.hashTag.all()))
        RetweetRelationShip.objects.create(
            target_tweet=target_tweet,
            retweet=retweet,
            retweet_user=login_user
        )
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)



class ReplyViewSet(BaseModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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


class mUserViewSet(viewsets.ModelViewSet):
    """
    ユーザー関連のViewSet

        Methods
        ---------------------------
        isFollow : フォローしているか

        follow : フォローする時

        unfollow : フォロー解除
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = mUser.objects.all()
    serializer_class = ProfileSerializer


    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        fields = [
            'pk',
            'username',
            'email',
            'address',
        ]
        if page is not None:
            serializer = ProfileSerializer(page, many=True, fields=fields)
            return self.get_paginated_response(serializer.data)
        serializer = ProfileSerializer(queryset, many=True, fields=fields)
        return Response(serializer.data)


    @action(methods=['post'], detail=False)
    def isFollow(self, request):
        login_user = request.user
        target_user = request.data['target_user']
        isFollow = 1 if login_user.followees.filter(username=target_user).exists() else 0
        return Response({'status': 'success', 'isFollow': isFollow}, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=False)
    def follow(self, request):

        login_user = request.user
        followed_username = request.data['target_user']
        followed_user = mUser.objects.get(username=followed_username)
        login_user.followees.add(followed_user)
        logger.debug(str(request.user) + 'が' + request.data['target_user'] + 'をフォロー')
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

        return super().list(request, response=True, *args, **kwargs)
        # self.set_login_user(request)
        # login_user = mUser.objects.get(username=self.login_user)
        # rooms = mUser_Room.objects.filter(user_id=login_user.id)
        # queryset = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

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
        return super().list(request, response=True, *args, **kwargs)
        # self.set_login_user(request)
        # queryset = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def message_delete(self, request, pk=None):
        message = Message.objects.get(pk=pk)
        message.deleted = True
        message.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False)
    def message_read(self, request):
        logger.info('既読')
        messages = []
        for i in request.data:
            msg = Message.objects.get(id=i['id'])
            msg.readed = True
            messages.append(msg)

        Message.objects.bulk_update(messages, fields=['readed'])
        return Response(status=status.HTTP_200_OK)


class EntryViewSet(BaseModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_class = EntryFilter

    def list(self, request, *args, **kwargs):
        return super().list(request, response=True,
                            paginate=True, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data.update({
            'author_pk': str(request.user.pk)
        })
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(self.get_serializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)
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

    @action(methods=['post'], detail=False)
    def isRead(self, request):
        logger.info('既読したーー')
        logger.info(request.data)
        user = mUser.objects.get(username=request.user.username)
        entry = Entry.objects.get(id=request.data['id'])
        read_manage_cnt = ReadManagement.objects.filter(Q(entry=entry) & Q(target=user)).count()
        if read_manage_cnt == 0:
            # 新規既読ならレコード追加
            ReadManagement.objects.create(
                target=user,
                entry=entry,
                is_read=True,
            )
            # 記事の既読数を１に設定
            entry.read_count = 1
            entry.save()

        else:
            # 現在の既読数を中間テーブルから取得して設定
            entry.read_count = read_manage_cnt
            entry.save()

        return Response(status=status.HTTP_200_OK)


class InfoViewSet(BaseModelViewSet):
    """
    通知関連のViewSet
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Notification.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        self.serializer_class = NotificationSerializer
        if self.login_user == None:
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(
                receive_user=mUser.objects.get(username=self.login_user)
            )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def getInfoCnt(self, request):
        self.set_login_user(request)
        self.serializer_class = NotificationCountSerializer
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def readInfo(self, request):
        self.set_login_user(request)
        self.serializer_class = NotificationSerializer

        notifications = Notification.objects.filter(
            receive_user=mUser.objects.get(username=self.login_user),
            readed=False
        )
        infos = []
        for notification in notifications:
            notification.readed = True
            infos.append(notification)
        Notification.objects.bulk_update(infos, fields=['readed'])

        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
