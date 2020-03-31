from django.contrib import admin
from .models import (
    mUser,
    Message,
    # MessageRelationShip,
    HashTag,
    Tweet,
    Reply,
    mSetting,
    hUserUpd,
    hTweetUpd,
    mAccessLog,
    Group,
    MemberShip
)

admin.site.register(mUser)
admin.site.register(Message)
# admin.site.register(MessageRelationShip)
admin.site.register(HashTag)
admin.site.register(Tweet)
admin.site.register(Reply)
admin.site.register(mSetting)
admin.site.register(hUserUpd)
admin.site.register(hTweetUpd)
admin.site.register(mAccessLog)
admin.site.register(Group)
admin.site.register(MemberShip)
