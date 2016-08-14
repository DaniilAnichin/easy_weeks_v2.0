import os
import logging


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# BASE_DIR = os.path.dirname(os.path.dirname("/home/antonbogovis/Projects/ew-2_0/easy_weeks_v2.0"))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_NAME = 'FICT_timetable.db'


class Logger(logging.Logger):
    def __init__(self):
        super(Logger, self).__init__('root')
        if not self.level == logging.DEBUG:
            formatter = logging.Formatter(
    u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
            )

            filehandler = logging.FileHandler(
                os.path.join(BASE_DIR, u'easy_weeks.log')
            )
            filehandler.setFormatter(formatter)
            filehandler.setLevel(logging.INFO)
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(logging.DEBUG)
            self.addHandler(filehandler)
            self.addHandler(console)

db_codes = {
    'success': 0,
    'params': 1,
    'session': 2,
    'university': 3,
    'faculty': 4,
    'department': 5,
    'wrong': 6,
    'group': 7,
    'degree': 8,
    'teacher': 9,
    'room': 10,
    'subject': 11,
    'lesson': 12,
    'lesson_plan': 13,
    'exists': 14,
    'absent': 15,
    'reserved': 16,
    'user': 17,
    'temp_lesson': 18,
    'time': 19,
    '': 20,
}

db_codes_output = {
    0: 'Success',
    1: 'Some params missed',
    2: 'No DB session',
    3: 'Problem with university',
    4: 'Problem with faculty',
    5: 'Problem with department',
    6: 'Incorrect parameter',
    7: 'Problem with groups',
    8: 'Problem with degrees',
    9: 'Problem with teachers',
    10: 'Problem with rooms',
    11: 'Problems with subjects',
    12: 'Problem with lessons',
    13: 'Problem with lesson plans',
    14: 'This data already exists',
    15: 'Data with this id does not exist',
    16: 'This data may not be edited in any way',
    17: 'Problem with users',
    18: 'Problem with temporary_lessons',
    19: 'Impossible time'
}