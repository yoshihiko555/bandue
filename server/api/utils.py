import time
import logging

logger = logging.getLogger(__name__)
def analyzeMethod(func):
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