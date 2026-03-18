# score.py
# Классы:

# ScoreHandler — класс для обработки очков
# GameRecord — класс, содержащий записи об игроках
# PlayerRecord — класс для хранения записи об одном игроке


# <!!__________ __________!!>
#! ScoreHandler

# game_record — объект класса GameRecord, туда мы будем считывать сохранённые очки и записывать таблицу с новыми
# file_name — имя файла, откуда и куда мы записываем очки


# __init__ — принимает только имя файла и сохраняет его. Вызывает метод для чтения файла
# read — метод, который будет читать файл и каждую его строку сохранять в PlayerRecord, которые будут сохраняться в GameRecord
# save — метод, который нужен, чтобы записать новые результаты в файл (предварительно отсортировать и обрезать, если нужно)
# display — метод для отображения очков


#! GameRecord
# records — список объектов типа PlayerRecord

# __init__ — создаёт объект с пустым списком записей
# add_record — метод для добавления записи об одном игроке. Должен проверять, нет ли у нас уже такого игрока, и если есть, то перезаписывать его результат. 
# Тот же самый игрок проверяется по имени и уровню сложности (игрок может быть представлен в таблице два раза на разном уровне сложности). 
# Можно использовать magic-метод __eq__ для поиска через in

# prepare_records — метод для сортировки существующих результатов и обрезки до максимального количества, указанного в настройках


#! PlayerRecord
# name mode score 

# __init__ — для создания объекта принимает все три параметра
# __gt__ — чтобы можно было отсортировать записи по очкам
# __str__ — для удобного вывода данных

import models
import settings

class PlayerRecord:
    # def __init__(self, player_name:models.Player, enemy_mode:models.Enemy):
    #     self.name = player_name.name
    #     self.mode = enemy_mode.mode
    #     self.score= player_name.score

    def __init__(self, name: str, mode: str, score: int):
        self.name = name
        self.mode = mode
        self.score = score
    
    def __str__(self) ->str:
        return f"Name: {self.name}\tMode: {self.mode}\t Score: {self.score}\n"
    
    def __gt__(self,other:"PlayerRecord") -> bool:
        if not isinstance(other,PlayerRecord):
            return NotImplemented
        return self.score > other.score




class ScoreHandler:
    def __init__(self,records:PlayerRecord):
        self.records = []

    def __eq__(self:PlayerRecord,other:PlayerRecord):
        if not isinstance(other,PlayerRecord):
            return NotImplemented
        if self.name == other.name:
            return self.mode == other.mode
        return False

    def add_record(self):
        pass


class GameRecord:
    pass

# Note
# players = [Player(10), Player(5), Player(20)]

# players.sort()

# for p in players:
#     print(p.score)