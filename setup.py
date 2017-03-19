from distutils.core import setup
from os.path import join as _
import py2exe

PATH = __file__
DATA = [('database', [_(PATH, 'database', 'FICT_timetable.db')]),
        ('', [_(PATH, 'easy_weeks.log'), _(PATH, 'README.md')]),
        (_('database', 'start_db'), [_(PATH, 'database', 'start_db', 'teachers.json'),
                                     _(PATH, 'database', 'start_db', 'groups.json'),
                                     _(PATH, 'database', 'start_db', 'departments.json'),
                                     _(PATH, 'database', 'start_db', 'departments_2.json'),
                                     _(PATH, 'database', 'start_db', 'departments_def.json'),
                                     _(PATH, 'database', 'start_db', 'teachers_all.json'),
                                     _(PATH, 'database', 'start_db', 'seeds.json')])]
setup(
    windows=['main_file.py'],
    data_files=DATA,
    options={
        'py2exe': {
            'packages': ['database', 'gui', 'sqlalchemy'],
            'includes': ['sip', 'cffi'],
            'excludes': ['email'],
            # 'bundle_files': 2,
            'skip_archive': 1
        }
    }
)
