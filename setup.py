from distutils.core import setup
import py2exe

DATA = [('database', ['D:\\KPI\\Kursach\\easy_weeks_v2.0\\database\\FICT_timetable.db']), ('', ['D:\\KPI\\Kursach\\easy_weeks_v2.0\\easy_weeks.log', 'D:\\KPI\\Kursach\\easy_weeks_v2.0\\README.md']), ('database\\start_db', ['D:\\KPI\\Kursach\\easy_weeks_v2.0\\database\\start_db\\teachers.txt', 'D:\\KPI\\Kursach\\easy_weeks_v2.0\\database\\start_db\\groups.txt'])] 
setup(
    windows=['main_file.py'],
    data_files = DATA,
    options = {
        'py2exe': {
            'packages': ['database', 'gui', 'sqlalchemy'],
            'includes': ['sip', 'cffi'],
            # 'bundle_files': 2,
            'skip_archive': 1
        }
    }
)
