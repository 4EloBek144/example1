import sqlite3
from groups import Group
from init import *
from error import Error, errors


def find_name(s, name): # Поиск пользователей и расписаний по имени/названию
    try:
        for i in s:
            if i.name.lower() == name.lower():
                return i
        return errors[0]
    except Exception:
        print(f'Объект не имеет параметра имени', end=' - ')
        return errors[0]


def find_id(s, uid): # Поиск пользователей и расписаний по id
    try:
        for i in s:
            if i.id == uid:
                return i
        return errors[0]
    except Exception:
        print(f'Объект не имеет параметра id', end=' - ')
        return errors[0]


def st_r():
    print('Информацию о каком из студентов вы бы хотели просмотреть? Возможные варианты:')
    for u in users:
        if u.role == 'st':
            print(u.name)
    user = input()
    if user in user_names and find_name(users, user).role == 'st':
        print(f'Имя - {find_name(users, user).name}')
        g = find_name(users, user).find_groups()
        if g != -1:
            print(f'Посещаемость - {find_name(users, user).att}')
            print(f'Обучается в группе с номером {g}')
        else:
            print('Не состоит в группе')
    else:
        print('Пользователь не найден')


def group_r():
    print('Введите номер группы')
    gr_id = int(input())
    gr = find_id(groups, gr_id)
    if gr_id == -1 or gr.id != gr_id:
        print('Группа не найдена')
    else:
        print(f'Номер группы - {gr.id}')
        print(f'Состав группы - {gr.comp}')
        print(f'Расписание группы - {gr.tt.name}')


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

    if curr_user != '' and find_name(users, curr_user).role == 'st':
        print(f'Ваш аккаунт - студенческий аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр посещаемости, просмотр состава группы, просмотр ответственного преподавателя, просмотр расписания, выход из аккаунта ')
        match action.lower():
            case 'просмотр посещаемости':
                if find_name(users, curr_user).find_groups() != -1:
                    sub = input('Введите название предмета: ')
                    print(find_name(users, curr_user).get_att(sub))
                else:
                    print('Вы не состоите в группе')
            case 'просмотр состава группы':
                if find_name(users, curr_user).find_groups() != -1:
                    print(f'Ваша группа: {find_id(groups, find_name(users, curr_user).find_groups()).comp}')
                else:
                    print('Вы не состоите в группе')
            case 'просмотр ответственного преподавателя':
                if find_name(users, curr_user).find_groups() != -1:
                    print(f'Ответственный за вашу группу преподаватель - {find_id(groups, find_name(users, curr_user).find_groups()).teacher.name}')
                else:
                    print('Вы не состоите в группе')
            case 'просмотр расписания':
                if find_name(users, curr_user).find_groups() != -1:
                    o = input('чет или нечет неделя? ')
                    if o.lower() == 'чет':
                        print(find_id(ttables, find_name(users, curr_user).find_groups()).get(2))
                    elif o.lower() == 'нечет':
                        print(find_id(ttables, find_name(users, curr_user).find_groups()).get(1))
                    else:
                        print('Команда не распознана')
                else:
                    print('Вы не состоите в группе')
            case 'выход из аккаунта':
                open('../resourses/akk.txt', 'w').write('')
                curr_user = ''

    elif curr_user != '' and find_name(users, curr_user).role == 'te':
        print(f'Ваш аккаунт - преподавательский аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр информации о студентах, просмотр групп, изменение посещаемости студентов, выход из аккаунта ')
        match action.lower():
            case 'просмотр информации о студентах':
                st_r()
            case 'просмотр групп':
                group_r()
            case 'изменение посещаемости студентов':
                st = input('Введите имя студента: ')
                subj = input('Введите название предмета, на котором хотите отметить присутствие студента: ')
                if st in user_names and find_name(users, st).find_groups() != -1:
                    find_name(users, st).write_att(subj)
                else:
                    print('Студент не найден или не обучается в группе')
            case 'выход из аккаунта':
                open('../resourses/akk.txt', 'w').write('')
                curr_user = ''

    elif curr_user != '' and find_name(users, curr_user).role == 'adm':
        print(f'Ваш аккаунт - администраторский аккаунт {curr_user}')
        action = input('Возможные действия: Просмотр информации о студентах, просмотр/редактирование/создание групп, редактирование/создание расписаний, назначение преподавателей, создание профилей, выход из аккаунта ')
        match action.lower():
            case 'просмотр информации о студентах':
                st_r()
            case 'просмотр групп':
                group_r()
            case 'редактирование групп':
                print('Введите номер группы')
                gr_id = int(input())
                gr = find_id(groups, gr_id)
                if gr_id == -1 or gr.id != gr_id:
                    print('Группа не найдена')
                else:
                    print('Что бы вы хотели отредактировать?')
                    act2 = input('Возможные варианты: состав, расписание ')
                    match act2.lower():
                        case 'состав':
                            if gr.comp is not None:
                                print(f'Текущий состав: {gr.comp.split(", ")}')
                            else:
                                print('Группа пуста')
                            act3 = input('Добавить или исключить человека? ')
                            match act3.lower():
                                case 'добавить':
                                    no_gr = [x.name for x in users if x.find_groups() == -1 and x.role == 'st']
                                    if no_gr == []:
                                        print('Все студенты уже состоят в группах')
                                    else:
                                        user = input(f'Кого добавить? Варианты: {', '.join(no_gr)} ')
                                        if user in user_names and find_name(users, user).role == 'st' and find_name(users, user).find_groups() == -1:
                                            user = find_name(users, user)
                                            if gr.comp is not None and ', ' in gr.comp:
                                                res = gr.comp.split(", ")
                                                res.append(user.name)
                                                gr.write('comp', ', '.join(res))
                                            elif gr.comp is None:
                                                gr.write('comp', user.name)
                                            else:
                                                res = [gr.comp, user.name]
                                                gr.write('comp', ', '.join(res))
                                            print('Пользователь добавлен')
                                            user.tt_create(gr_id)
                                        else:
                                            print('Пользователь не найден')
                                case 'исключить':
                                    user = input(f'Кого исключить? Варианты: {gr.comp.split(", ")}')
                                    if user in gr.comp.split(", "):
                                        res = gr.comp.split(", ").pop([gr.comp.split(", ").find(user)])
                                        gr.write('comp', ', '.join(res))
                                        print('Пользователь исключен')
                                    else:
                                        print('Пользователь не найден')
                        case 'расписание':
                            print('Введите название расписания, возможные варианты: ')
                            for t in ttables:
                                print(t.name)
                            table_n = input()
                            table = find_name(ttables, table_n)
                            if table.id == -1:
                                print('Расписание не найдено')
                            else:
                                gr.write('timetable', table.id)
                                print('Расписание выставлено')
            case 'создание групп':
                print('Введите название расписания, по которому будет обучаться группа')
                print('Варианты расписаний: ')
                for i in ttables:
                    print(i.name)
                tt = input()
                while find_name(ttables, tt).id == -1:
                    tt = input('Расписание не найдено, повторите ввод: ')
                print('Введите имя отвечающего за группу преподавателя')
                print('Возможные преподаватели: ')
                for i in users:
                    if i.role == 'te':
                        print(i.name)
                te = input()
                while find_name(users, te).id == -1:
                    te = input('Преподаватель не найден, повторите ввод: ')
                cursor.execute(f"INSERT INTO groups (timetable, teacher) VALUES ('{find_name(ttables, tt).id}', '{find_name(users, te).id}');")
                conn.commit()
                groups.append(Group(len(groups) + 1, None, find_name(ttables, tt).id, find_name(users, te).id))
                print('Пустая группа создана')
            case 'редактирование расписаний':
                print('Введите название расписания, возможные варианты: ')
                for t in ttables:
                    print(t.name)
                tt = input()
                tt = find_name(ttables, tt)
                if tt.id == -1:
                    print('Расписание не найдено')
                else:
                    print(f'Текущее расписание на нечет неделю: {tt.get(1)}')
                    print(f'Текущее расписание на чет неделю: {tt.get(2)}')
                    d = input('Какой день недели вы бы хотели отредактировать: ')
                    w = input('Чет или  нечет недели?: ')
                    if d in 'понедельник вторник среда четверг пятница суббота'.split() and w in 'чет нечет'.split():
                        ds = {'понедельник': 'mon', 'вторник': 'tue', 'среда': 'wed', 'четверг': 'thu', 'пятница': 'fri', 'суббота': 'sat',}
                        ws = {'чет': '2', 'нечет': '1'}
                        print('Введите 5 занятий, отсутствующее занятие отмечается как -')
                        print('Возможные виды занятий: гит, математика, информатика, программирование, английский, русский, дискретная математика, орг, история, физика')
                        ans = []
                        f = 1
                        subjs = {'гит': 'ГИТ', 'математика': 'МАТ', 'информатика': 'ИНФ', 'программирование': 'ПРОГ',
                                 'английский': 'АНГЛ', 'русский': 'РУС', 'дискретная математика': 'ДМАТ', 'орг': 'ОРГ',
                                 'история': 'ИСТ', 'физика': 'ФИЗ', '-': '-'}
                        for s in range(5):
                            p = input(f'{s + 1} занятие: ')
                            if p in 'гит, математика, информатика, программирование, английский, русский, дискретная математика, орг, история, физика, -'.split(', '):
                                ans.append(subjs[p])
                            else:
                                print('Предмет не найден')
                                f = 0
                        if f:
                            tt.write(ds[d] + ws[w], '|'.join(ans))
                            print('Расписание отредактировано')
                            for u in [x for x in users if x.role == 'st' and x.find_groups() != -1 and find_id(groups, x.find_groups()).tt == tt]:
                                u.tt_create(ex=1)
                        else:
                            print('Ошибка в ходе редактирования')
            case 'создание расписаний':
                name = input('Введите название расписания: ')
                while find_name(ttables, name).id != -1:
                    name = input('Расписание с таким именем уже существует, повторите ввод: ')
                dig_ru = {1: 'понедельник', 2: 'вторник', 3: 'среду', 4: 'четверг', 5: 'пятницу', 6: 'субботу'}
                dig_en = {1: 'mon', 2: 'tue', 3: 'wed', 4: 'thu', 5: 'fri', 6: 'sat'}
                subjs = {'гит': 'ГИТ', 'математика': 'МАТ', 'информатика': 'ИНФ', 'программирование': 'ПРОГ',
                         'английский': 'АНГЛ', 'русский': 'РУС', 'дискретная математика': 'ДМАТ', 'орг': 'ОРГ',
                         'история': 'ИСТ', 'физика': 'ФИЗ'}
                res = []
                for i in range(12):
                    if i == 0:
                        print('Нечетная неделя: ')
                    elif i == 6:
                        print('Четная неделя: ')
                    print(f'Введите занятия на {dig_ru[(i % 6) + 1]}: ')
                    s = []
                    for p in range(5):
                        inp = input(str(p + 1) + ' занятие: ')
                        while inp not in 'гит, математика, информатика, программирование, английский, русский, дискретная математика, орг, история, физика, -'.split(', '):
                            print('Неверный ввод')
                            inp = input(str(p + 1) + ' занятие: ')
                        s.append(subjs[inp])
                    res.append('|'.join(s))
                cursor.execute(f"INSERT INTO timetable (name, mon1, tue1, wed1, thu1, fri1, sat1, mon2, tue2, wed2, thu2, fri2, sat2) VALUES ('{name}', '{res[0]}', '{res[1]}', '{res[2]}', '{res[3]}', '{res[4]}', '{res[5]}', '{res[6]}', '{res[7]}', '{res[8]}', '{res[9]}', '{res[10]}', '{res[11]}');")
                conn.commit()
                ttables.append(TimeTable(len(ttables) + 1, res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11], name))
            case 'назначение преподавателей':
                print('Введите номер группы для которой хотели бы назначить преподавателя')
                gr_id = int(input())
                gr = find_id(groups, gr_id)
                if gr_id == -1 or gr.id != gr_id:
                    print('Группа не найдена')
                else:
                    print('Введите имя преподавателя')
                    print('Возможные варианты преподавателей: ')
                    for u in users:
                        if u.role == 'te':
                            print(u.name)
                    te_n = input()
                    if te_n in user_names and find_name(users, te_n).role == 'te':
                        gr.write('teacher', find_name(users, te_n).id)
                        print('Преподаватель назначен')
                    else:
                        print('Пользователь не найден')
            case 'создание профилей':
                rl = input('Введите роль пользователя (студент, преподаватель): ')
                rls = {'студент': 'st', 'преподаватель': 'te'}
                nm = input('Введите имя: ')
                if nm not in user_names:
                    cursor.execute(f"INSERT INTO users (name, role) VALUES ('{nm}', '{rls[rl]}');")
                    conn.commit()
                    users.append(User(len(users) + 1, nm, None, rls[rl]))
                    user_names.append(nm)
                    print('Аккаунт создан')
            case 'выход из аккаунта':
                open('../resourses/akk.txt', 'w').write('')
                curr_user = ''
