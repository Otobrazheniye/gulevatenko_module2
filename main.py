import game.game
from game.exceptions import PlayerExit

def run():
    game_app = game.game.Game()
    while True:
        try:
            user_choose = game_app.gameui.show_main_menu()
            game_app.play(user_choose)

        except PlayerExit as e:
            print(e)
            break


if __name__=='__main__': 
    run()
