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
        if isinstance(self.mode, Normal):
            return self.level
        return self.level + 2


def choose_mode():
    while True:
        try:
            mode = int(input(settings.MODE_PROMPT))
            if mode in MODES:
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
            enemy.lives = enemy._calculate_lives()
            raise EnemyDown (f"{enemy.level} Next Level\n\tEnemy Died!")

def player_decrease_lives(player:Player):
    player.lives -= 1
    if player.lives <= 0:
        raise GameOver (f"{player.name} Died!")



def player_add_score(player:Player):
    player.score += 1


        

# temp main
while True:
    try:
        user_choose = int(input(
            "Welcome!\n"
            "Choose what process you want to do?\n"
            "1] Start Game\n"
            "2] Score information\n"
            "3] Exit\n"
        ))

        match user_choose:
            case 1:
                name = input("Enter player name: ")
                player1 = Player(name)
# plr -> C
                mode_number = choose_mode()
                mode = create_mode(mode_number)
# mode -> C
                enemy = Enemy(mode, settings.LEVEL)
# enm -> C
                while True:
                    try:
                        print("\n>->->-> !!New Round!! <-<-<-<")
                        print(f"Player lives: {player1.lives} | score: {player1.score}")
                        print(f"Enemy level: {enemy.level} | lives: {enemy.lives}")
# inf -> S
                        player_attack = player_select_attack(player1)
                        enemy.player_history = player_attack
                        enemy_attack = enemy_select_attack(enemy)
# enm & plr -> c atk
                        print(f"Player attack: {player_attack}")
                        print(f"Enemy attack: {enemy_attack}")
# inf -> S
                        if player_attack == enemy_attack:
                            print("Draw!")
# D
                        elif (
                            (player_attack == settings.PAPER and enemy_attack == settings.STONE) or
                            (player_attack == settings.STONE and enemy_attack == settings.SCISSORS) or
                            (player_attack == settings.SCISSORS and enemy_attack == settings.PAPER)
                        ):
                            print("Player wins the round!")
                            player_add_score(player1)
                            enemy_decrease_lives(enemy, 1)
# W
                        else:
                            print("Enemy wins the round!")
                            player_decrease_lives(player1)
# L
                    except EnemyDown as e:
                        print(e)
                        print("New enemy appeared!")
                        continue

                    except GameOver as e:
                        print(e)
                        print(f"Final score: {player1.score}")
                        break

            case 2:
                print("Score information is not implemented yet.")

            case 3:
                raise PlayerExit("Good Bye!")

            case _:
                print("Wrong menu choice")

    except PlayerExit as e:
        print(e)
        break

    except ValueError:
        print("Please enter a number")
