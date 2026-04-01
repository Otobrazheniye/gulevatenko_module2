from abc import ABC, abstractmethod
import random
from . import settings
from game.exceptions import GameOver, EnemyDown, PlayerExit


# Player
class Player():
    def __init__(self, name: str):
        self.name = name
        self.lives = settings.LIVES 
        self.score = 0


class Mode(ABC):
    @abstractmethod
    def attack(self,player_history=None) -> int:
        pass

    @abstractmethod
    def get_enemy_lives(self, level: int) -> int:
        pass


class Normal(Mode):
    def attack(self, player_history=None) -> int:
        return random.randint(1, 3)

    def get_enemy_lives(self, level: int) -> int:
        return level


class Hard(Mode):
    def attack(self, player_history=None) -> int:
        match player_history:
            case 1:
                return random.choice((1, 2))
            case 2 | 3:
                return random.choice((2, 3))
            case _:
                return random.randint(1, 3)
            

    def get_enemy_lives(self, level: int) -> int:
        return level + 2


MODES = {
    1: Normal,
    2: Hard,
}


def create_mode(mode_number: int) -> Mode:
    mode_class = MODES.get(mode_number)
    if mode_class is None:
        raise ValueError("Wrong mode")
    return mode_class()


# Enemy
class Enemy:
    def __init__(self, mode: Mode, level: int):
        self.mode = mode
        self.level = level
        self.player_history = None
        self.lives = self._calculate_lives()        


    def _calculate_lives(self) -> int:
        return self.mode.get_enemy_lives(self.level)


def choose_mode():
    while True:
        try:
            mode = int(input(settings.MODE_PROMPT))
            if mode in MODES:
                return mode
            print("Enter correct num")
        except ValueError:
            print("Please enter a number")


def player_select_attack() -> str:
    while True:
        try:
            action_choose = int(input("Choose attack: \n1] Paper \n2]Stone \n3]Scissors"))
            attack = _number_to_attack(action_choose)
            if attack is not None:
                return attack
            print("Wrong parameter")    

        except ValueError:
            print("Please enter a number")


def enemy_select_attack(enemy: Enemy) -> int:
    enemy_action = enemy.mode.attack(enemy.player_history)
    return _number_to_attack(enemy_action)

        
def _number_to_attack(number: int) -> str | None:
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
            

def enemy_decrease_lives(enemy: Enemy) -> None:
    enemy.lives -=1
    if enemy.lives <= 0:
        enemy.level += 1
        enemy.lives = enemy._calculate_lives()
        raise EnemyDown (f"{enemy.level} Next Level\n\tEnemy Died!")


def player_decrease_lives(player:Player) -> None:
    player.lives -= 1
    if player.lives <= 0:
        raise GameOver (f"{player.name} Died!")


def player_add_score(player:Player) -> None:
    player.score += 1
