from django.urls import path
from . import views

app_name = 'front_view'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<path:path>', views.HomeView.as_view(), name='sub_home'),
    # path('home/', views.HomeView.as_view(), name='home'),
    # path('explore/', views.ExploreView.as_view(), name='explore'),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('signup_complete/<token>/', views.SignUpCompleteView.as_view(), name='signup-comp'),
    # path('signin/', views.SignInView.as_view(), name='signin'),
    # path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    # path('message/', views.MessageView.as_view(), name='message'),
    # path('setting/', views.SettingView.as_view(), name='setting'),
    # path('bbs/', views.BbsView.as_view(), name='bbs'),
    # path('info/', views.InfoView.as_view(), name='info'),
    # path('404/', views.PageNotFoundView.as_view(), name='page_not_found'),
    # path('<str:username>/', views.ProfileView.as_view(), name='profile'),
]
