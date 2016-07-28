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
    'reserved': 16
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
    16: 'This data may not be edited in any way'
}