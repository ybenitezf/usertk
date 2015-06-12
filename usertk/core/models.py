# -*- coding: utf-8 -*-
import datetime
from pydal import DAL, Field
from core import config

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class BaseModel(object):

    def __init__(self):
        self.db = config.DATABASE

    def define_table(self):
        """
        Subclasses must implement this and define the database table
        """
        raise NotImplementedError()


class Parserstatus(BaseModel):
    """Holds the status of the parser"""

    def define_table(self):
        db = self.db
        if not hasattr(db, 'parser_status'):
            db.define_table('parser_status',
                Field('lastdate','datetime',default=datetime.datetime.now),
                Field('offset', 'integer', default=0)
            )
            db.commit()

    def get(self, id):
        return self.db.parser_status[id]

    def update(self, **kwargs):
        offset = kwargs['offset']
        id = kwargs['id']
        lastdate = datetime.datetime.now()
        self.db(self.db.paser_status.id == id).update(offset=offset,lastdate=lastdate)
        self.db.commit()

    def insert(self, **kwargs):
        id = self.db.paser_status.insert(kwargs)
        self.db.commit()
        return self.get(id)

    @staticmethod
    def rotate():
        # reset parser status on the database
        ps = Parserstatus()
        status = ps.get(config.SITE_ID)
        if not status:
            ps.insert(offset=0)
            config.LOGGER.debug("Usertk was expecting Parserstatus instance")
            return False
        ps.update(id=status.id, offset=0)
        return True

