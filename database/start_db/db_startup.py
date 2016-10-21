#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Create_new_db.py
#
#  Copyright 2016 AntonBogovis <antonbogovis@lenovo-bogovis>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
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
        os.remove(os.path.join(DATABASE_DIR, path))

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
