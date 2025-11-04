import sqlite3


class User:
    def __init__(self, uid, name, att, role):
        self.id = uid
        self.name = name
        self.att = att
        self.role = role

    def write(self, part, inf):
        con = sqlite3.connect('C:/Users/Arseniy/PycharmProjects/sem1/scr/main/resourses/db')
        cur = con.cursor()
        match part:
            case 'name':
                cur.execute(f"UPDATE users SET name = '{inf}' WHERE id = {self.id}")
            case 'att':
                cur.execute(f"UPDATE users SET att = '{inf}' WHERE id = {self.id}")
            case 'role':
                cur.execute(f"UPDATE users SET role = '{inf}' WHERE id = {self.id}")
        con.commit()
        con.close()

    def find_groups(self):
        con = sqlite3.connect('C:/Users/Arseniy/PycharmProjects/sem1/scr/main/resourses/db')
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
            print('Отвечает за группы с номерами:', ' '.join(self.groups))
        elif self.role == 'st':
            self.groups = 0
            for i in groups:
                if str(self.id) in str(i[1]):
                    self.groups = i[0]
            if self.groups == 0:
                print('Студент не состоит в группе')
            else:
                print('Студент состоит в группе номер', self.groups)

