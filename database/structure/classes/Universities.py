#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Logger
from database.structure import Base
logger = Logger()


class Universities(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Університет'

    def __unicode__(self):
        return self.short_name

    faculties = relationship(
        'Faculties', backref='university', cascade='all, delete-orphan'
    )

    _columns = ['id', 'full_name', 'short_name']
    _links = ['faculties']
