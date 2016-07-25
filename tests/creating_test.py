#!/usr/bin/python
# -*- coding: utf-8 -*- #
from database import *
from database.start_db.New_db_startup import *
from database.structure.select_tools import *


def main():
    s = create_new_database('FICT_timetable.db')
    s = connect_database('FICT_timetable.db')
    deg = select_degrees(s, id_d=1)
    print deg
    print deg[0]['teachers'][0].full_name

    tea = select_teachers(s, id_t=8)
    print tea

    print BASE_DIR


if __name__ == "__main__":
    main()
