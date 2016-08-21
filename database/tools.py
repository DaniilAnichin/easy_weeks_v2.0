#!/usr/bin/python
# -*- coding: utf-8 -*- #
from database import db_codes, Logger
from database.structure.db_structure import *
logger = Logger()


def swap_local(first, second):
    first_time = first.time()
    second_time = second.time()
    logger.info('Local lessons swap started')
    logger.debug('First time: %d' % first.row_time)
    logger.debug('Second time: %d' % second.row_time)

    first.set_time(second_time)
    second.set_time(first_time)


def swap_lessons(session, first, second):
    # Perform difficult checks
    first_time = first.time()
    second_time = second.time()
    logger.info('Swap started')
    logger.debug('Id\'s: %d, %d' % (first.id, second.id))
    logger.debug('First time: %d' % first.raw_time)
    logger.debug('Second time: %d' % second.raw_time)

    res = Lessons.update(session, first.id, **Lessons.bad_time())
    res += Lessons.update(session, second.id, **first_time)
    res += Lessons.update(session, first.id, **second_time)

    if res:
        logger.error('Something went wrong in swap')
        return 1    # something went wrong
    logger.info('Successful swap')

    return 0


def check_temp_lessons(session, table):
    for day in table:
        for lesson in day:
            pass
    pass


def upload_temp_lessons(session, table):
    check_temp_lessons(session, table)
    pass