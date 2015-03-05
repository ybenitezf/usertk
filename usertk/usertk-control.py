#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from core.system import UtkSystem

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


if __name__ == "__main__":
    optp = OptionParser()
    optp.add_option('--start', dest="start", default=False, action='store_true', help="Start usertk")
    optp.add_option('--stop', dest="stop", default=False, action='store_true', help="Stop usertk")

    (options, args) = optp.parse_args()
    us = UtkSystem()
    if options.start:
        us.start()
    elif options.stop:
        us.stop()
        exit(0)
