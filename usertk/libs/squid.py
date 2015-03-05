# -*- coding: utf-8 -*-
"""Squid data models and related utils"""
from datetime import datetime
from urlparse import urlsplit

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class SquidRequest(object):
    """A rewrite request form squid"""

    def __init__(self, line):
        line = line.strip('\n')
        fields = line.split()
        self.__url = fields[0]
        self.__clientIp = (fields[1].split("/"))[0]
        self.__userName = fields[2]
        self.__raw = fields[0]

    def get_url(self):
        return self.__url

    def get_client_ip(self):
        return self.__clientIp

    def get_user_name(self):
        return self.__userName

    def get_raw(self):
        return self.__raw

    url = property(get_url, None, None, "URL")
    clientIp = property(get_client_ip, None, None, "Client IP")
    userName = property(get_user_name, None, None, "Username")
    raw = property(get_raw, None, None, "Raw SQUID request")


class LogEntry(object):
    """access.log entry from squid proxy-cache"""

    def __init__(self, line, offset):
        self.raw = line
        self.offset = offset
        line = line.strip('\n')
        fields = line.split()
        self.timeStamp = datetime.fromtimestamp(float(fields[0]))
        self.timeElapsed = float(fields[1])
        self.clientIP = fields[2]
        action, code = fields[3].split('/')
        self.action = action
        self.code = code
        self.size = float(fields[4])
        self.method = fields[5]
        self.uri = fields[6]
        self.userId = fields[7]
        self.heriarchy = fields[8]
        self.contentType = fields[9]

    def getRemoteHost(self):
        """Extract remote server hostname"""
        # TODO: review and test this
        if self.method == 'CONNECT':
            # if the method is connect this field not have a valid
            # URI.
            return self.uri.split(':')[0]
        else:
            r = urlsplit(self.uri)
            # in some cases when it come as hostname:port
            # urlsplit fail, this solve it
            return r.netloc.split(':')[0]

    def __unicode__(self):
        return '{0:d} {1:s} {2:s}'.format(self.offset, self.getRemoteHost(), self.userId)

    def __str__(self):
        return self.__unicode__()

    remoteHost = property(getRemoteHost, None, None, 'Remote host name')
