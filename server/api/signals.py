from .models import (
    mUser,
    HashTag,
    Tweet,
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
    pre_bulk_update,
    post_bulk_update,
    MessageNotification,
    ReplyRelationShip,
)

from api.serializers import (
    ProfileSerializer,
    TweetSerializer,
    NotificationSerializer,
    MessageSubSerializer,
    MessageNotificationSerializer,
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


from ws.consumers import MessageConsumer, NotificationConsumer
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
    REPLY,
]


@receiver(m2m_changed, sender=mUser.followees.through)
def follow_receiver(sender, instance, action, reverse, model, pk_set, using, **kwargs):

    if action == 'post_add':
        try:
            receive_user = mUser.objects.get(pk=list(pk_set)[0])
            send_user = instance
            isExists = check_exists(FOLLOW, receive_user, send_user)
            isBlocked = check_blocked(receive_user, send_user)
            if not isExists and not isBlocked:
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
            isMyself = check_myself(receive_user, send_user)
            isBlocked = check_blocked(receive_user, send_user)
            if not isExists and not isMyself and not isBlocked:
                send_response(RETWEET, receive_user, send_user, target_instance)

        except RetweetRelationShip.DoesNotExist:
            logger.error('RetweetRelationShipが存在しません。')

    except mUser.DoesNotExist:
        logger.error('mUserが存在しません。')

@receiver(post_save, sender=ReplyRelationShip)
def reply_receiver(sender, instance, created, **kwargs):

    target_instance = instance.reply_target_tweet
    reply_instance = instance.reply

    receive_user = target_instance.author
    send_user = reply_instance.author

    try:
        isExists = check_exists(REPLY, receive_user, send_user, target_instance)
        isMyself = check_myself(receive_user, send_user)
        isBlocked = check_blocked(receive_user, send_user)
        if not isExists and not isMyself and not isBlocked:
            send_response(REPLY, receive_user, send_user, target_instance)

    except ReplyRelationShip.DoesNotExist:
        logger.error('ReplyRelationShipが存在しません。')



@receiver(m2m_changed, sender=Tweet.liked.through)
def liked_receiver(sender, instance, action, reverse, model, pk_set, using, **kwargs):

    if action == 'post_add' and instance.isRetweet == False:
        try:
            receive_user = instance.author
            send_user = mUser.objects.get(pk=list(pk_set)[0])
            isExists = check_exists(LIKED, receive_user, send_user, instance)
            isMyself = check_myself(receive_user, send_user)
            isBlocked = check_blocked(receive_user, send_user)

            if not isExists and not isMyself and not isBlocked:
                send_response(LIKED, receive_user, send_user, instance)

        except mUser.DoesNotExist:
            logger.error('mUserが存在しません。')

# @receiver(post_save, sender=Notification)
# def notification_receiver(sender, instance, created, raw, using, update_fields, **kwargs):
#     logger.debug('============Notification_receiver==================')
#     logger.debug(sender)
#     logger.debug('readed : ' + str(instance.readed))
#     logger.debug('created : ' + str(created))
#     logger.debug(raw)
#     logger.debug(using)
#     logger.debug(update_fields)
#     logger.debug(kwargs)
#
#
# @receiver(pre_save, sender=Notification)
# def notification_pre_receiver(sender, instance, raw, using, update_fields, **kwargs):
#     logger.debug('============Notification_PRE_receiver==================')
#     logger.debug(sender)
#     logger.debug('pk : ' + str(instance.pk))
#     logger.debug('readed : ' + str(instance.readed))
#     logger.debug(Notification.objects.all().last().pk)
#     logger.debug(Notification.objects.all().last().readed)


# @receiver(post_bulk_update, sender=Notification)
# def notification_receiver(sender, **kwargs):
#     logger.debug('============Notification_bulk_receiver==================')
#     logger.debug(kwargs)
    # instance = kwargs['instance']
    # update_kwargs = kwargs['update_kwargs']
    # logger.debug(instance)
    # logger.debug(update_kwargs)


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


def check_myself(receive_user, send_user):
    """
    自分自身に対するアクションじゃないかチェック
    """

    return receive_user == send_user

def check_blocked(receive_user, send_user):
    """
    対象ユーザーにブロックされていないかチェック
    """
    block_list = receive_user.msetting.block_list
    return block_list.filter(username=send_user.username).exists()


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

@receiver(post_bulk_update, sender=Message)
def send_read_message(sender, **kwargs):
    """
    対象ルームに対して、既読通知を送るメソッド
    """

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(kwargs['queryset'][0].room.id),
        {'type': 'read_message',  'data': MessageSubSerializer(kwargs['queryset'], many=True).data}
    )


@receiver(post_save, sender=Message)
def recevie_message(sender, instance, created, raw, using, update_fields, **kwargs):
    logger.info('メッセージが来た')

    try:
        target_room = instance.room
        sender = instance.sender
        receiver = target_room.users.exclude(username=sender.username)[0]
        isMyself = check_myself(receiver, sender)
        if not isMyself:
            send_message_notice(receiver, sender, target_room, instance)

    except mUser.DoesNotExist:
        logger.info('ユーザーが存在しません')

def send_message_notice(receiver, sender, room, message):
    """
    対象のレイヤーにメッセージの通知を送るメソッド
    """

    res = MessageNotification.objects.create(
        receiver=receiver,
        sender=sender,
        room=room,
        message=message,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        receiver.username,
        {'type': 'message_notification',  'content': MessageNotificationSerializer(res).data}
    )