from game.score import ScoreHandler
from game.models import *

import pytest


# def test_all_records_types():
#     total_board = ScoreHandler("dublicate.txt")

#     print(total_board.game_record.records)
#     assert len(total_board.game_record.records) > 0
#     for record in total_board.game_record.records:
#         assert isinstance(record.name, str)
#         assert isinstance(record.mode, str)
#         assert isinstance(record.score, int)


# Player:

#! Создание игрока с корректным именем и начальными значениями (lives, score)
#! Метод add_score корректно увеличивает очки
#! Метод decrease_lives уменьшает жизни на 1
#! Метод decrease_lives вызывает GameOver, когда жизни заканчиваются


# <!-------- PLAYER ---------!>
@pytest.mark.parametrize(
    "name, lives, score",
    [
        ("Oleg", 3, 0),
    ]
)
def test_create_player(name, lives, score):
    tplayer = Player(name)

    assert tplayer.name == name
    assert tplayer.lives == lives
    assert tplayer.score == score


@pytest.mark.parametrize("score",[0])
def test_add_score(score):
    tplayer = Player("test_Andrii")
    player_add_score(tplayer)
    assert tplayer.score == score + 1 

@pytest.mark.parametrize("lives",[3])
def test_decrease_lives(lives):
    tplayer = Player("test_Andrii")
    tplayer.lives = lives
    player_decrease_lives(tplayer)
    assert tplayer.lives == lives - 1

@pytest.mark.parametrize("expected_exception, lives",[(GameOver,1)])
def test_decrease_game_over(expected_exception,lives):
    tplayer = Player("test_Andrii")
    tplayer.lives = lives
    with pytest.raises(expected_exception):
        player_decrease_lives(tplayer)        



 

