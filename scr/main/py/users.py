import sqlite3


class User: # Класс пользователей
    def __init__(self, uid, name, att, role):
        self.id = uid
        self.name = name
        self.att = att
        self.role = role

    def write(self, part, inf):
        con = sqlite3.connect('../resourses/db')
        cur = con.cursor()
        match part:
            case 'name':
                cur.execute(f"UPDATE users SET name = '{inf}' WHERE id = {self.id}")
            case 'role':
                cur.execute(f"UPDATE users SET role = '{inf}' WHERE id = {self.id}")
        con.commit()
        con.close()

    def find_groups(self):
        con = sqlite3.connect('../resourses/db')
        cur = con.cursor()

        groups = []
        cur.execute("SELECT * FROM groups")
        for i in cur.fetchall():
            groups.append([i[0], i[1], i[2], i[3]])
        con.close()

        if self.role == 'te':
            self.groups = []
            for i in groups:
                if i[3] == self.id:
                    self.groups.append(str(i[0]))
            print(f'{self.name} отвечает за группы с номерами:', ' '.join(self.groups))
        elif self.role == 'st':
            self.groups = 0
            for i in groups:
                if str(self.name) in str(i[1]):
                    self.groups = i[0]
            if self.groups == 0:
                print(f'Студент {self.name} не состоит в группе')
            else:
                print(f'Студент {self.name} состоит в группе номер', self.groups)

    def get_att(self, subject):
        pass

    def write_att(self, subject):
        con = sqlite3.connect('../resourses/db')
        cur = con.cursor()
        subjs = {'гит': 0, 'математика': 1, 'информатика': 2, 'программирование': 3, 'английский': 4, 'русский': 5, 'дискретная математика': 6, 'орг': 7, 'история': 8, 'физика': 9}
        try:
            subjs[subject]
        except Exception:
            print(f'Данный студент не имеет предмета {subject} в своем расписании.')
        else:
            att = self.att.split()
            att[subjs[subject]] = '-'.join([att[subjs[subject]].split('-')[0], str(int(att[subjs[subject]].split('-')[1]) + 1)])
            print(att)
            self.att = ' '.join(att)
            cur.execute(f"UPDATE users SET att = '{self.att}' WHERE id = {self.id}")
            con.commit()
