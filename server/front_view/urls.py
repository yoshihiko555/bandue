from django.urls import path
from . import views

app_name = 'front_view'
urlpatterns = [
    path('', views.IsAuthView.as_view(), name='is-auth'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('explore/', views.ExploreView.as_view(), name='explore'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('message/', views.MessageView.as_view(), name='message'),
    path('setting/', views.SettingView.as_view(), name='setting'),
    path('bbs/', views.BbsView.as_view(), name='bbs'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
]
