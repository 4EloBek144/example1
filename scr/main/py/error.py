class Error: # Класс для вывода ошибок при использовании функций других классов
    def __init__(self, uid, name):
        self.id = uid
        self.name = name

    def find_groups(self):
        print('Ошибка')


errors = [Error(-1, 'Ошибка')]
