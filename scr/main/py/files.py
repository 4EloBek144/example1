import json
import sqlite3
import csv
import xml.etree.ElementTree as ET
import yaml
import os


def get_users(fl_type):
    con = sqlite3.connect('../resources/db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    if fl_type == 'json':
        ret = {'id': {}}
        for user in cur.fetchall():
            ret['id'][user[0]] = {'name': user[1], 'attendance': user[2], 'role': user[3]}

    elif fl_type == 'csv':
        ret = [['id', 'name', 'attendance', 'role']]
        for user in cur.fetchall():
            ret.append([user[0], user[1], user[2], user[3]])

    elif fl_type == 'xml':
        r = ET.Element('users')
        s = []
        i = 0
        for user in cur.fetchall():
            s.append(ET.SubElement(r, 'user'))
            s[i].set('id', str(user[0]))
            s[i].set('name', str(user[1]))
            s[i].set('attendance', str(user[2]))
            s[i].set('role', user[3])
            i += 1
        ret = ET.ElementTree(r)

    elif fl_type == 'yaml':
        for user in cur.fetchall():
            ret = {user[0]: {'name': user[1], 'attendance': user[2], 'role': user[3]}}

    return ret


def get_timetables(fl_type):
    con = sqlite3.connect('../resources/db')
    cur = con.cursor()
    cur.execute("SELECT * FROM timetable")

    if fl_type == 'json':
        ret = {'id': {}}
        for table in cur.fetchall():
            w1 = [table[1], table[2], table[3], table[4], table[5], table[6]]
            w2 = [table[7], table[8], table[9], table[10], table[11], table[12]]
            ret['id'][table[0]] = {'name': table[-1], 'odd w': w1, 'even w': w2}

    elif fl_type == 'csv':
        ret = [['id', 'name', 'odd w', 'even w']]
        for table in cur.fetchall():
            w1 = [table[1], table[2], table[3], table[4], table[5], table[6]]
            w2 = [table[7], table[8], table[9], table[10], table[11], table[12]]
            ret.append([table[0], table[-1], w1, w2])

    elif fl_type == 'xml':
        r = ET.Element('tables')
        s = []
        i = 0
        for table in cur.fetchall():
            s.append(ET.SubElement(r, 'table'))
            w1 = [table[1], table[2], table[3], table[4], table[5], table[6]]
            w2 = [table[7], table[8], table[9], table[10], table[11], table[12]]
            s[i].set('id', str(table[0]))
            s[i].set('name', str(table[-1]))
            s[i].set('odd w', str(w1))
            s[i].set('even w', str(w2))
            i += 1
        ret = ET.ElementTree(r)

    elif fl_type == 'yaml':
        for table in cur.fetchall():
            w1 = [table[1], table[2], table[3], table[4], table[5], table[6]]
            w2 = [table[7], table[8], table[9], table[10], table[11], table[12]]
            ret = {table[0]: {'name': table[-1], 'odd w': w1, 'even w': w2}}

    return ret


def get_groups(fl_type):
    con = sqlite3.connect('../resources/db')
    curg = con.cursor()
    curu = con.cursor()
    curt = con.cursor()

    g = curg.execute("SELECT * FROM groups")
    if fl_type == 'json':
        ret = {'id': {}}
    elif fl_type == 'csv':
        ret = [['id', 'composition', 'timetable', 'teacher']]
    elif fl_type == 'xml':
        r = ET.Element('groups')
        s = []
        i = 0

    for group in g.fetchall():
        u = curu.execute(f'SELECT * FROM users where id = {group[3]}').fetchall()[0]
        te = {'id': u[0], 'name': u[1], 'attendance': u[2]}

        t = curt.execute(f'SELECT * FROM timetable where id = {group[2]}').fetchall()[0]
        w1 = [t[1], t[2], t[3], t[4], t[5], t[6]]
        w2 = [t[7], t[8], t[9], t[10], t[11], t[12]]

        if fl_type == 'json':
            ret['id'][group[0]] = {'composition': group[1], 'timetable': {'id': t[0], 'name': t[-1], 'odd w': w1, 'even w': w2}, 'teacher': te}
        elif fl_type == 'csv':
            ret.append([group[0], group[1], {'id': t[0], 'name': t[-1], 'odd w': w1, 'even w': w2}, te])
        elif fl_type == 'xml':
            s.append(ET.SubElement(r, 'group'))
            s[i].set('id', str(group[0]))
            s[i].set('name', str(group[-1]))
            s[i].set('timetable', {'id': t[0], 'name': t[-1], 'odd w': w1, 'even w': w2})
            s[i].set('teacher', te)
            i += 1
            ret = ET.ElementTree(r)
        elif fl_type == 'yaml':
            ret = {group[0]: {'name': group[-1], 'timetable': {'id': t[0], 'name': t[-1], 'odd w': w1, 'even w': w2}, 'teacher': te}}

    return ret


def files(tab):
    try:
        os.mkdir('../../../out')
    except FileExistsError:
        pass
    if tab not in ['пользователи', 'расписания', 'группы']:
        print('Неверный ввод')
        return
    match tab:
        case 'пользователи':
            with open('../../../out/users.json', 'w', encoding='UTF-8') as f:
                json.dump(get_users('json'), f)
            with open('../../../out/users.csv', 'w', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerows(get_users('csv'))
            get_users('xml').write('../../../out/users.xml', encoding='UTF-8')
            with open('../../../out/users.yaml', 'w', encoding='UTF-8') as f:
                yaml.dump(get_users('yaml'), f)

        case 'группы':
            with open('../../../out/groups.json', 'w', encoding='UTF-8') as f:
                json.dump(get_groups('json'), f)
            with open('../../../out/groups.csv', 'w', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerows(get_groups('csv'))
            get_groups('xml').write('../../../out/groups.xml', encoding='UTF-8')
            with open('../../../out/groups.yaml', 'w', encoding='UTF-8') as f:
                yaml.dump(get_groups('yaml'), f)

        case 'расписания':
            with open('../../../out/timetables.json', 'w', encoding='UTF-8') as f:
                json.dump(get_timetables('json'), f)
            with open('../../../out/timetables.csv', 'w', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerows(get_timetables('csv'))
            get_timetables('xml').write('../../../out/timetables.xml', encoding='UTF-8')
            with open('../../../out/timetables.yaml', 'w', encoding='UTF-8') as f:
                yaml.dump(get_timetables('yaml'), f)
