# coding:utf-8
import logging
import os
from pymongo import MongoClient
import logging.config
from slaveaccount.calnav import Calnav
import ConfigParser

if __debug__:
    path = './tmp'
else:
    path = '/srv/slaveaccount/bin'

logging.config.fileConfig(os.path.join(path, 'logging.ini'))

def main():
    config = ConfigParser.ConfigParser()
    read_ok = config.read(os.path.join(path, 'config.ini'))

    client = MongoClient(
        config.get('mongodb', 'host'),
        config.getint('mongodb', 'port'),
    )

    c = Calnav(config, client)
    c.run()


if __name__ == '__main__':
    main()
