import time
import logging

from .models import (
    RetweetRelationShip,
    ReplyRelationShip,
)


logger = logging.getLogger(__name__)
def analyzeMethod(func):
    """
    メソッドを解析するデコレーター
        メソッドのargs, kwargs, result, 実行時間をログ上に表示する
    """
    def inner(*args, **kwargs):
        logger.debug('=====================================================================')
        logger.debug('========================This is AnalyzeMethod========================')
        logger.debug('=====================================================================')
        logger.debug('【関数名】  ====> ' + func.__name__)
        logger.debug(' ↓↓↓ 【Arguments】 ↓↓↓ ')
        logger.debug(args)
        logger.debug(' ↓↓↓ 【Keyword Aurguments】 ↓↓↓ ')
        logger.debug(kwargs)
        logger.debug(' ↓↓↓ 【実行結果】 ↓↓↓ ')
        start_time = time.time()
        res = func(*args, **kwargs)
        logger.debug(res)
        total_time = time.time() - start_time
        logger.debug('【実行時間】  ====> ' + str(total_time) + '[sec]')
        logger.debug('=====================================================================')
        logger.debug('========================AnalyzeMethod Finished========================')
        logger.debug('=====================================================================')
        return func(*args, **kwargs)
    return inner


def chunked(queryset, chunk_size=1000):
    """
    メモリに載りきらないような大量なデータを扱う時に、
    QuerySetを分割して実行するメソッド
    """

    start = 0
    while True:
        chunk = queryset[start: start + chunk_size]
        for obj in chunk:
            yield obj
        if len(chunk) < chunk_size:
            raise StopIteration
        start += chunk_size



def search_retweet_target(tweet):
    """
    リツイートの対象を取得するメソッド　
    """
    try:
        return RetweetRelationShip.objects.get(retweet=tweet).target_tweet
    except RetweetRelationShip.DoesNotExist:
        raise ObjectDoesNotExist


def search_reply_target(tweet):
    """
    リプライの対象を取得するメソッド
    """
    try:
        return ReplyRelationShip.objects.get(reply=tweet).reply_target_tweet
    except ReplyRelationShip.DoesNotExist:
        raise ObjectDoesNotExist


def search_retweet_reply_target(tweet):
    """
    リツイートのリプライの対象を取得するメソッド
    """
    try:
        return ReplyRelationShip.objects.get(reply=\
            RetweetRelationShip.objects.get(retweet=tweet).target_tweet).reply_target_tweet
    except ReplyRelationShip.DoesNotExist:
        raise ObjectDoesNotExist


def search_reply_target_base(tweet):
    """
    リプライの対象のベースツイートを取得するメソッド
    """
    try:
        return ReplyRelationShip.objects.get(reply=tweet).reply_target_base
    except ReplyRelationShip.DoesNotExist:
        raise ObjectDoesNotExist


def search_retweet_reply_target_base(tweet):
    """
    リツイートのリプライの対象のベースツイートを取得するメソッド
    """
    try:
        return ReplyRelationShip.objects.get(reply=\
            RetweetRelationShip.objects.get(retweet=tweet).target_tweet).reply_target_base
    except ReplyRelationShip.DoesNotExist:
        raise ObjectDoesNotExist

def is_base_tweet(tweet):
    """
    大元のツイートか判定
    """
    return tweet.isReply == False and tweet.isRetweet == False
