from django_filters import rest_framework as django_filter
from django.db.models import Q
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
)
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import get_object_or_404



class TweetFilter(django_filter.FilterSet):
    """
    ツイートを絞るフィルタークラス

        Parameters
        -----------------------------------------
        tweetListFlg : ページによってツイートを絞る

        searchFlg : 検索文字によってツイートを絞る
            0 => トレンド
            1 => 新着順
            3 => 画像ありツイート

        searchText : 検索文字列
    """

    def __init__(self, *args, **kwargs):
        self.target_user = kwargs['data']['targetUser'] if 'targetUser' in kwargs['data'] else None
        self.searchFlg = kwargs['data']['searchFlg'] if 'searchFlg' in kwargs['data'] else None
        super().__init__(*args, **kwargs)

    tweetListFlg = django_filter.NumberFilter(method='tweet_filter')
    searchText = django_filter.CharFilter(field_name='content', method='content_filter')
    deleted = django_filter.BooleanFilter(field_name='deleted', method='deleted_filter')


    class Meta:
        model = Tweet
        fields = ['deleted']

    # 検索文字からツイートを絞る
    def content_filter(self, queryset, name, value):
        logger.debug('=====CONTENT_FILTER=====')

        h_list = []
        q_list = []
        qs = list({i.strip() for i in value.split(',')})
        for q in qs:
            if q[0] == '#':
                h_list.append('Q(hashTag__title=q)')
            else:
                q_list.append('Q(content__contains=q)')
        query_str = '&'.join(q_list) + '|'.join(h_list)

        q = Tweet.objects.filter(eval(query_str))
        # TODO トレンド順
        if self.searchFlg == '0':
            logger.debug('=====================================トレンド============================================')
            q = q.order_by('-created_at')

        # 新着順
        elif self.searchFlg == '1':
            q = q.order_by('-created_at')

        # 画像ある該当ツイートで新着順
        elif self.searchFlg == '3':
            q = q.exclude(images__isnull=False).order_by('-created_at')

        logger.debug('検索結果 : ')
        logger.debug(q)
        return q


    # ページによってTweetを絞る
    def tweet_filter(self, queryset, name, value):
        logger.debug('=====TWEET_FILTER=====')
        res = queryset
        if self.target_user != None:

            # target_user = mUser.objects.get(username=self.target_user)
            target_user = get_object_or_404(mUser, username=self.target_user)

            # リプライツイート除いた一覧
            if value == 0:

                t_list = Tweet.objects.filter( \
                    author=target_user).exclude(Q(isRetweet=True) & \
                        Q(author=target_user) & Q(retweet_username=self.target_user))
                res = t_list.exclude(reply__isnull=False).order_by('-created_at')

            # リプライツイート含めた一覧
            elif value == 1:

                res = target_user.author.all().exclude(Q(isRetweet=True) & \
                    Q(author=target_user) & Q(retweet_username=self.target_user)).order_by('-created_at')

            # 画像含めた一覧
            elif value == 2:
                res = target_user.author.all().exclude( \
                    Q(images__isnull=False) | Q(author=target_user) & \
                        Q(retweet_username=self.target_user)).order_by('-created_at')

            # いいねしたツイート一覧
            elif value == 3:
                res = target_user.liked.all().order_by('-created_at')

            # ユーザー&フォローユーザーツイート一覧
            elif value == 4:
                my_tweets = target_user.author.all().exclude()

                followees_tweets = Tweet.objects.filter( \
                    author__in=target_user.followees.all()).exclude(isRetweet=True)

                followees_retweets = Tweet.objects.filter( \
                    pk__in=RetweetRelationShip.objects.filter( \
                        retweet_user__in=target_user.followees.all()))

                res = my_tweets.union(followees_tweets).union(followees_retweets).order_by('-created_at')

        logger.debug('--TWEET_FILTER_RESULT--')
        logger.debug(res)
        return res


    def deleted_filter(self, queryset, name, value):

        logger.debug('====DELETED_FILTER====')
        logger.debug(name)
        logger.debug(value)
        lookup = '__'.join([name, 'isnull'])
        res = queryset.filter(**{lookup: value})
        logger.debug('--result--')
        logger.debug(res)
        return res


    def get_username(self):

        return self.target_user if self.target_user != None else None



class MUserFilter(django_filter.FilterSet):
    """
    ユーザーを絞るフィルタークラス

        Parameters
        --------------------------------------------------------
        self.login_userを元にログインユーザー以外の該当ユーザーを絞る
    """

    searchText = django_filter.CharFilter(field_name='username', method='username_filter')

    class Meta:
        model = mUser
        fields = ['username']

    def __init__(self, *args, **kwargs):
        self.login_user = kwargs['data']['loginUser'] if 'loginUser' in kwargs['data'] else None
        super().__init__(*args, **kwargs)

    def username_filter(self, queryset, name, value):

        # 同じ検索ワード, ハッシュタグは省く
        q_list = list({Q(username__contains=i.strip()) for i in value.split(',') if i.strip()[0] != '#'})
        return mUser.objects.filter(*q_list).exclude(username=self.login_user)


class EntryFilter(django_filter.FilterSet):
    """
    記事一覧を絞るフィルタークラス
    """

    entryListFlg = django_filter.NumberFilter(method='entry_filter')

    class Meta:
        model = Entry
        fields = ['title']

    def entry_filter(self, queryset, name, value):
        logger.info('------Entry Filter------')
        res = queryset

        if value == 0:
            # 人気記事一覧
            res = Entry.objects.filter(is_public=False).order_by('-read_count')
        elif value == 1:
            # 新着記事一覧
            res = Entry.objects.filter(is_public=False).order_by('-created_at')

        logger.info(res)

        return res
