# coding:utf-8
import os
import signal
import traceback
import sys
from threading import Event
import logging.config
from slaveaccount.ctpgateway import CtpGateway
from pymongo import MongoClient

import ConfigParser

if __debug__:
    path = '/srv/slaveaccount/tmp/'
else:
    path = '/srv/slaveaccount/bin/'

logging.config.fileConfig(os.path.join(path, 'logging.ini'))


def main():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(path, 'config.ini'))
    userIDs = config.get('CTP', 'userIDs').split(',')

    client = MongoClient(
        config.get('mongodb', 'host'),
        config.getint('mongodb', 'port'),
    )

    gateWays = []
    for userID in userIDs:
        ctpGateway = CtpGateway(config, 'CTP', userID, client)
        gateWays.append(ctpGateway)
        ctpGateway.run()

    stoped = Event()

    def shutdownFunction(signalnum, frame):
        logging.info(u'系统即将关闭')
        for g in gateWays:
            g.close()

        if not stoped.isSet():
            stoped.set()

    for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
        signal.signal(sig, shutdownFunction)

    while not stoped.wait(1):
        pass

    logging.info(u'系统完全关闭')


if __name__ == '__main__':
    try:
        main()
    except:
        logging.error(traceback.format_exc())
