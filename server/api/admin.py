from django.contrib import admin
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
    mUser_Room,
    Age,
)

admin.site.register(mUser)
# admin.site.register(MessageRelationShip)
admin.site.register(HashTag)
admin.site.register(Tweet)
admin.site.register(Reply)
admin.site.register(mSetting)
admin.site.register(hUserUpd)
admin.site.register(hTweetUpd)
admin.site.register(mAccessLog)
admin.site.register(Band)
admin.site.register(MemberShip)
admin.site.register(Entry)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(mUser_Room)
admin.site.register(Age)
