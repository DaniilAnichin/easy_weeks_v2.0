#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bcrypt
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Logger
from database.structure import Base
logger = Logger()


class Users(Base):
    nickname = Column(String, unique=True)
    hashed_password = Column(String)
    status = Column(String)   # Expected values are 'admin' and 'method'
    message = Column(String)   # Message when giving an methodist request
    translated = u'Користувач'

    @classmethod
    def create(cls, session, **kwargs):
        password = kwargs.pop('password', '').encode('utf-8')
        if not password:
            logger.error('No password passed')
            raise ValueError('No password passed')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        kwargs.update(hashed_password=hashed)
        return super(Users, cls).create(session, **kwargs)

    def __unicode__(self):
        return self.nickname

    def authenticate(self, password):
        logger.info('User %s auth passing' % self.nickname)
        encoded = password.encode('cp1251')
        result = bcrypt.hashpw(encoded, self.hashed_password.encode('cp1251'))
        return self.hashed_password.encode('cp1251') == result

    # To give methodist user separated rights we need to create merging table
    # between User and Department, but if we don't - user can edit any table.
    departments = relationship(
        'Departments', secondary='user_departments', backref='users'
    )

    _columns = ['id', 'nickname', 'hashed_password', 'message', 'status']
    _associations = ['departments']
