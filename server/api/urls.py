from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.mUserViewSet)
router.register('tweet', views.TweetViewSet)
router.register('bbs', views.BbsViewSet)

app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('tweet/', views.TweetListView.as_view(), name='tweet-list'),
    # path('tweet/<int:pk>/', views.TweetDetailView.as_view(), name='tweet-detail'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    # path('bbs/', views.BbsListView.as_view(), name='bbs-list'),
    # path('bbs/<int:pk>/', views.BbsDetailView.as_view(), name='bbs-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('signout/', views.SignOutView.as_view(), name='signout'),
    path('', include(router.urls)),
]
