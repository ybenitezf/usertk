#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from core.system import utk_system

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'

if __name__ == "__main__":
    optp = OptionParser()
    optp.add_option('--start', dest="start", default=False, action='store_true', help="Start usertk")
    optp.add_option('--stop', dest="stop", default=False, action='store_true', help="Stop usertk")
    optp.add_option('--restart', dest="restart", default=False, action='store_true', help="Restart usertk")

    (options, args) = optp.parse_args()
    if options.start:
        utk_system.start()
    elif options.stop:
        utk_system.stop()
    elif options.restart:
        utk_system.restart()
