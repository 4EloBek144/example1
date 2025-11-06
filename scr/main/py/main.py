import sqlite3
from PyQt5 import *
from groups import Group
from init import *
from error import Error, errors


def find_name(s, name): # Поиск пользователей и расписаний по имени/названию
    try:
        for i in s:
            if i.name.lower() == name.lower():
                return i
        print(f'В списке не найден {name}')
        return errors[0]
    except Exception:
        print(f'Объект не имеет параметра имени', end=' - ')
        return errors[0]


groups = []
cursor.execute("SELECT * FROM groups")
for i in cursor.fetchall():
    groups.append(Group(i[0], i[1], i[2], i[3]))
for i in groups[0].tt.get(1): # Получение расписания группы
    print(str(i).replace('-', '\t'))

users[0].write('name', 'Биткин Арсений') # Изменение информации в базе данных
groups[0].write('comp', 'Биткин Арсений')
ttables[0].write('name', 'Расписание 25-ИВТ-4-1')

find_name([1], 'Биткин Арсений').find_groups() # Нахождение групп по имени преподавателя или студента
find_name(users, 'Какой-то препод').find_groups()
find_name(ttables, 'расписание 25-ивт-4-1').find_groups() # Нахождение групп по названию расписания
conn.close()
