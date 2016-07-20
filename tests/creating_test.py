#!/usr/bin/python
# -*- coding: utf-8 -*- #
from db.Database_config.start_up.select_tools import *
from db.Database_config.New_db_startup import *


def main():
    # s = create_new_database('FICT_timetable.db')
    s = connect_database('FICT_timetable.db')
    deg = select_degees(s, id_d=1)
    print deg
    print deg[0]['teachers'][0].full_name


if __name__ == "__main__":
    main()
