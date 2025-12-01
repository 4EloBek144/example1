import sqlite3


class User: # Класс пользователей
    def __init__(self, uid, name, att, role):
        self.id = uid
        self.name = name
        self.att = att
        self.role = role
        self.rtt = None
        if self.role == 'st' and self.find_groups() != -1:
            con = sqlite3.connect('../resources/db')
            cur = con.cursor()
            self.gr = cur.execute(f"SELECT * FROM groups WHERE id = {self.find_groups()}").fetchall()
            self.tt_init()
            con.close()

    def tt_init(self, group = None):
        con = sqlite3.connect('../resources/db')
        cur = con.cursor()
        if self.rtt is None and group is not None:
            self.gr = cur.execute(f"SELECT * FROM groups WHERE id = {group}").fetchall()
            self.rtt = cur.execute(f"SELECT * FROM timetable WHERE id = {self.gr[0][2]}").fetchall()
        else:
            self.rtt = cur.execute(f"SELECT * FROM timetable WHERE id = {self.gr[0][2]}").fetchall()
        con.close()
        w1 = [self.rtt[0][1], self.rtt[0][2], self.rtt[0][3], self.rtt[0][4], self.rtt[0][5], self.rtt[0][6]]
        w2 = [self.rtt[0][7], self.rtt[0][8], self.rtt[0][9], self.rtt[0][10], self.rtt[0][11], self.rtt[0][12]]
        w  = [w1, w2]
        self.subj = []
        subj_vol = {}
        for i in w:
            for j in i:
                for sj in j.split('|'):
                    if sj != '-':
                        if sj not in self.subj:
                            self.subj.append(sj)
                        if sj not in subj_vol:
                            subj_vol[sj] = 1 * 8
                        else:
                            subj_vol[sj] += 1 * 8
        return subj_vol

    def tt_create(self, group = None, ex = None):
        vol = self.tt_init(group)
        con = sqlite3.connect('../resources/db')
        cur = con.cursor()
        if ex is None:
            att = ' '.join([f'{x}-0-{vol[x]}' for x in self.subj])
        else:
            try:
                att = ' '.join([f'{x}-{' '.join(self.att.split('-')).split()[' '.join(self.att.split('-')).split().index(x) + 1]}-{vol[x]}' for x in self.subj])
            except Exception:
                att = ' '.join([f'{x}-0-{vol[x]}' for x in self.subj])
                print(f'Не удалось перенести посещаемость студента {self.name} из-за различая учебных программ')
        cur.execute(f"UPDATE users SET att = '{att}' WHERE id = {self.id}")
        con.commit()
        con.close()

    def write(self, part, inf):
        con = sqlite3.connect('../resources/db')
        cur = con.cursor()
        match part:
            case 'name':
                cur.execute(f"UPDATE users SET name = '{inf}' WHERE id = {self.id}")
            case 'role':
                cur.execute(f"UPDATE users SET role = '{inf}' WHERE id = {self.id}")
        con.commit()
        con.close()

    def find_groups(self):
        con = sqlite3.connect('../resources/db')
        cur = con.cursor()
        gr = cur.execute(f"SELECT * FROM groups").fetchall()
        if self.role == 'te':
            self.groups = []
            for i in gr:
                if i[3] == self.id:
                    self.groups.append(str(i[0]))
            con.close()
            return self.groups
        elif self.role == 'st':
            self.groups = -1
            for i in gr:
                if i[1] is not None and str(self.name) in i[1].split(', '):
                    self.groups = i[0]
            con.close()
            return self.groups
        return None

    def get_att(self, subject):
        subjs = {'гит': 'ГИТ', 'математика': 'МАТ', 'информатика': 'ИНФ', 'программирование': 'ПРОГ', 'английский': 'АНГЛ', 'русский': 'РУС', 'дискретная математика': 'ДМАТ', 'орг': 'ОРГ', 'история': 'ИСТ', 'физика': 'ФИЗ'}
        try:
            subjs[subject]
        except Exception:
            return 'Предмет не найден'
        else:
            return f'Вы посетили {self.att.split()[self.subj.index(subjs[subject])].split('-')[1]} занятий из {self.att.split()[self.subj.index(subjs[subject])].split('-')[2]} за этот семестр.'

    def write_att(self, subject):
        con = sqlite3.connect('../resources/db')
        cur = con.cursor()
        subjs = {'гит': 'ГИТ', 'математика': 'МАТ', 'информатика': 'ИНФ', 'программирование': 'ПРОГ', 'английский': 'АНГЛ', 'русский': 'РУС', 'дискретная математика': 'ДМАТ', 'орг': 'ОРГ', 'история': 'ИСТ', 'физика': 'ФИЗ'}
        try:
            subjs[subject]
        except Exception:
            print(f'Предмет не найден')
        else:
            if subjs[subject] not in self.subj:
                print(f'Данный студент не имеет предмета {subject} в своем расписании.')
            else:
                att = self.att.split()
                att[self.subj.index(subjs[subject])] = '-'.join([att[self.subj.index(subjs[subject])].split('-')[0], str(int(att[self.subj.index(subjs[subject])].split('-')[1]) + 1), str(self.tt_init()[subjs[subject]])])
                self.att = ' '.join(att)
                cur.execute(f"UPDATE users SET att = '{self.att}' WHERE id = {self.id}")
                con.commit()
