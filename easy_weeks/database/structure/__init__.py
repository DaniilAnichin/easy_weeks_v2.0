from .base import Base
from .degrees import Degrees
from .department_rooms import DepartmentRooms
from .departments import Departments
from .faculties import Faculties
from .group_plans import GroupPlans
from .groups import Groups
from .lesson_plans import LessonPlans
from .lesson_times import LessonTimes
from .lesson_types import LessonTypes
from .lessons import Lessons
from .rooms import Rooms
from .subjects import Subjects
from .teacher_plans import TeacherPlans
from .teachers import Teachers
from .universities import Universities
from .user_departments import UserDepartments
from .users import Users
from .week_days import WeekDays
from .weeks import Weeks


tables = [
    'Degrees', 'DepartmentRooms', 'Departments', 'Faculties', 'Groups',
    'GroupPlans', 'LessonPlans', 'TeacherPlans', 'LessonTimes',
    'LessonTypes', 'Lessons', 'Rooms', 'Subjects', 'Teachers', 'Universities',
    'WeekDays', 'Weeks', 'Users', 'UserDepartments'
]
__all__ = tables
