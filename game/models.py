from abc import ABC, abstractmethod
import random
from . import settings
from game.exceptions import GameOver, EnemyDown, PlayerExit


# Player
class Player:
    def __init__(self, name: str):
        if not isinstance(name,str):
            raise TypeError("Name must be string")
        if name.strip() == "":
            raise ValueError("can't be empty")
        self.name = name.strip()
        self.lives = settings.LIVES 
        self.score = 0

    def player_decrease_lives(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            raise GameOver (f"{self.name} Died!")

    def player_add_score(self) -> None:
        if not isinstance(self.score, int):
            raise TypeError("Must be a correct number")
        if self.score < 0:
            self.score = 0
        self.score += 1


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
            case 2:
                return random.choice((2, 3))
            case 3:
                return random.choice((1, 3))
            case None:
                return random.randint(1, 3)
            case _:
                raise ValueError(f"Invalid player history: {player_history}")
            

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
        if not isinstance(mode,Mode):
            raise TypeError("mode must be an instance of Mode")
        if not isinstance(level,int):
            raise TypeError("level must be an integer")
        if level <= 0:
            self.level = 1
        else:
           self.level = level 
        self.mode = mode
        self.player_history = None
        self.lives = self._calculate_lives()        

    def enemy_decrease_lives(self) -> None:
        self.lives -=1
        if self.lives <= 0:
            self.level += 1
            self.lives = self._calculate_lives()
            raise EnemyDown (f"{self.level} Next Level\n\tEnemy Died!")
        
    def enemy_select_attack(self) -> int:
        enemy_action = self.mode.attack(self.player_history)
        return _number_to_attack(enemy_action)


    def _calculate_lives(self) -> int:
        return self.mode.get_enemy_lives(self.level)


# util
def _number_to_attack(number: int) -> str | None:
    match number:
        case 1:
            return settings.PAPER
        case 2:
            return settings.STONE
        case 3:
            return settings.SCISSORS
        case _:
            raise ValueError(f"Invalid attack number: {number}")
