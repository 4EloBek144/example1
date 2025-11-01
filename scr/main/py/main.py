import sqlite3
from PyQt5 import *
from groups import Group
from init import *


groups = []
cursor.execute("SELECT * FROM groups")
for i in cursor.fetchall():
    groups.append(Group(i[0], i[1], i[2], i[3]))
print(groups)
for i in groups[0].tt.get(1):
    print(str(i).replace('-', '\t'))

users[0].write('name', 'Биткин Арсений')
groups[0].write('comp', 'Биткин Арсений, Какие-то балбесы')
ttables[0].write('name', 'Расписание 25-ИВТ-4-1')

users[1].find_groups()
ttables[0].find_groups()
conn.close()
