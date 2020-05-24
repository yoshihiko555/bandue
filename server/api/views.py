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
    Entry
)
from .permissions import IsMyselfOrReadOnly
from django_filters import rest_framework as django_filter

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):

    template_name = 'pages/index.html'


class TweetFilter(django_filter.FilterSet):

    def __init__(self, *args, **kwargs):
        self.username = kwargs['data']['username'] if 'username' in kwargs['data'] else None
        super().__init__(*args, **kwargs)

    tweetListFlg = django_filter.NumberFilter(method='tweet_filter')
    content = django_filter.CharFilter(lookup_expr='contains')
    deleted = django_filter.BooleanFilter(field_name='deleted', method='deleted_filter')

    class Meta:
        model = Tweet
        fields = ['deleted']

    def tweet_filter(self, queryset, name, value):
        res = queryset
        if self.username != None:
            login_user = mUser.objects.get(username=self.username)
            logger.debug(login_user)
            if value == 0:
                # TODO リプライツイートは除く
                logger.debug('リプライツイート除いた一覧')
                res = Tweet.objects.filter(author=login_user)
            elif value == 1:
                # TODO リプライツイートも含める
                logger.debug('リプライツイート含めた一覧')
                res = Tweet.objects.filter(author=login_user)
            elif value == 2:
                # TODO 画像含める?
                logger.debug('画像含めた一覧')
                res = Tweet.objects.filter(author=login_user)
            elif value == 3:
                # TODO いいねしたツイート一覧 model定義変える
                logger.debug('いいねしたツイート一覧')
                res = Tweet.objects.filter(author=login_user)
            elif value == 4:
                # TODO ユーザー&フォローユーザー
                logger.debug('ユーザー&フォローユーザーツイート一覧')
                # res = Tweet.objects.filter(author=login_user)
                res = Tweet.objects.all()

        else:
            logger.debug('ログインしていないユーザー=>一覧返す')

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
        return self.username if self.username != None else None


class TweetViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_class = TweetFilter

    def get_target_user(self):
        return self.target_user if hasattr(self, 'target_user') else None

    def list(self, request, *args, **kwargs):
        logger.debug(self.request.query_params)
        self.target_user = request.query_params['username'] if 'username' in request.query_params else None
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
            'author_pk': str(request.user.pk)
        })
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def liked(self, request):
        logger.debug('likedメソッド')
        login_user = mUser.objects.get(username=request.data['username'])
        target_tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        target_tweet.liked.add(login_user)
        return Response({'status': 'success', 'isLiked': 1}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def unliked(self, request):
        logger.debug('unlikedメソッド')
        login_user = mUser.objects.get(username=request.data['username'])
        target_tweet = Tweet.objects.get(pk=request.data['target_tweet_id'])
        target_tweet.liked.remove(login_user)
        return Response({'status': 'success', 'isLiked': 0}, status=status.HTTP_200_OK)


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


class BbsListView(generics.ListCreateAPIView):

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class BbsDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


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
