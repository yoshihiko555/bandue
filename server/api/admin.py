from django.contrib import admin
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
    Age,
    ReadManagement,
    Notification,
    MessageNotification,
    ReplyRelationShip,
    FollowRequest,
)

admin.site.register(mUser)
# admin.site.register(MessageRelationShip)
admin.site.register(HashTag)
admin.site.register(Tweet)
admin.site.register(mSetting)
admin.site.register(hUserUpd)
admin.site.register(hTweetUpd)
admin.site.register(mAccessLog)
admin.site.register(Band)
admin.site.register(MemberShip)
admin.site.register(Entry)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Age)
admin.site.register(ReadManagement)
admin.site.register(Notification)
admin.site.register(MessageNotification)
admin.site.register(ReplyRelationShip)
admin.site.register(FollowRequest)
