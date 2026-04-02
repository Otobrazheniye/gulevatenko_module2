import game.game
from game.exceptions import PlayerExit

while True:
    try:
        game_app = game.game.Game()
        user_choose = game_app.gameui.show_main_menu()
        game_app.play(user_choose)

    except PlayerExit as e:
        print(e)
        break
