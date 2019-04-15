import logging
import traceback
try:
    from slaveaccount.ctp.vnctpmd import MdApi
    from slaveaccount.ctp.vnctptd import TdApi
except ImportError:
    logging.info(traceback.format_exc())

from .ctp_constant import *