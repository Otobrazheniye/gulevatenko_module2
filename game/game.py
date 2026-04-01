from . import models
from . import settings
from . import score
from .exceptions import GameOver, EnemyDown, PlayerExit


# Input / Output helpers
def show_main_menu() -> int:
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


def ask_player_name() -> str:
    return input("Enter player name: ")


# Game logic
def print_round_info(player: models.Player, enemy: models.Enemy) -> None:
    print("\n>->->-> !!New Round!! <-<-<-<")
    print(f"Player lives: {player.lives} | score: {player.score}")
    print(f"Enemy level: {enemy.level} | lives: {enemy.lives}")


def is_player_winner(player_attack: str, enemy_attack: str) -> bool:
    return (
        (player_attack == settings.PAPER and enemy_attack == settings.STONE) or
        (player_attack == settings.STONE and enemy_attack == settings.SCISSORS) or
        (player_attack == settings.SCISSORS and enemy_attack == settings.PAPER)
    )


def handle_round_result(player: models.Player, enemy: models.Enemy, player_attack: str, enemy_attack: str) -> None:
    print(f"Player attack: {player_attack}")
    print(f"Enemy attack: {enemy_attack}")

    if player_attack == enemy_attack:
        print("Draw!")
        return

    if is_player_winner(player_attack, enemy_attack):
        print("Player wins the round!")
        models.player_add_score(player)
        models.enemy_decrease_lives(enemy)
        return

    print("Enemy wins the round!")
    models.player_decrease_lives(player)


def play_round(player: models.Player, enemy: models.Enemy) -> None:
    print_round_info(player, enemy)

    player_attack = models.player_select_attack()
    enemy.player_history = player_attack
    enemy_attack = models.enemy_select_attack(enemy)

    handle_round_result(player, enemy, player_attack, enemy_attack)


def create_player() ->models.Player:
    name = ask_player_name()
    return models.Player(name)


def create_enemy() -> models.Enemy:
    mode_number = models.choose_mode()
    mode = models.create_mode(mode_number)
    return models.Enemy(mode, settings.START_LEVEL)


def start_game() -> None:
    player = create_player()
    enemy = create_enemy()

    while True:
        try:
            play_round(player, enemy)

        except EnemyDown as e:
            print(e)
            print("New enemy appeared!")

        except GameOver as e:
            print(e)
            # print(f"Final score: {player.score}")
            player_record = score.PlayerRecord(player.name,enemy.mode.__class__.__name__,player.score)
            total_board = score.ScoreHandler("score_board.txt")
            total_board.game_record.add_record(player_record)
            total_board.save()
            break


def show_score_info() -> None:
    total_board = score.ScoreHandler("score_board.txt")
    total_board.display()


def play(choice: int) -> None:
    match choice:
        case 1:
            start_game()
        case 2:
            show_score_info()
        case 3:
            raise PlayerExit("Good Bye!")
        case _:
            print("Wrong menu choice")
