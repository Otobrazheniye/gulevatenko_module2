from . import models
from . import settings
from . import score
from .exceptions import GameOver, EnemyDown, PlayerExit


class Game:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.gameui = GameUI()
        
    def create_player(self) ->models.Player:
        name = self.gameui.ask_player_name()
        return models.Player(name)

    def create_enemy(self) -> models.Enemy:
        mode_number = models.choose_mode()
        mode = models.create_mode(mode_number)
        return models.Enemy(mode, settings.START_LEVEL)

    def play(self,choice: int) -> None:
        match choice:
            case 1:
                self.start_game()
            case 2:
                self.show_score_info()
            case 3:
                raise PlayerExit("Good Bye!")
            case _:
                print("Wrong menu choice")

    def start_game(self) -> None:
        self.player = self.create_player()
        self.enemy = self.create_enemy()
        while True:
            try:
                self.play_round()

            except EnemyDown as e:
                print(e)
                print("New enemy appeared!")

            except GameOver as e:
                print(e)
                player_record = score.PlayerRecord(self.player.name,self.enemy.mode.__class__.__name__,self.player.score)
                total_board = score.ScoreHandler("score_board.txt")
                total_board.game_record.add_record(player_record)
                total_board.save()
                break
            
    def play_round(self) -> None:
        self.print_round_info()
        player_attack = models.player_select_attack()
        self.enemy.player_history = player_attack
        enemy_attack = self.enemy.enemy_select_attack()

        self.handle_round_result( player_attack, enemy_attack)

    def handle_round_result(self, player_attack: str, enemy_attack: str) -> None:
        print(f"Player attack: {player_attack}")
        print(f"Enemy attack: {enemy_attack}")

        if player_attack == enemy_attack:
            print("Draw!")
            return

        if self.is_player_winner(player_attack, enemy_attack):
            print("Player wins the round!")
            self.player.player_add_score()
            self.enemy.enemy_decrease_lives()
            return

        print("Enemy wins the round!")
        self.player.player_decrease_lives()

    def print_round_info(self) -> None:
        print("\n>->->-> !!New Round!! <-<-<-<")
        print(f"Player lives: {self.player.lives} | score: {self.player.score}")
        print(f"Enemy level: {self.enemy.level} | lives: {self.enemy.lives}")

    def show_score_info(self) -> None:
        total_board = score.ScoreHandler("score_board.txt")
        total_board.display()
     
    def is_player_winner(self,player_attack: str, enemy_attack: str) -> bool:
        return (
            (player_attack == settings.PAPER and enemy_attack == settings.STONE) or
            (player_attack == settings.STONE and enemy_attack == settings.SCISSORS) or
            (player_attack == settings.SCISSORS and enemy_attack == settings.PAPER)
        )

class GameUI:
    def show_main_menu(self) -> int:
        while True:
            try:
                return int(input(
                    "Welcome!\n"
                    "Choose what process you want to do?\n"
                    "1] Start Game\n"
                    "2] Score information\n"
                    "3] Exit\n"
                ))
        
            except ValueError:
                print("Please enter a number")


    def ask_player_name(self) -> str:
        return input("Enter player name: ")
