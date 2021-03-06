# -*- coding: utf-8 -*-
""" The ida of this simple plugin framework was take from:

http://martyalchin.com/2008/jan/10/simple-plugin-framework/
"""
from usertk.core import config
from usertk.core.models import Parserstatus
from usertk.libs import excludes, squid

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
        ps = Parserstatus()
        status = ps.get(config.SITE_ID)
        ps.update(id=status.id, offset=entry.offset, lastdate=entry.timeStamp)
        config.LOGGER.debug('Updaing parser status OS: %d', entry.offset)
