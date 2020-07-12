from .models import (
    mUser,
    HashTag,
    Tweet,
    Reply,
    mSetting,
    hUserUpd,
    hTweetUpd,
    mAccessLog,
    Band,
    MemberShip,
    Entry,
    Room,
    Message,
    ReadManagement,
    FollowRelationShip,
    RetweetRelationShip,
    Notification,
)

from api.serializers import (
    ProfileSerializer,
    TweetSerializer,
    NotificationSerializer,
)


import logging
import requests
import json

from .utils import (
    analyzeMethod,
)

from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
)

from django.core.signals import (
    request_started,
    request_finished,
)

from django.dispatch import receiver


logger = logging.getLogger(__name__)


from ws.consumers import NotificationConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


FOLLOW = 0
RETWEET = 1
LIKED = 2
REPLY = 3

NOTIFICATION_WORD = {
    FOLLOW: 'さんにフォローされました。',
    RETWEET: 'さんがあなたのツイートをリツイートしました。',
    LIKED: 'さんがあなたのツイートをいいねしました。',
    REPLY: 'さんからリプライが届きました。',
}

TWEET_EVENT = [
    RETWEET,
    LIKED,
    REPLY
]



@receiver(m2m_changed, sender=mUser.followees.through)
def follow_receiver(sender, instance, action, reverse, model, pk_set, using, **kwargs):

    if action == 'post_add':
        try:
            receive_user = mUser.objects.get(pk=list(pk_set)[0])
            send_user = instance
            isExists = check_exists(FOLLOW, receive_user, send_user)
            if not isExists:
                send_response(FOLLOW, receive_user, send_user)

        except mUser.DoesNotExist:
            logger.error('mUserが存在しません。')


@receiver(post_save, sender=RetweetRelationShip)
def retweet_receiver(sender, instance, created, raw, using, update_fields, **kwargs):

    try:
        target_instance = instance.target_tweet
        retweet_instance = instance.retweet

        receive_user = target_instance.author
        send_user = mUser.objects.get(username=instance.retweet_user)

        try:
            isExists = check_exists(RETWEET, receive_user, send_user, target_instance)
            if not isExists:
                send_response(RETWEET, receive_user, send_user, target_instance)

        except RetweetRelationShip.DoesNotExist:
            logger.error('RetweetRelationShipが存在しません。')

    except mUser.DoesNotExist:
        logger.error('mUserが存在しません。')


@receiver(m2m_changed, sender=Tweet.liked.through)
def liked_receiver(sender, instance, action, reverse, model, pk_set, using, **kwargs):

    if action == 'post_add' and instance.isRetweet == False:
        try:
            receive_user = instance.author
            send_user = mUser.objects.get(pk=list(pk_set)[0])
            isExists = check_exists(LIKED, receive_user, send_user, instance)

            if not isExists:
                send_response(LIKED, receive_user, send_user, instance)

        except mUser.DoesNotExist:
            logger.error('mUserが存在しません。')


def check_exists(event, receive_user, send_user, *args):
    """
    同じ通知で未読の通知があったら、被るためチェック
    """

    if event in TWEET_EVENT:
        return Notification.objects.filter(
            event=event,
            receive_user=receive_user,
            send_user=send_user,
            target_tweet_info=args[0],
            readed=False,
        ).exists()
    else:
        return Notification.objects.filter(
            event=event,
            receive_user=receive_user,
            send_user=send_user,
            readed=False,
        ).exists()


def send_response(event, receive_user, send_user, *args):
    """
    対象のレイヤーに通知を送るメソッド。
    ツイート関連の通知ならツイート情報も追加する。
    """

    if event in TWEET_EVENT:

        res = Notification.objects.create(
            event=event,
            receive_user=receive_user,
            send_user=send_user,
            target_tweet_info=args[0],
            infomation=send_user.username + NOTIFICATION_WORD[event]
        )
    else:
        res = Notification.objects.create(
            event=event,
            receive_user=receive_user,
            send_user=send_user,
            infomation=send_user.username + NOTIFICATION_WORD[event]
        )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        receive_user.username,
        {'type': 'notification',  'content': NotificationSerializer(res).data}
    )
