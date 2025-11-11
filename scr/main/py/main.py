import sqlite3
from unittest import case

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
curr_user = open('../resourses/akk.txt', 'r').read()

while True:
    if curr_user == '':
        curr_user = input('Войдите в аккаунт: ')
        print(user_names)
        if curr_user in user_names:
            open('../resourses/akk.txt', 'w').write(curr_user)
        else:
            curr_user = ''
    if find_name(users, curr_user).role == 'st':
        print(f'Ваш аккаунт - студенческий аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр посещаемости, просмотр состава группы, просмотр ответственного преподавателя, просмотр расписания')
        match action.lower():
            case 'просмотр посещаемости':
                pass
            case 'просмотр состава группы':
                pass
            case 'просмотр ответственного преподавателя':
                pass
            case 'просмотр расписания':
                pass
    if find_name(users, curr_user).role == 'te':
        print(f'Ваш аккаунт - преподавательский аккаунт {curr_user}')
        action = input('Возможные действия: ')
