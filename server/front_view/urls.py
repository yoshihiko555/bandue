from django.urls import path
from . import views

app_name = 'front_view'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('message/', views.MessageView.as_view(), name='message'),
    path('setting/', views.SettingView.as_view(), name='setting'),
    path('bbs/', views.BbsView.as_view(), name='bbs'),
]
