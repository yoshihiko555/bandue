from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps
from django.http import Http404
from django.views import generic
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.db import transaction
import logging
import re
from rest_framework import generics, permissions, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializers import (
    ProfileSerializer,
    TweetSerializer,
    EntrySerializer,
    MUserSerializer,
    ReplySerializer,
    RoomSerializer,
    MessageSerializer,
    SearchSerializer,
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


class IndexView(generic.TemplateView):

    template_name = 'pages/index.html'


class ProfileDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = mUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'


class ProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = mUser.objects.all()
    serializer_class = ProfileSerializer


class SignUpView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = mUser.objects.all()
    serializer_class = MUserSerializer

    @transaction.atomic
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = mUser.objects.get(id=serializer.data['pk'])

            current_site = get_current_site(self.request)
            domain = current_site.domain
            context = {
                'protocol': 'https' if self.request.is_secure() else 'http',
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }

            subject = '題名'
            message = render_to_string('register/message.txt', context)
            user.email_user(subject, message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchView(generics.ListAPIView, GetLoginUserMixin):

    permission_classes = (permissions.AllowAny,)
    search_query = {
        '0': {
            'queryset': Tweet.objects.all(),
            'serializer_class': TweetSerializer,
            'filter_class': TweetFilter,
        },
        '1': {
            'queryset': Tweet.objects.all(),
            'serializer_class': TweetSerializer,
            'filter_class': TweetFilter,
        },
        '2': {
            'queryset': mUser.objects.all(),
            'serializer_class': ProfileSerializer,
            'filter_class': MUserFilter,
        },
        '3': {
            'queryset': Tweet.objects.all(),
            'serializer_class': TweetSerializer,
            'filter_class': TweetFilter,
        },
    }

    def list(self, request, *args, **kwargs):
        self.login_user = request.query_params['loginUser'] if 'loginUser' in request.query_params else None
        searchFlg = request.query_params['searchFlg']
        self.setSearchQuery(searchFlg, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def setSearchQuery(self, searchFlg, *args, **kwargs):
        self.queryset = self.search_query[searchFlg]['queryset']
        self.serializer_class = self.search_query[searchFlg]['serializer_class']
        self.filter_class = self.search_query[searchFlg]['filter_class']
