import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from api.models import mUser
from django.utils.safestring import mark_safe
import logging
import json

logger = logging.getLogger(__name__)

class IsAuthView(TemplateView):
    template_name = 'pages/isAuth.html'

class HomeView(TemplateView):
    template_name = 'pages/home.html'

class ExploreView(TemplateView):
    template_name = 'pages/explore.html'

class SignUpView(TemplateView):
    template_name = 'register/signup.html'

class SignInView(TemplateView):
    template_name = 'register/signin.html'

class SignUpCompleteView(TemplateView):
    template_name = 'register/signup_complete.html'

    # # 認証の制限時間を設定
    # timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
    #
    # # 認証ページに飛んで来たら、tokenが正しいか判定。
    # # 正しくなければエラーページに飛ばし、正しければユーザーのステータスをactiveにする。
    # def get(self, request, **kwargs):
    #     token = kwargs.get('token')
    #     try:
    #         user_pk = loads(token, max_age=self.timeout_seconds)
    #
    #     except SignatureExpired:
    #         return HttpResponse("Expired error")
    #
    #     except BadSignature:
    #         return HttpResponse("token error")
    #
    #     else:
    #         try:
    #             user = mUser.objects.get(pk=user_pk)
    #
    #         except MyUser.DoesNotExist:
    #             return HttpResponseBadRequest()
    #         else:
    #             # TODO アクティブじゃなければログイン出来ないようにする？
    #             if not user.is_active:
    #                 user.is_active = True
    #                 user.save()
    #                 return super().get(request, **kwargs)
    #
    #     return HttpResponseBadRequest()

class ProfileView(TemplateView):
    template_name = 'pages/profile.html'
    lookup_field = 'username'

    # def get_context_data(self, *arg, **kwargs):
    #     logger.info(self.request.user)
    #     context = super().get_context_data(*arg, **kwargs)
    #     context.update({
    #         'mUser': mUser.objects.get(username=self.request.user)
    #     })
    #
    #     return context

class MessageView(TemplateView):
    template_name = 'pages/message.html'

class SettingView(TemplateView):
    template_name = 'pages/setting.html'

class BbsView(TemplateView):
    template_name = 'pages/bbs.html'

class InfoView(TemplateView):
    template_name = 'pages/info.html'
