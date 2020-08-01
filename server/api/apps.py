from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .signals import (
            follow_receiver,
            retweet_receiver,
            reply_receiver,
            liked_receiver,
            follow_request_receiver,
            send_read_message,
            recevie_message
        )
