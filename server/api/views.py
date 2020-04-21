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

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

class TweetListView(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        return super().get(self, **kwargs)

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

class TweetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = mUser.objects.all()
    serializer_class = ProfileSerializer

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
        serializer = MUserSerializer(data=request.data)
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
