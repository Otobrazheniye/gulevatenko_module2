
# Для этого вызывает два метода: fight и handle_fight_result. Отслеживает, не произошло ли одно из исключений при вызове второго метода — GameOver или EnemyDown. 
# При первом завершает игру и вызывает метод для записи очков, при втором создаёт нового, более сильного соперника
# fight — метод запрашивает у пользователя и соперника атаки, из констант получает результат боя (-1, 0, 1)
# handle_fight_result — принимает результат боя и в зависимости от результата отнимает жизни либо у игрока, либо у соперника
# save_score — вызывает сохранение очков при помощи класса из файла score.py


import models
import settings
from exceptions import GameOver, EnemyDown, PlayerExit



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
    return models.Enemy(mode, settings.LEVEL)


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
            print(f"Final score: {player.score}")
            break


def show_score_info() -> None:
    print("Score information is not implemented yet.")


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

#  temp main 2

while True:
    try:
        user_choose = show_main_menu()
# int menu choose
        play(user_choose)

    except PlayerExit as e:
        print(e)
        break
# [show_main_menu -> play()] -> [start_game()] -> [create_player() -> create_enemy() -> play_round(player, enemy) or
# create_player() -> ask_player_name()
# create_enemy_for_game() -> models.choose_mode() -> models.create_mode(mode_number) 
# play_round(player, enemy) -> print_round_info(player, enemy) -> models.player_select_attack() -> SAVE player atk history -> models.enemy_select_attack(enemy) -> handle_round_result(player, enemy, player_attack, enemy_attack) -> [models.player_add_score(player) and models.enemy_decrease_lives(enemy)] or  models.player_decrease_lives(player)
