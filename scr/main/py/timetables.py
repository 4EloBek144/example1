import sqlite3


class TimeTable: # Класс расписаний
    def __init__(self, uid, mon1, tue1, wed1, thu1, fri1, sat1, mon2, tue2, wed2, thu2, fri2, sat2, name):
        self.id = uid
        self.name = name
        self.mon1 = mon1
        self.tue1 = tue1
        self.wed1 = wed1
        self.thu1 = thu1
        self.fri1 = fri1
        self.sat1 = sat1
        self.mon2 = mon2
        self.tue2 = tue2
        self.wed2 = wed2
        self.thu2 = thu2
        self.fri2 = fri2
        self.sat2 = sat2

    def get(self, n): # Получение расписания как списка по чет/нечет неделям
        self.w1 = [self.mon1, self.tue1, self.wed1, self.thu1, self.fri1, self.sat1]
        self.w2 = [self.mon2, self.tue2, self.wed2, self.thu2, self.fri2, self.sat2]
        if n == 1:
            return self.w1
        else:
            return self.w2

    def write(self, part, inf): # Многа букав для отдельного изменения дней недели
        con = sqlite3.connect('C:/Users/Arseniy/PycharmProjects/sem1/scr/main/resourses/db')
        cur = con.cursor()
        match part:
            case 'mon1':
                cur.execute(f"UPDATE timetable SET mon1 = '{inf}' WHERE id = {self.id}")
            case 'tue1':
                cur.execute(f"UPDATE timetable SET tue1 = '{inf}' WHERE id = {self.id}")
            case 'wed1':
                cur.execute(f"UPDATE timetable SET wed1 = '{inf}' WHERE id = {self.id}")
            case 'thu1':
                cur.execute(f"UPDATE timetable SET thu1 = '{inf}' WHERE id = {self.id}")
            case 'fri1':
                cur.execute(f"UPDATE timetable SET fri1 = '{inf}' WHERE id = {self.id}")
            case 'sat1':
                cur.execute(f"UPDATE timetable SET sat1 = '{inf}' WHERE id = {self.id}")
            case 'mon2':
                cur.execute(f"UPDATE timetable SET mon2 = '{inf}' WHERE id = {self.id}")
            case 'tue2':
                cur.execute(f"UPDATE timetable SET tue2 = '{inf}' WHERE id = {self.id}")
            case 'wed2':
                cur.execute(f"UPDATE timetable SET wed2 = '{inf}' WHERE id = {self.id}")
            case 'thu2':
                cur.execute(f"UPDATE timetable SET thu2 = '{inf}' WHERE id = {self.id}")
            case 'fri2':
                cur.execute(f"UPDATE timetable SET fri2 = '{inf}' WHERE id = {self.id}")
            case 'sat2':
                cur.execute(f"UPDATE timetable SET sat2 = '{inf}' WHERE id = {self.id}")
            case 'name':
                cur.execute(f"UPDATE timetable SET name = '{inf}' WHERE id = {self.id}")
        con.commit()
        con.close()

    def find_groups(self): # Тот самый поиск из мейна
        con = sqlite3.connect('C:/Users/Arseniy/PycharmProjects/sem1/scr/main/resourses/db')
        cur = con.cursor()

        groups = []
        cur.execute("SELECT * FROM groups")
        for i in cur.fetchall():
            groups.append([i[0], i[1], i[2], i[3]])
        con.close()

        self.groups = []
        for i in groups:
            if i[2] == self.id:
                self.groups.append(str(i[0]))
        if self.groups == []:
            print(f'По расписанию "{self.name}" никто не обучается')
        else:
            print(f'По расписанию "{self.name}" обучаются группы с номерами:', ''.join(self.groups))
