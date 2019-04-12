# encoding: UTF-8
import logging
from pymongo import MongoClient
from threading import Event, Thread
from collections import defaultdict

from .object import *


########################################################################
class Gateway(object):
    """交易接口"""

    # ----------------------------------------------------------------------
    def __init__(self, config, gatewayName, userID, client):
        """Constructor"""

        self.config = config
        self.gatewayName = '{}.{}'.format(gatewayName, userID)
        self.clinet = client  # pymongo.MongoClient

        self.logger = logging.getLogger(self.gatewayName)
        self.account = VtAccountData()
        self.position = VtPositionData()
        self.banks = {}


    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """市场行情推送"""
        # 通用事件
        # event1 = Event(type_=EVENT_TICK)
        # event1.dict_['data'] = tick
        # self.eventEngine.put(event1)
        #
        # # 特定合约代码的事件
        # event2 = Event(type_=EVENT_TICK + tick.vtSymbol)
        # event2.dict_['data'] = tick
        # self.eventEngine.put(event2)

    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        """成交信息推送"""
        # 通用事件
        # event1 = Event(type_=EVENT_TRADE)
        # event1.dict_['data'] = trade
        # self.eventEngine.put(event1)
        #
        # # 特定合约的成交事件
        # event2 = Event(type_=EVENT_TRADE + trade.vtSymbol)
        # event2.dict_['data'] = trade
        # self.eventEngine.put(event2)

        # ----------------------------------------------------------------------

    def onOrder(self, order):
        """订单变化推送"""
        # 通用事件
        # event1 = Event(type_=EVENT_ORDER)
        # event1.dict_['data'] = order
        # self.eventEngine.put(event1)
        #
        # # 特定订单编号的事件
        # event2 = Event(type_=EVENT_ORDER + order.vtOrderID)
        # event2.dict_['data'] = order
        # self.eventEngine.put(event2)

    # ----------------------------------------------------------------------
    def onPosition(self, position):
        """持仓信息推送"""
        log = ''
        for k, v in list(position.__dict__.items()):
            log += '{}\t{}\n'.format(k, v)
            # 更新持仓状态
            setattr(self.position, k, v)
            # self.logger.info(log)

            # 通用事件
            # event1 = Event(type_=EVENT_POSITION)
            # event1.dict_['data'] = position
            # self.eventEngine.put(event1)
            #
            # # 特定合约代码的事件
            # event2 = Event(type_=EVENT_POSITION + position.vtSymbol)
            # event2.dict_['data'] = position
            # self.eventEngine.put(event2)

    # ----------------------------------------------------------------------
    def onAccount(self, account):
        """账户信息推送"""
        log = ''
        for k, v in list(account.__dict__.items()):
            log += '{}\t{}\n'.format(k, v)
            # 更新账号状态
            setattr(self.account, k, v)
        # self.logger.info(log)

    # ----------------------------------------------------------------------
    def onError(self, error):
        """错误信息推送"""
        # 通用事件
        # event1 = Event(type_=EVENT_ERROR)
        # event1.dict_['data'] = error
        # self.eventEngine.put(event1)

        # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def onContract(self, contract):
        """合约基础信息推送"""
        # # 通用事件
        # event1 = Event(type_=EVENT_CONTRACT)
        # event1.dict_['data'] = contract
        # self.eventEngine.put(event1)

        # ----------------------------------------------------------------------

    def connect(self):
        """连接"""
        pass

    # ----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """订阅行情"""
        pass

    # ----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        pass

    # ----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        pass

    # ----------------------------------------------------------------------
    def qryAccount(self):
        """查询账户资金"""
        pass

    # ----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        pass

    # ----------------------------------------------------------------------
    def close(self):
        """关闭"""
        pass

    def onAccountRegister(self, bankAccount):
        """
        :param bankAccount:
        :return:
        """
        # 每个银行只有一个实例
        self.banks[bankAccount.bankAccount] = bankAccount

    def onTransferSerial(self, transferSerial):
        """

        :param transferSerial:
        :return:
        """
        assert isinstance(transferSerial, VtTransferSerialData)
        log = ''
        for k, v in list(transferSerial.__dict__.items()):
            log += '{}\t{}\n'.format(k, v)

        self.logger.info(log)


    def run(self):
        raise NotImplementedError
