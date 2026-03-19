import game.game
from game.exceptions import PlayerExit

while True:
    try:
        user_choose = game.game.show_main_menu()
        game.game.play(user_choose)

    except PlayerExit as e:
        print(e)
        break