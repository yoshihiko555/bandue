from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .signals import (
            liked_receiver,
            follow_receiver,
            retweet_receiver,
        )
