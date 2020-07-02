from django.urls import path, include
from . import views, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', viewsets.mUserViewSet)
router.register('tweet', viewsets.TweetViewSet)
router.register('reply', viewsets.ReplyViewSet)
router.register('room', viewsets.RoomViewSet)
router.register('message', viewsets.MessageViewSet)
router.register('entry', viewsets.EntryViewSet)

app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', include(router.urls)),
    path('search/', views.SearchView.as_view(), name='search'),
    path('setting/<int:pk>/', views.SettingView.as_view(), name='setting'),
    # path('setting/<str:username>/', views.SettingView.as_view(), name='setting'),
]
