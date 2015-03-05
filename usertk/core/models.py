# -*- coding: utf-8 -*-
import datetime
from peewee import Model, DateTimeField, BigIntegerField, DoesNotExist, IntegerField
from core import config

__author__ = 'Yoel Benítez Fonseca <ybenitezf@gmail.com>'


class BaseModel(Model):
    class Meta:
        database = config.DATABASE


class Parserstatus(BaseModel):
    """Holds the status of the parser"""
    id = IntegerField(primary_key=True, default=config.SITE_ID)
    lastdate = DateTimeField(default=datetime.datetime.now)
    offset = BigIntegerField()

    @staticmethod
    def rotate():
        # reset parser status on the database
        try:
            ps = Parserstatus.get(Parserstatus.id == config.SITE_ID)
        except DoesNotExist, e:
            # this can't happen
            config.LOGGER.debug("Usertk was expecting Parserstatus instance but this happen: %s", e)
            return False
        ps.offset = 0
        ps.save()
        return True

config.LOGGER.debug("Checking main database models")
# TODO: when pluggin are loaded we need to create their tables to
config.DATABASE.create_tables([Parserstatus], safe=True)
