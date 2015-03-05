# -*- coding: utf-8 -*-
""" The ida of this simple plugin framework was take from:

http://martyalchin.com/2008/jan/10/simple-plugin-framework/
"""
from core import config
from core.models import Parserstatus
from libs import excludes, squid

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'

class PluginMount(type):
    """Metaclass or class template, this is a minimal plugin framework"""

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [p(*args,**kwargs) for p in cls.plugins]


class LogProcessPlugin(object):

    __metaclass__ = PluginMount

    def __init__(self):
        self.ex = excludes.Excludes(config.EXCLUDES)
        self.actions = ['TCP_MISS', 'TCP_REFRESH_MISS',
                        'TCP_CLIENT_REFRESH', 'TCP_CLIENT_REFRESH_MISS',
                        ]

    def is_exclude(self, entry):
        # check if entry is on excludes
        if self.ex.is_exclude(entry.uri) or entry.action not in self.actions:
            return True

        return False

    def process_entry(self, entry):
        """Process a log entry.
        Each pluggin has to implement this and make something with entry
        """
        pass


class ParserStatusUpdater(LogProcessPlugin):
    """Default plugin in charge of update parser status"""

    def process_entry(self, entry):
        assert isinstance(entry, squid.LogEntry)
        status = Parserstatus.get(Parserstatus.id == config.SITE_ID)
        status.offset = entry.offset
        status.lastdate = entry.timeStamp
        status.save()
        config.LOGGER.debug('Updaing parser status OS: %d', status.offset)
