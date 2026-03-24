from . import settings

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
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                name = parts[0]
                mode = parts[1]
                score = int(parts[2])

                record = PlayerRecord(name, mode, score)
                self.game_record.add_record(record)
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


# eq
    # def add_record(...
    #eq       if record == new_record:
    #             ..