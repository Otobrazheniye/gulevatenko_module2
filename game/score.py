
# <!!__________ __________!!>
#! ScoreHandler

# game_record — объект класса GameRecord, туда мы будем считывать сохранённые очки и записывать таблицу с новыми
# file_name — имя файла, откуда и куда мы записываем очки


# __init__ — принимает только имя файла и сохраняет его. Вызывает метод для чтения файла
# read — метод, который будет читать файл и каждую его строку сохранять в PlayerRecord, которые будут сохраняться в GameRecord
# save — метод, который нужен, чтобы записать новые результаты в файл (предварительно отсортировать и обрезать, если нужно)
# display — метод для отображения очков


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

    def __eq__(self:PlayerRecord,other:PlayerRecord)->bool:
        if not isinstance(other,PlayerRecord):
            return NotImplemented
        if self.name == other.name:
            return self.name == other.name and self.mode == other.mode
        return False



class GameRecord:
    def __init__(self):
        self.records = []



    def add_record(self,new_record:PlayerRecord):
        for i,record in enumerate(self.records):
            if record == new_record:
                self.records[i] = new_record
                self.prepare_records()
                return
        self.records.append(new_record)
        self.prepare_records()


    def prepare_records(self):
        self.records.sort(reverse=True)
        self.records = self.records[:settings.MAX_SCORE]


class ScoreHandler:
    def __init__(self,file_name: str):
        self.file_name = file_name
        self.game_record = GameRecord()
        self.read()

    def read(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                parts = line.strip().split(",")
                
                name =parts[0]
                mode =parts[1]
                score=int(parts[2])

                records = PlayerRecord(name,mode,score)
                self.game_record.add_record(records)
        except FileNotFoundError:
            pass

    def save(self):
        self.game_record.prepare_records()

        with open(self.file_name, "w", encoding="utf-8") as f:
            for record in self.game_record.records:
                line = f"{record.name},{record.mode},{record.score}\n"
                f.write(line)

        
    def display(self):
        for record in self.game_record.records:
            print(record)


# Note
# players = [Player(10), Player(5), Player(20)]

# players.sort()

# for p in players:
#     print(p.score)