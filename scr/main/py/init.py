import sqlite3
from PyQt5 import *
from users import User
from timetables import TimeTable


conn = sqlite3.connect('../resourses/db')
cursor = conn.cursor()

users = []
user_names = []
cursor.execute("SELECT * FROM users")
for i in cursor.fetchall():
    user_names.append(i[1])
    users.append(User(i[0], i[1], i[2], i[3]))

ttables = []
cursor.execute("SELECT * FROM timetable")
for i in cursor.fetchall():
    ttables.append(TimeTable(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13]))

# Это все для того, что бы в классе групп могли использоваться классы расписаний и пользователей...
