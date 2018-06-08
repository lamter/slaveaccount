# coding:utf-8
import signal
import logging.config
from slaveaccount import CtpGateway
from pymongo import MongoClient

import ConfigParser

logging.config.fileConfig('/srv/slaveaccount/bin/logging.ini')
config = ConfigParser.ConfigParser()
read_ok = config.read('/srv/slaveaccount/bin/config.ini')
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

from threading import Event

stoped = Event()
count = 0


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
