# coding:utf-8
import pytz
import functools
import logging
import traceback
from bson import CodecOptions

LOCAL_TIMEZONE = pytz.timezone('Asia/Shanghai')
TRAE_DAYS = 245  # 一年交易日的天数

exceptionDic = {}


def exception(func):
    """
    用于捕获函数中的代码
    :param do:
     None       不抛出异常
     'raise'    继续抛出异常
    :return:
    """
    if func in exceptionDic:
        # 缓存
        return exceptionDic[func]

    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            logger = logging.getLogger()
            logger.error('{} {}'.format(str(args), str(kw)))
            logger.error(traceback.format_exc())
            raise

    # 缓存
    exceptionDic[func] = wrapper
    return wrapper


def getColTZ(col):
    """
    给 collection 查询添加时区
    :param col:
    :return:
    """
    return col.with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=LOCAL_TIMEZONE))
