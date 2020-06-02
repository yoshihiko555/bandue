from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import ModelFormMixin, FormMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse, QueryDict
from django.views import generic
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count, Q
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView
)
from django.db import transaction
import logging
import json
import re
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from functools import reduce
import operator
from datetime import datetime, timedelta
from rest_framework import generics, permissions, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializers import (
    ProfileSerializer,
    TweetSerializer,
    EntrySerializer,
    MUserSerializer,
    BbsSerializer,
)
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
    ReTweet,
)
from .permissions import IsMyselfOrReadOnly
from django_filters import rest_framework as django_filter

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):

    template_name = 'pages/index.html'


class TweetFilter(django_filter.FilterSet):

    def __init__(self, *args, **kwargs):
        self.target_user = kwargs['data']['targetUser'] if 'targetUser' in kwargs['data'] else None
        super().__init__(*args, **kwargs)

    tweetListFlg = django_filter.NumberFilter(method='tweet_filter')
    content = django_filter.CharFilter(lookup_expr='contains')
    deleted = django_filter.BooleanFilter(field_name='deleted', method='deleted_filter')

    class Meta:
        model = Tweet
        fields = ['deleted']

    def tweet_filter(self, queryset, name, value):
        res = queryset
        if self.target_user != None:
            target_user = mUser.objects.get(username=self.target_user)
            if value == 0:
                logger.debug('リプライツイート除いた一覧')
                res = Tweet.objects.filter(author=target_user)

            elif value == 1:
                logger.debug('リプライツイート含めた一覧')
                t_list = Tweet.objects.filter(author=target_user)
                r_list = ReTweet.objects.filter(retweet_user=target_user)
                res = t_list.union(r_list).order_by('-created_at')

            elif value == 2:
                logger.debug('画像含めた一覧')
                res = Tweet.objects.filter(author=target_user).exclude(images__isnull=False)

            elif value == 3:
                logger.debug('いいねしたツイート一覧')
                res = Tweet.objects.filter(liked=target_user)

            elif value == 4:
                logger.debug('ユーザー&フォローユーザーツイート一覧')

                tweet_list = Tweet.objects.filter(author=target_user)
                query_list = []
                for i in target_user.followees.all():
                    query_list.append("Tweet.objects.filter(author=mUser.objects.get(username='" + i.username + "'))")
                for i in range(len(query_list)):
                    tweet_list = tweet_list.union(eval(query_list[i]))
                res = tweet_list.order_by('-created_at')

        else:
            logger.debug('target_userがない')

        logger.debug('--TWEET_FILTER_RESULT--')
        logger.debug(res)
        return res

    def deleted_filter(self, queryset, name, value):
        logger.debug('====DELETED_FILTER====')
        logger.debug(name)
        logger.debug(value)
        lookup = '__'.join([name, 'isnull'])
        res = queryset.filter(**{lookup: value})
        logger.debug('--result--')
        logger.debug(res)
        return res

    def get_username(self):
        return self.target_user if self.target_user != None else None


class TweetViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_class = TweetFilter

    def get_login_user(self):
        return self.login_user if hasattr(self, 'login_user') else None

    def list(self, request, *args, **kwargs):
        logger.debug(self.request.query_params)
        self.login_user = request.query_params['loginUser'] if 'loginUser' in request.query_params else None
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
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

    def retrieve(self, request, pk=None):
        logger.debug('★★★★★詳細取得★★★★★')
        queryset = self.queryset.get(pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

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
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def liked(self, request):
        logger.debug('likedメソッド')
        login_user = mUser.objects.get(username=request.data['login_user'])
        target_tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        target_tweet.liked.add(login_user)
        logger.debug(target_tweet.liked.all())
        return Response({'status': 'success', 'isLiked': 1}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def unLiked(self, request):
        logger.debug('unlikedメソッド')
        login_user = mUser.objects.get(username=request.data['login_user'])
        target_tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        target_tweet.liked.remove(login_user)
        logger.debug(target_tweet.liked.all())
        return Response({'status': 'success', 'isLiked': 0}, status=status.HTTP_200_OK)

    @action(methods=['postc'], detail=False)
    def retweet(self, request):
        logger.debug('retweetメソッド')
        login_user = mUser.objects.get(username=request.data['login_user'])
        tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        self.set_tweet_relation(login_user, tweet, true)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def unRetweet(self, request):
        logger.debug('unRetweetメソッド')
        login_user = mUser.objects.get(username=request.data['login_user'])
        tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        self.set_tweet_relation(login_user, tweet, false)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    def set_tweet_relation(self, login_user, tweet, set_flg):
        if set_flg:
            tweet.retweet_user.add(login_user)
            retweet = ReTweet.objects.create(author=tweet.author, content=tweet.content, images=tweet.images)
            retweet.liked.add(*list(tweet.liked.all()))
            retweet.liked.add(*list(tweet.hashTag.all()))
            retweet.retweet_user.add(login_user)
            tweet.relation = retweet
            retweet.relation = tweet
        else:
            tweet.retweet_user.remove(login_user)
            tweet.relation.delete()
            tweet.relation = None


class TweetListView(generics.ListCreateAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def post(self, request, *args, **kwargs):
        logger.debug('apiのpost')
        logger.debug(request.user)
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


class TweetDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = mUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'


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

class BbsViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Bbs.objects.all()
    serializer_class = BbsSerializer

    def get_login_user(self):
        return self.login_user if hasattr(self, 'login_user') else None

    def list(self, request, *args, **kwargs):
        logger.debug(self.request.query_params)
        self.login_user = request.query_params['loginUser'] if 'loginUser' in request.query_params else None
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        logger.debug('viewsetのcreate')
        logger.debug(request.user)
        request.data.update({
            'writer_pk': str(request.user.pk)
        })
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            # とりあえずの処置
            queryset = Bbs.objects.filter(writer=request.user)
            logger.debug(queryset)
            return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BbsListView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    @transaction.atomic
    def post(self, request, format=None):
        logger.info('test')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BbsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = BbsSerializer


class SignUpView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = mUser.objects.all()
    serializer_class = MUserSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ユーザー削除のView
# サインアウトを実装してるときに間違って作った
# 後で使うだろうから残しておく
class DeleteUserView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MUserSerializer
    lookup_field = 'username'
    queryset = mUser.objects.all()

    def get_object(self):
        try:
            logger.info(self.request.user)
            instance = self.queryset.get(username=self.request.user)
            return instance
        except mUser.DoesNotExist:
            return Http404
