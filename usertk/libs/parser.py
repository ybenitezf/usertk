# -*- coding: utf-8 -*-
import time
from core import config
from libs.squid import LogEntry

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


l = config.LOGGER


class Parser(object):
    """Parser for squid access.log file, standard squid log format"""
    lfn = None

    def __init__(self, log_file_name):
        self.lfn = open(log_file_name, 'r')
        l.info('Parser started with %s log file', log_file_name)

    def __unicode__(self):
        return u'Parser for: {0:s}'.format(self.lfn.name, )

    def seek(self, offset):
        """Jump to the given offset in the log file."""
        # require valid open file
        if self.lfn:
            self.lfn.seek(offset)
            l.warning('Parser seek to %d', offset)
        else:
            l.warning('Parser was asked to seek to %d, but log file is closed.', offset)

        return self.lfn.tell() == offset

    def nextEntry(self):
        """Give the next log entry or wait until one being read"""
        offset, line = self.__get_line()
        try:
            entry = LogEntry(line, offset)
        except Exception, e:
            l.debug("Can't parse: %s error: %s", line, e)
            return None

        return entry

    def __get_line(self):
        while True:
            line = self.lfn.readline()
            offset = self.lfn.tell()
            # if get EOF wait until new lines come
            if not line:
                l.debug('Waiting for more log entrys...sleep 10s')
                time.sleep(10)
            else:
                break
        return offset, line
