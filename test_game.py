from game.score import ScoreHandler
from game.models import *
from game.game import *

import pytest


# def test_all_records_types():
#     total_board = ScoreHandler("dublicate.txt")

#     print(total_board.game_record.records)
#     assert len(total_board.game_record.records) > 0
#     for record in total_board.game_record.records:
#         assert isinstance(record.name, str)
#         assert isinstance(record.mode, str)
#         assert isinstance(record.score, int)


# <!-------- PLAYER ---------!>
# @pytest.mark.parametrize(
#     "name, lives, score",
#     [
#         ("Oleg", 3, 0),
#     ]
# )
# def test_create_player(name, lives, score):
#     tplayer = Player(name)

#     assert tplayer.name == name
#     assert tplayer.lives == lives
#     assert tplayer.score == score


# @pytest.mark.parametrize("score",[0])
# def test_add_score(score):
#     tplayer = Player("test_Andrii")
#     player_add_score(tplayer)
#     assert tplayer.score == score + 1 

# @pytest.mark.parametrize("lives",[3])
# def test_decrease_lives(lives):
#     tplayer = Player("test_Andrii")
#     tplayer.lives = lives
#     player_decrease_lives(tplayer)
#     assert tplayer.lives == lives - 1

# @pytest.mark.parametrize("expected_exception, lives",[(GameOver,1)])
# def test_decrease_game_over(expected_exception,lives):
#     tplayer = Player("test_Andrii")
#     tplayer.lives = lives
#     with pytest.raises(expected_exception):
#         player_decrease_lives(tplayer)        


# <!-------- ENEMY ---------!>


# @pytest.mark.parametrize(
#     "mode, level, expected_lives",
#     [
#         (Normal(), 1, 1),
#         (Normal(), 3, 3),
#         (Hard(), 1, 3),
#         (Hard(), 2, 4),
#     ]
# )
# def test_enemy_lives(mode, level, expected_lives):
#     tenemy = Enemy(mode, level)

#     assert tenemy.lives == expected_lives


# @pytest.mark.parametrize(
#     "player_history, expected_attacks",
#     [
#         (1, {settings.PAPER, settings.STONE}),
#         (2, {settings.STONE, settings.SCISSORS}),
#         (3, {settings.PAPER, settings.SCISSORS}),
#     ]
# )
# def test_select_attack(player_history, expected_attacks):
#     tenemy = Enemy(Hard(), 1)
#     tenemy.player_history = player_history

#     enemy_attack = enemy_select_attack(tenemy)

#     assert enemy_attack in expected_attacks

# @pytest.mark.parametrize("lives,expected_exception",[(1,EnemyDown)])
# def test_enemy_decrease_lives(lives,expected_exception):
#     tenemy = Enemy(Hard(),1)
#     tenemy.lives = lives
#     with pytest.raises(expected_exception):
#         enemy_decrease_lives(tenemy)

# <!-------- Game ---------!>

#! Метод fight возвращает корректный результат (-1, 0, 1) для разных комбинаций атак
#! Метод create_enemy создаёт соперника с правильным уровнем

@pytest.mark.parametrize(
    "tplayer_attack, tenemy_attack",[(settings.PAPER, settings.PAPER)])
def test_fight_draw(tplayer_attack, tenemy_attack):
    tplayer = Player("test_Andrii")
    tenemy = Enemy(Hard(), 1)

    start_player_lives = tplayer.lives
    start_enemy_lives = tenemy.lives
    start_score = tplayer.score

    handle_round_result(tplayer, tenemy, tplayer_attack, tenemy_attack)

    assert tplayer.lives == start_player_lives
    assert tenemy.lives == start_enemy_lives
    assert tplayer.score == start_score

@pytest.mark.parametrize("tplayer_attack, tenemy_attack",[(settings.PAPER, settings.STONE)])
def test_fight_win(tplayer_attack,tenemy_attack):
    tplayer = Player("test_Andrii")
    tenemy = Enemy(Hard(),1)

    start_player_lives = tplayer.lives
    start_enemy_lives = tenemy.lives
    start_score = tplayer.score

    handle_round_result(tplayer,tenemy,tplayer_attack,tenemy_attack)
    assert tplayer.lives == start_player_lives
    assert tenemy.lives < start_enemy_lives
    assert tplayer.score > start_score


@pytest.mark.parametrize("tplayer_attack, tenemy_attack",[(settings.SCISSORS, settings.STONE)])
def test_fight_lose(tplayer_attack,tenemy_attack):
    tplayer = Player("test_Andrii")
    tenemy = Enemy(Hard(),1)

    start_player_lives = tplayer.lives
    start_enemy_lives = tenemy.lives
    start_score = tplayer.score

    handle_round_result(tplayer,tenemy,tplayer_attack,tenemy_attack)
    assert tplayer.lives < start_player_lives
    assert tenemy.lives == start_enemy_lives
    assert tplayer.score == start_score



@pytest.mark.parametrize(
    "mode_number, expected_mode",
    [
        (1, models.Normal),
        (2, models.Hard),
    ]
)
def test_create_enemy(monkeypatch, mode_number, expected_mode):
    monkeypatch.setattr(models, "choose_mode", lambda: mode_number)

    enemy = create_enemy()

    assert enemy.level == settings.LEVEL
    assert isinstance(enemy.mode, expected_mode)

