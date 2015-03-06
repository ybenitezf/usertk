# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread
from peewee import DoesNotExist
from core import config
from core.models import Parserstatus
from libs.parser import Parser
from libs.plugs import LogProcessPlugin

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class LogProducer(Thread):

    def __init__(self, queue, parser):
        # init producer, need a parser instance and a Queue
        Thread.__init__(self)
        assert isinstance(queue, Queue)
        assert isinstance(parser, Parser)
        self.q = queue
        self.p = parser
        # load old parser status or initialize it
        try:
            st = Parserstatus.get(Parserstatus.id == config.SITE_ID)
        except DoesNotExist:
            st = Parserstatus.create(offset=0)
            config.LOGGER.warning("Initializing paser status record")
        self.p.seek(st.offset)

    def run(self):
        while True:
            # get a log entry and put in the queue
            try:
                self.q.put(self.p.nextEntry())
            except ValueError:
                self.q.put(None)
                break


class LogConsumer(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        assert isinstance(queue, Queue)
        self.q = queue
        # load plugins
        self.plugins = LogProcessPlugin.get_plugins()

    def run(self):
        while True:
            entry = self.q.get()
            if not entry:
                self.q.task_done()
                break
            for p in self.plugins:
                try:
                    p.process_entry(entry)
                except Exception, e:
                    config.LOGGER.error("Plugin %s raise exception: %s", p, e)
            self.q.task_done()
