# Player
# Атрибуты:

#1 name — имя игрока, задаётся пользователем через консоль
#1 lives — количество жизней, берётся из константы из settings.py
#1 score — очки игрока, изначально 0

# Методы:

#1 __init__ — для инициализации игрока, принимает только имя, назначает имя, количество жизней и очков
#1 select_attack — метод для ввода атаки игроком. Вводим до тех пор, пока пользователь не введёт валидное значение (1, 2, 3),  использует константы из файла settings.py
#1 decrease_lives — метод, который будет вызываться, если игрок проиграл «бой», уменьшает жизни на 1. Если жизни закончились, вызывает исключение GameOver из файла exceptions.py
#1 add_score — метод для начисления очков игроку

# Enemy
# Атрибуты:

#1 lives — количество жизней, изначально зависит от уровня соперника и уровня сложности, уменьшается на 1, когда соперник проигрывает «бой»
#1 level — уровень соперника, будет увеличиваться с каждым новым соперником. Изначально 1
# Методы:

#1 __init__ — для инициализации соперника, принимает только уровень и сложность, чтобы вычислить количество жизней, назначает количество жизней и уровень
#1 select_attack — метод для случайного выбора атаки (1, 2, 3), использует константы из файла settings.py
#1 decrease_lives — уменьшает жизни при проигрыше «боя», вызывает исключение EnemyDown из файла exceptions.py, если у соперника закончились жизни
import random
import settings
from exceptions import GameOver
from exceptions import EnemyDown

# Player
class Player():
    def __init__(self, name: str):
        self.name = name
        self.lives = settings.LIVES 
        # change on const settings.py
        self.score = 0
# Enemy
class Enemy:
    def __init__(self, mode: int, level: int):
        self.mode = mode
        self.level = level

        if self.mode == 1:
            self.lives = self.level
        else:
            self.lives = self.level + 2

        self.player_history = None

def choose_mode():
    while True:
        try:
            mode = int(input(settings.MODES))
            if 0 < mode < 3:
                return mode
            else:
                print("Enter correct num")
        except ValueError:
            print("Please enter a number")

# Methods
class Select_attack:
    def player_select_attack(self, player: Player) -> int:
        while True:
            try:
                action_choose = int(input("Choose attack: \n1] Paper \n2]Stone \n3]Scissors"))
                attack = self._number_to_attack(action_choose)
                if attack is not None:
                    return attack
                
            except ValueError:
                print("Please enter a number")

    def enemy_select_attack(self,enemy:Enemy) -> int:
        if enemy.mode == 2:
            match enemy.player_history:
                case 1:
                    number = random.choice((1 , 2))
                case 2,3:
                    number = random.choice((2 , 3))
                case _:
                    number = random.randint(1,3)
        elif enemy.mode == 1:
            number = random.randint(1,3)
        return self._number_to_attack(number)
        

    def _number_to_attack(self, number: int):
        match number:
            case 1:
                return settings.PAPER
            case 2:
                return settings.STONE
            case 3:
                return settings.SCISSORS
            case _:
                print("Wrong parameter")
                return None
            
class Decrease_lives():
    def enemy_decrease_lives(self,enemy:Enemy,result:int):
        if result == 1:
            enemy.lives -=1
            if enemy.lives <= 0:
                enemy.level += 1
                enemy.lives = enemy.level + 1
                raise EnemyDown (f"{enemy.level} Next Level\n\tEnemy Died!")

    def player_decrease_lives(self,player:Player):
        player.lives -= 1
        if player.lives <= 0:
            raise GameOver (f"{player.name} Died!")

class Add_score():
        def player_add_score(self,player:Player):
            player.score += 1



name = input("Enter player name:")
player1 = Player(name)
mode = choose_mode()
enemy = Enemy(mode, settings.LEVEL)