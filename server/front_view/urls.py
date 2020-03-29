from django.urls import path
from . import views

app_name = 'front_view'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
