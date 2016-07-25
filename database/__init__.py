import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_NAME = 'FICT_timetable.db'

db_codes = {
    'success': 0,
    'params': 1,
    'session': 2,
    'university': 3,
    'faculty': 4,
    'department': 5,
    '': 6,
    'group': 7,
    'degree': 8,
    'teacher': 9,
    'room': 10,
    'subject': 11,
    'lesson': 12,
    'lesson_plan': 13,


}

db_codes_output = [
    'Success'
    'Some params missed',
    'No DB session',
    'Problem with university',
    'Problem with faculty',
    'Problem with department',
    0,
    'Problem with groups',
    'Problem with degrees',
    'Problem with teachers',
    'Problem with rooms',
    'Problem with lessons',
    'Problem with lesson plans',
    '',
    ''
]