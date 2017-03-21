#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Logger, DATABASE_DIR, DATABASE_NAME
from database.start_db.seeds import *
from database.structure import Base
logger = Logger()


def create_new_database(path=DATABASE_NAME):
    # Temporary deleting:
    full_path = os.path.join(DATABASE_DIR, path)
    try:
        os.remove(full_path)
    except OSError:
        pass
    if os.path.isfile(full_path):
        logger.debug("Database with same name already exits")
        return -1
    en = create_engine('sqlite:///%s' % full_path)
    Base.metadata.create_all(en)
    session_m = sessionmaker(bind=en)
    s = session_m()
    s.commit()
    return s


def create_database(delete_past=True, path=DATABASE_NAME):
    if delete_past:
        try:
            os.remove(os.path.join(DATABASE_DIR, path))
        except OSError:
            pass

    session = create_new_database()
    if not isinstance(session, int):
        session = create_empty(session)
        session = create_common(session)
        session = create_custom(session)

    return session


def connect_database(path=DATABASE_NAME, hard=False):
    full_path = os.path.join(DATABASE_DIR, path)
    if os.path.isfile(full_path):
        en = create_engine('sqlite:///%s' % full_path)
        Base.metadata.create_all(en)
        session_m = sessionmaker(bind=en)
        session = session_m()
    else:
        if hard:
            session = create_database()
        else:
            logger.debug("Database does not exits")
            session = -1

    return session
