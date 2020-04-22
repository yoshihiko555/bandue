import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import mUser
import logging

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'pages/index.html'

class SignUpView(TemplateView):
    template_name = 'register/signup.html'

class SignInView(TemplateView):
    template_name = 'register/signin.html'

class ProfileView(TemplateView):
    template_name = 'pages/profile.html'

    def get_context_data(self, *arg, **kwargs):
        logger.info(self.request.user)
        context = super().get_context_data(*arg, **kwargs)
        context.update({
            'mUser': mUser.objects.get(username=self.request.user)
        })

        return context

class MessageView(TemplateView):
    template_name = 'pages/message.html'

class SettingView(TemplateView):
    template_name = 'pages/setting.html'

class BssView(TemplateView):
    template_name = 'pages/bss.html'
