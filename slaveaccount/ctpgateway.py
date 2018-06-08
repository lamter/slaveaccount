# encoding: UTF-8

'''
vn.ctp的gateway接入

考虑到现阶段大部分CTP中的ExchangeID字段返回的都是空值
vtSymbol直接使用symbol
'''
import traceback
import datetime as dt
import pymongo.database
from pymongo import IndexModel, DESCENDING, ASCENDING
from pymongo.errors import OperationFailure
from threading import Event, Thread, Timer

import arrow
import tradingtime as tt

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from .gateway import Gateway
from .constant import *
from .ctpmdapi import CtpMdApi
from .ctptdapi import CtpTdApi
from .object import VtQuery, VtSaveMongodbData


########################################################################
class CtpGateway(Gateway):
    """CTP接口"""

    # ----------------------------------------------------------------------
    def __init__(self, config, gatewayName, userID, client):
        """Constructor"""
        super(CtpGateway, self).__init__(config, gatewayName, userID, client)

        self.confg = config
        self.userID = userID
        self.password = config.get(userID, 'password')
        self.brokerID = config.get(userID, 'brokerID')
        self.tdAddress = config.get(userID, 'tdAddress')
        self.mdAddress = config.get(userID, 'mdAddress')
        self.db = None
        self.authCode = None
        self.userProductInfo = None

        self.mdApi = CtpMdApi(self)  # 行情API
        self.tdApi = CtpTdApi(self)  # 交易API

        self.mdConnected = False  # 行情API连接状态，登录完成后为True
        self.tdConnected = False  # 交易API连接状态

        # 交易流水
        self.transferSerials = {}

        # 查询定时器
        self.qryTransferSerialTimer = None
        self.qryAccountTimer = None

        # 存库定时器
        self.saveAccountTimer = None

        # 查询队列
        self.qryQueue = Queue()  # VtQuery

        self.stoped = Event()
        self.queryForever = Thread(name='query', target=self.query)

        self.saveQueue = Queue()  # VtSaveMongodbData
        self.saveForever = Thread(name='save', target=self._save)

    def run(self):
        self.dbconnect()
        self.setQryEnabled(True)
        self.connect()
        self.queryForever.start()
        self.saveForever.start()

    def dbconnect(self):
        """
        建立数据库链接
        :return:
        """
        self.logger.info(u'链接MongoDB')
        config = self.config
        self.db = self.clinet[config.get('mongodb', 'dbn')]
        assert isinstance(self.db, pymongo.database.Database)
        self.db.authenticate(
            config.get('mongodb', 'username'),
            config.get('mongodb', 'password')
        )

        # 检查链接是否成功
        self.clinet.server_info()

        self.balanceMinCol = self.db['ctp_balance_min']  # 权益分钟线
        self.balanceDailyCol = self.db['ctp_balance_daily']  # 收盘权益
        self.transferSerialCol = self.db['transfer_serial']  # 转账记录

        self.initContractCollection()

    def initContractCollection(self):
        # 需要建立的索引
        indexUserID = IndexModel([('userID', ASCENDING)], name='userID', background=True)
        indexTradingDay = IndexModel([('tradingDay', DESCENDING)], name='tradingDay', background=True)
        indexes = [indexUserID, indexTradingDay]

        self._initCollectionIndex(self.balanceMinCol, indexes)
        self._initCollectionIndex(self.balanceDailyCol, indexes)

        indexUserID = IndexModel([('accountID', ASCENDING)], name='accountID', background=True)
        indexTradingDay = IndexModel([('tradingDay', DESCENDING)], name='tradingDay', background=True)
        indexFutureSerial = IndexModel([('futureSerial', DESCENDING)], name='futureSerial', background=True)
        indexes = [indexUserID, indexTradingDay, indexFutureSerial]
        self._initCollectionIndex(self.transferSerialCol, indexes)

    def _initCollectionIndex(self, col, indexes):
        """
        初始化分钟线的 collection
        :return:
        """

        # 检查索引
        try:
            indexInformation = col.index_information()
            for indexModel in indexes:
                if indexModel.document['name'] not in indexInformation:
                    col.create_indexes(
                        [
                            indexModel,
                        ],
                    )
        except OperationFailure:
            # 有索引
            col.create_indexes(indexes)

    # ----------------------------------------------------------------------
    def connect(self):
        """连接"""

        # 创建行情和交易接口对象
        self.mdApi.connect(self.userID, self.password, self.brokerID, self.mdAddress)
        self.tdApi.connect(self.userID, self.password, self.brokerID, self.tdAddress, self.authCode,
                           self.userProductInfo)

        # 初始化并启动查询
        self.initQuery()

    # ----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """订阅行情"""
        self.mdApi.subscribe(subscribeReq)

    # ----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        return self.tdApi.sendOrder(orderReq)

    # ----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        self.tdApi.cancelOrder(cancelOrderReq)

    # ----------------------------------------------------------------------
    def qryAccount(self):
        """查询账户资金"""
        self.tdApi.qryAccount()
        self.setQryAccountTimer()

    def onAccount(self, account):
        # 时间到了就进行保存
        self.setQryAccountTimer()
        if not self.saveAccountTimer:
            # 还没有计时器
            self.setSavePositionTimer()
        elif self.saveAccountTimer.isAlive():
            # 已经有计时器了
            pass
        else:
            # 已经有计时器了，但是已经触发了
            self.setSavePositionTimer()
        return super(CtpGateway, self).onAccount(account)

    def setSavePositionTimer(self):
        # 设置1分钟后存库
        def foo():
            document = self.account.__dict__.copy()
            now = arrow.now().replace(second=0, microsecond=0).datetime
            document['datetime'] = now
            is_tradingtime, tradeday = tt.get_tradingday(now)
            document['tradingDay'] = tradeday

            documentDaily = document.copy()

            # 分钟净值
            vtSave = VtSaveMongodbData(self.balanceMinCol.insert_one, (document,))
            self.saveQueue.put(vtSave)

            # 日线净值
            _filter = {
                'accountID': documentDaily['accountID'],
                'tradingDay': tradeday,
            }
            # 日净值
            vtSave = VtSaveMongodbData(self.balanceDailyCol.update_one, (_filter, {'$set': documentDaily},), {'upsert': True})
            self.saveQueue.put(vtSave)

        moment = now = dt.datetime.now()
        wait = 0
        for wait in range(60):
            # 等到整分钟的时候才存库
            moment += dt.timedelta(seconds=1)
            if moment.minute != now.minute:
                break
        self.saveAccountTimer = t = Timer(wait, foo)
        t.daemon = True
        t.start()

    def setQryAccountTimer(self):
        def foo():
            q = VtQuery(self.qryAccount)
            self.qryQueue.put(q)

        if self.qryAccountTimer:
            self.qryAccountTimer.cancel()
        self.qryAccountTimer = t = Timer(10, foo)
        t.daemon = True
        t.start()

    # ----------------------------------------------------------------------
    def qryAccountregister(self):
        """查询签约银行"""
        self.tdApi.qryAccountregister()

    def onAccountRegister(self, bankAccount):
        return super(CtpGateway, self).onAccountRegister(bankAccount)

    # ----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        self.tdApi.qryPosition()

    def qryTransferSerial(self):
        """
        查询入金
        :return:
        """
        self.tdApi.qryTransferSerial()

        # 设置定时查询
        self.setQryTransferSerialTimer()

    def onTransferSerial(self, transferSerial):
        """
        响应转账流水
        :return:
        """
        r = super(CtpGateway, self).onTransferSerial(transferSerial)

        # 记录转账流水
        _id = transferSerial.futureSerial
        if _id not in self.transferSerials:
            self.transferSerials[_id] = transferSerial
            _filter = {
                'futureSerial': transferSerial.futureSerial,
                'tradingDay': transferSerial.tradingDay,
            }
            document = {'$set': transferSerial.__dict__.copy()}

            s = VtSaveMongodbData(
                self.transferSerialCol.update_one,
                (_filter, document,),
                {'upsert': True}
            )
            self.saveQueue.put(s)

        self.setQryTransferSerialTimer()

        return r

    def setQryTransferSerialTimer(self):
        # 每分钟查询一次
        def foo():
            q = VtQuery(self.qryTransferSerial)
            self.qryQueue.put(q)

        if self.qryTransferSerialTimer:
            self.qryTransferSerialTimer.cancel()
        self.qryTransferSerialTimer = t = Timer(60, foo)
        t.daemon = True
        t.start()

    # ----------------------------------------------------------------------
    def close(self):
        """关闭"""
        self.stoped.set()

        if self.mdConnected:
            self.mdApi.close()
        if self.tdConnected:
            self.tdApi.close()

    # ----------------------------------------------------------------------
    def initQuery(self):
        """初始化连续查询"""

        queries = []

        # 签约银行
        q = VtQuery(self.qryAccountregister)
        queries.append(q)

        # 查询出入金
        q = VtQuery(self.qryTransferSerial)
        queries.append(q)

        q = VtQuery(self.qryAccount)
        queries.append(q)

        # self.qryPosition,  # TODO 查询持仓

        for q in queries:
            self.qryQueue.put(q)

    # ----------------------------------------------------------------------
    def query(self):
        """注册到事件处理引擎上的查询函数"""

        while not self.stoped.wait(3):
            # 查询间隔为3秒
            try:
                vtQuery = self.qryQueue.get_nowait()
                assert isinstance(vtQuery, VtQuery)
            except Empty:
                continue

            try:
                vtQuery.func(*vtQuery.args, **vtQuery.kwargs)
            except Exception:
                self.logger.error(traceback.format_exc())

    # ----------------------------------------------------------------------
    def setQryEnabled(self, qryEnabled):
        """设置是否要启动循环查询"""
        self.qryEnabled = qryEnabled

    def _save(self):
        """
        将数据存库
        :return:
        """
        while not self.stoped.wait(0):
            try:
                vtSave = self.saveQueue.get(timeout=1)
            except Empty:
                continue

            try:
                vtSave.func(*vtSave.args, **vtSave.kwargs)
            except Exception:
                self.logger.error(traceback.format_exc())
