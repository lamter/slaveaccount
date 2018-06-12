# coding:utf-8
import arrow
import pandas as pd
import os
import matplotlib.pyplot as plt

from .ctp import defineDict
from myplot.nav import draw_nav


class Navctp(object):
    """
    计算 ctp 的收盘净值
    """

    def __init__(self, userID, cal):
        self.userID = userID
        self.cal = cal

        d = arrow.get(self.config.get(self.userID, 'navtStartDate'))
        self.startDate = arrow.get('{} 00:00:00+08'.format(d.strftime('%Y-%m-%d'))).datetime

        self.balanceDF = None  # 权益数据
        self.transferSerialDF = None  # 出入金数据
        self.navDF = None  # 计算出来的净值和回撤等

    @property
    def config(self):
        return self.cal.config

    @property
    def client(self):
        return self.cal.client

    @property
    def balanceMinCol(self):
        return self.cal.balanceMinCol

    @property
    def balanceDailyCol(self):
        return self.cal.balanceDailyCol

    @property
    def transferSerialCol(self):
        return self.cal.transferSerialCol

    def loadBalance(self):
        sql = {
            'accountID': self.userID,
            'tradingDay': {
                '$gte': self.startDate
            }
        }
        cursor = self.balanceDailyCol.find(sql, {'_id': 0})
        if cursor.count() == 0:
            raise ValueError(u'没有任何权益数据')

        # 账户权益
        self.balanceDF = pd.DataFrame((_ for _ in cursor)).set_index('tradingDay').sort_index()

    def loadTransferSerial(self):
        """
        读取出入金流水
        :return:
        """
        sql = {
            'accountID': self.userID,
            'tradingDay': {
                '$gte': self.startDate
            }
        }
        cursor = self.transferSerialCol.find(sql, {'_id': 0})
        if cursor.count() == 0:
            raise ValueError(u'没有任何出入金数据')

        # 出入金流水
        df = pd.DataFrame((_ for _ in cursor))

        # 统计每天累计的出入金
        # 出入金分辨

        # 入金是正数，出金是负数
        df['intOut'] = df.tradeCode.apply(self.tradeCode2)
        # 计算出入金总额
        df['tradeAmount'] *= df['intOut']
        df = df[['tradeAmount', 'tradingDay']]
        df = df.groupby('tradingDay').sum().sort_index()
        self.transferSerialDF = df

    @staticmethod
    def tradeCode2(v):
        # 银行发起银行转期货
        if defineDict["THOST_FTDC_FTC_BankLaunchBankToBroker"] == v:
            return -1
        # 期货发起银行转期货
        if defineDict["THOST_FTDC_FTC_BrokerLaunchBankToBroker"] == v:
            return -1
        # 银行发起期货转银行
        if defineDict["THOST_FTDC_FTC_BankLaunchBrokerToBank"] == v:
            return 1
        # 期货发起期货转银行
        if defineDict["THOST_FTDC_FTC_BrokerLaunchBrokerToBank"] == v:
            return 1

    def calNav(self):
        """
        计算净值回撤等
        :return:
        """
        df = self.balanceDF[['balance']].copy()
        df['transferSerial'] = self.transferSerialDF['tradeAmount']
        # 没有出入金的交易日补0
        df['transferSerial'] = df['transferSerial'].fillna(0)
        # 将盘尾净值去掉出入金
        df['today'] = df['balance'] + df['transferSerial']
        df['pre'] = df['balance'].shift().fillna(method='bfill')

        # 净值和每天的增长率
        df['rate'] = df['today'] / df['pre']
        df['nav'] = df['rate'].cumprod()
        df['rate'] = df['rate'] - 1

        # 计算回撤
        self._max = 0

        def getMax(v):
            self._max = max(self._max, v)
            return self._max

        df['_max'] = df['nav'].apply(getMax)
        df['dropdown'] = df['nav'] / df['_max'] - 1

        self.navDF = df

    def draw(self):
        """
        :return:
        """
        # 绘制净值图
        path = self.config.get('CTP', 'navfigpath')
        with draw_nav(self.navDF['nav'], u'净值') as subplot:
            fn = u'{}_nav.png'.format(self.userID)
            plt.savefig(os.path.join(path, fn))

        # 绘制回撤图
        with draw_nav(self.navDF['dropdown'], u'回撤') as subplot:
            fn = u'{}_dropdown.png'.format(self.userID)
            plt.savefig(os.path.join(path, fn))

    def run(self):
        """
        计算净值
        :return:
        """
        # 读取盘尾权益
        self.loadBalance()

        # 读取出入金
        self.loadTransferSerial()

        # 计算净值、回撤等
        self.calNav()

        # 生成图片
        self.draw()
