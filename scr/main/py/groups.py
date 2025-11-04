from timetables import TimeTable
from users import User
from init import users, ttables
import sqlite3


class Group:
    def __init__(self, uid, comp, tt, teacher):
        self.id = uid
        self.comp = comp
        self.tt = ttables[tt - 1]
        self.teacher = users[teacher - 1]

    def write(self, part, inf):
        con = sqlite3.connect('C:/Users/Arseniy/PycharmProjects/sem1/scr/main/resourses/db')
        cur = con.cursor()
        match part:
            case 'comp':
                cur.execute(f"UPDATE groups SET composition = '{inf}' WHERE id = {self.id}")
            case 'timetable':
                cur.execute(f"UPDATE groups SET timetable = '{inf}' WHERE id = {self.id}")
            case 'teacher':
                cur.execute(f"UPDATE groups SET teacher = '{inf}' WHERE id = {self.id}")
        con.commit()
        con.close()

