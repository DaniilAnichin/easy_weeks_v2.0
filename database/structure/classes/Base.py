#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from database import db_codes, Logger
logger = Logger()
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


@as_declarative()
class Base(object):
    _columns = ['id']
    _links = []
    _associations = []
    id = Column(Integer, primary_key=True)

    def __init__(self, *args, **kwargs):
        logger.info('DB model init call invokes')   # Never called..
        super(Base, self).__init__(*args, **kwargs)

    @declared_attr
    def __tablename__(self):
        s1 = first_cap_re.sub(r'\1_\2', self.__name__)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    @classmethod
    def single(cls):
        if cls.__tablename__ in ['faculties', 'universities']:
            return cls.__tablename__[:-2] + 'y'
        else:
            return cls.__tablename__[:-1]

    @classmethod
    def links(cls):
        # To return list of fields, which provide one-to-many relations
        return cls._links[:]

    @classmethod
    def associations(cls):
        # To return list of fields, which provide many-to-many relations
        return cls._associations[:]

    @classmethod
    def columns(cls):
        # To return list of fields, which are sql columns
        return cls._columns[:]

    @classmethod
    def fields(cls):
        # To return full list of class fields
        return cls.columns() + cls.associations() + cls.links()

    @classmethod
    def create(cls, session, **kwargs):
        # looks like it's working
        # Add fields and associations?
        if not set(kwargs.keys()) < set(cls.fields()):
            return db_codes['wrong']

        result = cls.read(session, **kwargs)

        if isinstance(result, int):
            return result
        elif result:
            return db_codes['exists']
        else:
            elem = cls(**kwargs)
            session.add(elem)

        return elem

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            # return result.all()
            return result.all()[1:]

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                example = cls.read(session, id=1)[0]
                if isinstance(getattr(example, key), list):
                    for item in kwargs[key]:
                        result = result.filter(getattr(cls, key).contains(item))
                else:
                    result = result.filter(getattr(cls, key).in_(kwargs[key]))
                # OK as parent select for lesson_plan and other will be modified
                # work proper for all 'easy' classes
            else:
                result = result.filter(getattr(cls, key) == kwargs[key])

        return result.all()

    @classmethod
    def update(cls, session, main_id, **kwargs):
        # looks like it's working
        # No deleting first data:
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)

        # Check for existence:
        if not result:
            return db_codes['absent']
        if isinstance(result, int):
            return result
        result = result[0]

        data = {}
        for field in cls.fields():
            data.update({field: getattr(result, field)})
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            data.update({key: kwargs[key]})
        doubles = cls.read(session, **data)
        if doubles and doubles[0].id != main_id:
            return db_codes['exists']

        # Global filter loop:
        for key in kwargs.keys():
            setattr(result, key, kwargs[key])

        session.commit()

        return db_codes['success']

    @classmethod
    def delete(cls, session, main_id):
        # looks like it's working
        # No deleting first data:
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)

        # Check for existence:
        if not result:
            return db_codes['absent']
        if isinstance(result, int):
            return result

        result = result[0]

        # Reset links:
        for link in cls.links():
            default_id = 1
            linked = getattr(result, link)
            if isinstance(linked, list):
                for element in linked:
                    setattr(element, 'id_' + cls.single(), default_id)
            # else:
            #     setattr(linked, 'id_' + cls.single(), 1)
        for association in cls.associations():
            linked = getattr(result, association)
            for element in linked:
                getattr(element, cls.__tablename__).remove(result)

        # Delete:
        session.delete(result)
        session.commit()
        return db_codes['success']
