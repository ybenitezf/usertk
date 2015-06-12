# -*- coding: utf-8 -*-
import logging
from pydal import DAL

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


# This value is for the case in that there are more instances of usertk
# running on others servers and they use the same database. In that case put
# diferent values for SITE_ID in each server.
SITE_ID = 1
#
LOG = "/var/log/usertk/usertk.log"
#
SQUID_ACCESS_LOG = "/var/log/squid/access.log"
#
PID = "/tmp/usertk.pid"

# list of sites excludes from processing
EXCLUDES = '/etc/usertk/excludes.txt'

# List of active plugins
# for example: PLUGS = ['myplug1', 'myplus.mplug2']
PLUGS = []

# uncomment one of this and edit the apropiate values

# DONT USE THIS
DATABASE = DAL('sqlite://storage.db')

# see http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Connection-strings--the-uri-parameter-
# for a complete list of supported databases
# for postgres (Recommended) install psycopg2
# DATABASE = DAL('postgres://username:password@localhost/test')
# for MySQL install MySQLdb or pymysql
# DATABASE = DAL('mysql://username:password@localhost/test')

# don't change this if you don't know what are u doing
LOGGER = logging.getLogger('usertk')
__ch = logging.FileHandler(LOG)
LOGGER.setLevel(logging.WARNING)
__ch.setLevel(logging.WARNING)
__formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s',
   '%m/%d/%Y %I:%M:%S %p')
__ch.setFormatter(__formatter)
LOGGER.addHandler(__ch)
