from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/user/<str:username>/', consumers.NotificationConsumer),
    path('ws/<slug:room_name>/', consumers.MessageConsumer),
]
