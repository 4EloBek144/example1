import sqlite3
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


def find_id(s, uid): # Поиск пользователей и расписаний по id
    try:
        for i in s:
            if i.id == uid:
                return i
        print(f'В списке не найден {uid}')
        return errors[0]
    except Exception:
        print(f'Объект не имеет параметра id', end=' - ')
        return errors[0]


groups = []
cursor.execute("SELECT * FROM groups")
for i in cursor.fetchall():
    groups.append(Group(i[0], i[1], i[2], i[3]))
curr_user = open('../resourses/akk.txt', 'r').read()

while True:
    if curr_user == '':
        curr_user = input('Войдите в аккаунт: ')
        if curr_user in user_names:
            open('../resourses/akk.txt', 'w').write(curr_user)
        else:
            curr_user = ''
    if find_name(users, curr_user).role == 'st':
        print(f'Ваш аккаунт - студенческий аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр посещаемости, просмотр состава группы, просмотр ответственного преподавателя, просмотр расписания, выход из аккаунта ')
        match action.lower():
            case 'просмотр посещаемости':
                print(f'Ваша посещаемость: {find_name(users, curr_user).att}')
            case 'просмотр состава группы':
                pass
            case 'просмотр ответственного преподавателя':
                pass
            case 'просмотр расписания':
                o = input('чет или нечет неделя? ')
                if o.lower() == 'чет':
                    print(find_id(ttables, find_name(users, curr_user).find_groups()).get(2))
                elif o.lower() == 'нечет':
                    print(find_id(ttables, find_name(users, curr_user).find_groups()).get(1))
                else:
                    print('Команда не распознана')
                # print(find_id(ttables, find_name(users, curr_user).find_groups()).tt_cont(1))
            case 'выход из аккаунта':
                open('../resourses/akk.txt', 'w').write('')
                curr_user = ''
    elif find_name(users, curr_user).role == 'te':
        print(f'Ваш аккаунт - преподавательский аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр информации о студентах, просмотр групп, изменение посещаемости студентов, выход из аккаунта ')
        match action.lower():
            case 'просмотр информации о студентах':
                pass
            case 'просмотр групп':
                pass
            case 'изменение посещаемости студентов':
                st = input('Введите имя студента: ')
                subj = input('Введите название предмета, на котором хотите отметить присутствие студента: ')
                if st in user_names:
                    find_name(users, st).write_att(subj)
                else:
                    print('Студент не найден')
            case 'выход из аккаунта':
                open('../resourses/akk.txt', 'w').write('')
                curr_user = ''
    elif find_name(users, curr_user).role == 'adm':
        print(f'Ваш аккаунт - администраторский аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр информации о студентах, просмотр/редактирование групп, выставление/редактирование расписаний, назначение преподавателей, создание профилей, выход из аккаунта ')
        match action.lower():
            case 'просмотр информации о студентах':
                pass
            case 'просмотр групп':
                pass
            case 'редактирование групп':
                pass
            case 'выставление расписаний':
                tid = input('Введите номер группы, для которой хотите назначить расписание ')
                if find_id(groups, tid).name == 'Ошибка':
                    print('Группа не найдена')
                else:
                    group = find_id(groups, tid)
                    tname = input('Введите название расписания ')
                    if find_name(ttables, tname).name == 'Ошибка':
                        print('Расписание не найдено')
                    else:
                        group.write('timetable', find_name(ttables, tname))
            case 'редактирование расписаний':
                pass
            case 'назначение преподавателей':
                pass
            case 'создание профилей':
                pass
            case 'выход из аккаунта':
                open('../resourses/akk.txt', 'w').write('')
                curr_user = ''
