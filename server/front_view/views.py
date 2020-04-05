from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

class SignUpView(TemplateView):
    template_name = 'register/signup.html'

class SignInView(TemplateView):
    template_name = 'register/signin.html'
