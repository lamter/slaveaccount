# coding:utf-8
'''
盘尾进行净值计算的操作
'''
import traceback
import pymongo
import pymongo.database
import logging
from .navctp import Navctp
from .dealutils import getColTZ


class Calnav(object):
    def __init__(self, config, client):
        self.logger = logging.getLogger()
        self.config = config
        self.client = client  # pymongo.MongoClient
        # 净值始末日期

    def dbConnect(self):
        self.logger.info('链接MongoDB')
        config = self.config
        self.db = self.client[config.get('mongodb', 'dbn')]
        assert isinstance(self.db, pymongo.database.Database)
        self.db.authenticate(
            config.get('mongodb', 'username'),
            config.get('mongodb', 'password')
        )

        # 检查链接是否成功
        self.client.server_info()

        self.balanceMinCol = getColTZ(self.db['ctp_balance_min'])  # 权益分钟线
        self.balanceDailyCol = getColTZ(self.db['ctp_balance_daily'])  # 收盘权益
        self.transferSerialCol = getColTZ(self.db['transfer_serial'])  # 转账记录

    def calCtpNav(self):
        """
        计算 ctp 账户的收盘净值
        :return:
        """
        userIDs = self.config.get('CTP', 'userIDs').split(',')
        for userID in userIDs:
            try:
                self.n = Navctp(userID, self)
                self.n.run()
            except Exception:
                self.logger.error(traceback.format_exc())

    def run(self):
        """
        计算净值
        :return:
        """
        self.dbConnect()
        self.calCtpNav()
