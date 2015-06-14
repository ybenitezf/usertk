# -*- coding: utf-8 -*-
from Queue import Queue
import sys
from core import config
from core.process import LogProducer, LogConsumer
from libs.parser import Parser
from core.daemon import Daemon


__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class UtkSystem(Daemon):
    """
    Represent the complete usertk system
    """

    def __init__(self):
        super(UtkSystem, self).__init__(config.PID,config.LOGGER)

    def load_plugins(self):
        """Try to import all installed pluggins"""
        try:
            for p in config.PLUGS:
                # TODO: is this the way to do it?
                __import__(p)
        except Exception, e:
            config.LOGGER.debug("Error loading plugin: %s", p)
            config.LOGGER.debug("Error message: %s", e)
            sys.exit(1)

    def run(self):
        """Enter the running state"""
        l = config.LOGGER
        l.debug("loading pluggins")
        self.load_plugins()
        q = Queue(maxsize=5)
        parser = Parser(config.SQUID_ACCESS_LOG)
        p = LogProducer(q, parser)
        c = LogConsumer(q)
        #start all threads
        c.start()
        config.LOGGER.debug("Started consumer thread")
        p.start()
        config.LOGGER.debug("Started producer thread")
        # wait until all log entrys are processed
        config.LOGGER.debug("Processing started")
        q.join()
        sys.exit()

utk_system = UtkSystem()