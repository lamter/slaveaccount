import logging.config
import os

import configparser
from pymongo import MongoClient

from slaveaccount.calnav import Calnav

if __debug__:
    path = './tmp'
else:
    path = '/srv/slaveaccount/bin'

logging.config.fileConfig(os.path.join(path, 'logging.ini'))

def main():
    config = configparser.ConfigParser()
    read_ok = config.read(os.path.join(path, 'config.ini'))

    client = MongoClient(
        config.get('mongodb', 'host'),
        config.getint('mongodb', 'port'),
    )

    c = Calnav(config, client)
    c.run()


if __name__ == '__main__':
    main()
