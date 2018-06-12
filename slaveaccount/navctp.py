# coding:utf-8
import logging
import arrow


class Navctp(object):
    """
    计算 ctp 的收盘净值
    """

    def __init__(self, userID, cal):
        self.userID = userID
        self.cal = cal

        d = arrow.get(self.config.get(self.userID, 'navtStartDate'))
        self.startDate = arrow.get('{} 00:00:00+08'.format(d.strftime('%Y-%m-%d'))).datetime

    @property
    def config(self):
        return self.config

    @property
    def client(self):
        return self.client

    @property
    def balanceMinCol(self):
        return self.balanceMinCol

    @property
    def balanceDailyCol(self):
        return self.balanceDailyCol

    @property
    def transferSerialCol(self):
        return self.transferSerialCol

    def run(self):
        """
        计算净值
        :return:
        """
        # TODO 读取收盘权益
        self.client
        # TODO 读取出入金

        # TODO 只有1个净值日期

        # TODO 获得盘尾权益

        # TODO 获得上一个工作日权益
