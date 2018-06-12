# encoding: UTF-8

import logging
from .ctp_data_type import defineDict
try:
    from .vnctpmd import MdApi
    from .vnctptd import TdApi
except ImportError:
    logging.warning(u'加载 cptapid 失败')
