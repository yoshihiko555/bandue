from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection
from django.db.utils import OperationalError
from channels.db import database_sync_to_async
from django.core import serializers
from django.utils import timezone
import json
from api.models import (
    mUser,
    Room,
    Message,
)
from urllib.parse import urlparse
import datetime
import time
import json
import logging
logger = logging.getLogger(__name__)

class MessageConsumer(AsyncWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        logger.info('コネクト')
        try:
            await self.accept()
            self.room_group_name = self.scope['url_route']['kwargs']['room_name']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            raise

    async def disconnect(self, close_code):
        logger.info('ディスコネクト')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        logger.info('受信')
        try:
            text_data_json = json.loads(text_data)
            logger.info(text_data_json)
            roomId = text_data_json['roomId']
            content = text_data_json['content']
            sender = text_data_json['sender']
            receiver = text_data_json['receiver']
            await self.createMessage(text_data_json)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'roomId': roomId,
                    'content': content,
                    'sender': sender,
                    'receiver': receiver,
                }
            )
        except Exception as e:
            raise

    async def chat_message(self, event):
        try:
            content = event['content']
            sender = event['sender']
            receiver = event['receiver']
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'content': content,
                'sender': sender,
                'receiver': receiver,
            }))
        except Exception as e:
            raise

    @database_sync_to_async
    def createMessage(self, event):
        logger.info('作成')
        try:
            room = Room.objects.get(id=event['roomId'])
            sender = mUser.objects.get(username=event['sender'])
            receiver = mUser.objects.get(username=event['receiver'])
            Message.objects.create(
                room=room,
                content=event['content'],
                sender=sender,
                receiver=receiver,
            )
        except Exception as e:
            raise
