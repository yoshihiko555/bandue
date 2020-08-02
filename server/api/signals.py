from .models import (
    mUser,
    HashTag,
    Tweet,
    mSetting,
    hUserUpd,
    hTweetUpd,
    mAccessLog,
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
    FollowRequest,
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
FOLLOW_REQUEST = 4

NOTIFICATION_WORD = {
    FOLLOW: 'さんにフォローされました。',
    RETWEET: 'さんがあなたのツイートをリツイートしました。',
    LIKED: 'さんがあなたのツイートをいいねしました。',
    REPLY: 'さんからリプライが届きました。',
    FOLLOW_REQUEST: 'さんからフォロー申請が届きました。',
}

TWEET_EVENT = [
    RETWEET,
    LIKED,
    REPLY,
]



@receiver(m2m_changed, sender=mUser.followees.through)
def follow_receiver(sender, instance, action, pk_set, **kwargs):
    """
    フォローのレシーバー。
    manytomanyがaddされたらフォローされたユーザーに通知を送る。
    """

    if action == 'post_add':
        try:
            receive_user = mUser.objects.get(pk=list(pk_set)[0])
            send_user = instance
            isExists = check_exists(FOLLOW, receive_user, send_user)
            isBlocked = check_blocked(receive_user, send_user)
            isFollowRequest = check_isFollowRequest(receive_user, send_user)
            if not isExists and not isBlocked and not isFollowRequest:
                send_response(FOLLOW, receive_user, send_user)

        except mUser.DoesNotExist:
            logger.error('mUserが存在しません。')


@receiver(post_save, sender=RetweetRelationShip)
def retweet_receiver(sender, instance, created, **kwargs):
    """
    リツイートのレシーバー。
    リツイートが作成されたらリツイート元のユーザーに通知を送る。
    """

    if created:
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
    """
    リプライのレシーバー。
    リプライが作成されたらリプライ元のユーザーに通知を送る。
    """

    if created:
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
def liked_receiver(sender, instance, action, pk_set, **kwargs):
    """
    いいねのレシーバー。
    いいねされたら元のauthorに通知を送る。
    """

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


@receiver(post_save, sender=FollowRequest)
def follow_request_receiver(sender, instance, created, **kwargs):
    """
    フォロー申請のレシーバー。
    フォロー申請が作成されたら対象ユーザーに通知を送る。
    """

    if created == True:
        send_user = instance.follow_request_user
        receive_user = instance.follow_response_user

        isExists = check_exists(FOLLOW_REQUEST, receive_user, send_user)
        if not isExists:
            send_response(FOLLOW_REQUEST, receive_user, send_user)


"""
post_bulk_updateのテスト
"""
# @receiver(post_bulk_update, sender=Notification)
# def notification_receiver(sender, **kwargs):
#     logger.debug('============Notification_bulk_receiver==================')
#     logger.debug(kwargs)
#     instance = kwargs['instance']
#     update_kwargs = kwargs['update_kwargs']
#     logger.debug(instance)
#     logger.debug(update_kwargs)


def check_isFollowRequest(receive_user, send_user):
    """
    フォロー申請のデータがあるか、チェック
        True: 存在する。
        False: 存在しない。
    """

    try:
        FollowRequest.objects.get(
            follow_request_user=send_user,
            follow_response_user=receive_user
        ).delete()
    except FollowRequest.DoesNotExist:
        return False

    return True


def check_exists(event, receive_user, send_user, *args):
    """
    同じ通知で未読の通知があったら、被るためチェック。
        True: 存在する。
        False: 存在しない。
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
        # フォローは過去にフォローして事あったら通知送らない
        if event is FOLLOW:
            return Notification.objects.filter(
                event=event,
                receive_user=receive_user,
                send_user=send_user,
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
    自分自身に対するアクションじゃないかチェック。
    """

    return receive_user == send_user

def check_blocked(receive_user, send_user):
    """
    対象ユーザーにブロックされていないかチェック。
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
