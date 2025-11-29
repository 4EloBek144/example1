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
        con = sqlite3.connect('../resourses/db')
        cur = con.cursor()
        cur.execute(f"UPDATE timetable SET {part} = '{inf}' WHERE id = {self.id}")
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

        self.groups = []
        for i in groups:
            if i[2] == self.id:
                self.groups.append(str(i[0]))
        if self.groups == []:
            print(f'По расписанию "{self.name}" никто не обучается')
        else:
            print(f'По расписанию "{self.name}" обучаются группы с номерами:', ''.join(self.groups))

    def tt_cont(self, n):
        subjects = {}
        for j in range(6):
            for i in self.get(n)[j].split('|'):
                if i in subjects:
                    subjects[i] += 1
                else:
                    subjects[i] = 1
        return subjects
