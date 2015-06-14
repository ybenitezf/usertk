# -*- coding: utf-8 -*-
import datetime
from pydal import DAL, Field
from usertk.core import config

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class BaseModel(object):

    def __init__(self):
        self.db = config.DATABASE
        self.define_table()

    def define_table(self):
        """
        Subclasses must implement this and define the database table
        """
        raise NotImplementedError()


class Parserstatus(BaseModel):
    """Holds the status of the parser"""

    def define_table(self):
        if not hasattr(self.db, 'parser_status'):
            self.db.define_table('parser_status',
                Field('lastdate','datetime',default=datetime.datetime.now),
                Field('offset', 'integer', default=0)
            )
            self.db.commit()

    def get(self, id):
        return self.db.parser_status[id]

    def update(self, **kwargs):
        offset = kwargs['offset']
        id = kwargs['id']
        lastdate = datetime.datetime.now()
        self.db(self.db.parser_status.id == id).update(offset=offset,lastdate=lastdate)
        self.db.commit()

    def insert(self, **kwargs):
        offset = kwargs['offset']
        id = self.db.parser_status.insert(offset=offset)
        self.db.commit()
        return self.get(id)

    def rotate(self):
        # reset parser status on the database
        status = self.get(config.SITE_ID)
        if not status:
            self.insert(offset=0)
            config.LOGGER.warning("This should't happen")
            return False
        config.LOGGER.debug("Resseting parser status")
        self.update(id=status.id, offset=0)
        return True

