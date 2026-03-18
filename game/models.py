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
from abc import ABC, abstractmethod
import random
import settings
from exceptions import GameOver, EnemyDown, PlayerExit

# Player
class Player():
    def __init__(self, name: str):
        self.name = name
        self.lives = settings.LIVES 
        # change on const settings.py
        self.score = 0

# mode
class Mode(ABC):
    @abstractmethod
    def attack(self) -> int:
        pass




class Normal(Mode):
    def __init__(self,player_history=None):
        self.player_history = player_history
    def attack(self)-> int:  
        return random.randint(1,3)
    


class Hard(Mode):
    def __init__(self,player_history=None):
        self.player_history = player_history

    def attack(self) -> int:
        match self.player_history:
            case 1:
                return random.choice((1 , 2))
            case 2,3:
                return random.choice((2 , 3))
            case _:
                return random.randint(1,3)

#endregion

def create_mode(mode_number: int) -> Mode:
    mode_class = settings.MODES.get(mode_number)
    if mode_class is None:
        raise ValueError("Wrong mode")
    return mode_class()

# Enemy
class Enemy:
    def __init__(self, mode: Mode, level: int):
        self.mode = mode
        self.level = level
        self.player_history = None

        if isinstance(mode, Normal):
            self.lives = self.level
        else:
            self.lives = self.level + 2


def choose_mode():
    while True:
        try:
            mode = int(input(settings.MODES))
            if mode in settings.MODES:
                return mode
            print("Enter correct num")
        except ValueError:
            print("Please enter a number")

# Methods

def player_select_attack(player: Player) -> int:
    while True:
        try:
            action_choose = int(input("Choose attack: \n1] Paper \n2]Stone \n3]Scissors"))
            attack = _number_to_attack(action_choose)
            if attack is not None:
                return attack
                
        except ValueError:
            print("Please enter a number")


def enemy_select_attack(enemy: Enemy) -> int:
    enemy.mode.player_history = enemy.player_history
    enemy_action = enemy.mode.attack()
    return _number_to_attack(enemy_action)
        

def _number_to_attack(number: int):
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
            

def enemy_decrease_lives(enemy:Enemy,result:int):
    if result == 1:
        enemy.lives -=1
        if enemy.lives <= 0:
            enemy.level += 1
            enemy.lives = enemy.level + 1
            raise EnemyDown (f"{enemy.level} Next Level\n\tEnemy Died!")

def player_decrease_lives(player:Player):
    player.lives -= 1
    if player.lives <= 0:
        raise GameOver (f"{player.name} Died!")


def player_add_score(player:Player):
    player.score += 1


# temp main     
while True:
    user_choose = int(input("Welcome! \n Choose what procces you want to do? \n1] Start Game \n\t 2] Score information \n\t\t 3] Exit"))
    match user_choose:
        case 1:
            name = input("Enter player name:")
            player1 = Player(name)

            mode_number = choose_mode()
            mode = create_mode(mode_number)

            enemy = Enemy(mode, settings.LEVEL)
            action_choose = player_select_attack(player1)

        case 2:
            pass
        case 3:
            raise PlayerExit("Good Bye!")