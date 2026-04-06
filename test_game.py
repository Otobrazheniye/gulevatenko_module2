from game.score import *
from game.models import *
from game.game import *
import pytest

# Happy Path, Edge Cases / Boundary Cases, Smoke Tests, Negative Cases,Exception Tests
# Integration Tests

# <!-------- PLAYER ---------!>
class TestPlayer:
    def test_create_player_smoke_test(self):
        tplayer = Player("test_Andrii")
        assert tplayer is not None


    @pytest.mark.parametrize("name",["Oleg","Solomia","Elisabeth"])
    def test_create_player_happy_path(self,name):
        tplayer = Player(name)

        assert tplayer.name == name


    def test_create_player_happy_path_init(self):
        tplayer = Player("Andrii_test")
        assert tplayer.lives == settings.LIVES
        assert tplayer.score == 0


    @pytest.mark.parametrize("name",["S", "Andrii" * 100, "31/.@##!&^"])
    def test_create_player_edge_case(self,name):
        tplayer = Player(name)

        assert tplayer.name == name
        assert tplayer.lives == settings.LIVES
        assert tplayer.score == 0


    def test_create_player_negative_case(self):
        tplayer = Player("   Oleg    ")

        assert tplayer.name == "Oleg"


    @pytest.mark.parametrize("name",[None, [], {}])
    def test_create_player_exception_case_type(self,name):

        with pytest.raises(TypeError, match="Name must be string"):
            Player(name)
        

    @pytest.mark.parametrize("name",[ "", " "])
    def test_create_player_exception_case_value(self,name):

        with pytest.raises(ValueError):
            Player(name)


    @pytest.mark.parametrize("score",[1,4,8])
    def test_add_score_happy_path(self,score):
        tplayer = Player("test_Andrii")
        tplayer.score = score
        tplayer.player_add_score()

        assert tplayer.score == score + 1 


    @pytest.mark.parametrize("score",[0,999999])
    def test_add_score_edge_case(self,score):
        tplayer = Player("test_Andrii")
        tplayer.score = score
        tplayer.player_add_score()

        assert tplayer.score == score + 1


    def test_add_score_negative_case(self):
        tplayer = Player("test_Andrii")
        tplayer.score = -5
        tplayer.player_add_score()

        assert tplayer.score == 1


    @pytest.mark.parametrize("score",[None,[],{},3.14,"5"])
    def test_add_score_exception_case(self,score):
        tplayer = Player("test_Andrii")
        tplayer.score = score

        with pytest.raises(TypeError):
            tplayer.player_add_score()
           

    @pytest.mark.parametrize("lives",[2,5,10])
    def test_decrease_lives_happy_path(self,lives):
        tplayer = Player("test_Andrii")
        tplayer.lives = lives
        tplayer.player_decrease_lives()

        assert tplayer.lives == lives - 1
    

    @pytest.mark.parametrize("lives",[2,99999])
    def test_decrease_lives_edge_cases(self,lives):
        tplayer = Player("test_Andrii")
        tplayer.lives = lives
        tplayer.player_decrease_lives()

        assert tplayer.lives == lives - 1


    @pytest.mark.parametrize("lives",[-20,-1,0])
    def test_decrease_lives_negative_cases(self,lives):
        tplayer = Player("test_Andrii")
        tplayer.lives = lives

        with pytest.raises(GameOver):
            tplayer.player_decrease_lives()


    def test_decrease_lives_exception_test(self):
        tplayer = Player("test_Andrii")
        tplayer.lives = 1

        with pytest.raises(GameOver):
            tplayer.player_decrease_lives()




# <!-------- ENEMY ---------!>
@pytest.mark.parametrize(
    "mode, level, expected_lives",
    [
        (Normal(), 1, 1),
        (Normal(), 3, 3),
        (Hard(), 1, 3),
        (Hard(), 2, 4),
    ]
)
def test_enemy_lives(mode, level, expected_lives):
    tenemy = Enemy(mode, level)

    assert tenemy.lives == expected_lives


@pytest.mark.parametrize(
    "player_history, expected_attacks",
    [
        (1, {settings.PAPER, settings.STONE}),
        (2, {settings.STONE, settings.SCISSORS}),
        (3, {settings.PAPER, settings.SCISSORS}),
        # error
    ]
)
def test_select_attack(player_history, expected_attacks):
    tenemy = Enemy(Hard(), 3)
    tenemy.player_history = player_history

    enemy_attack = Enemy.enemy_select_attack(tenemy)

    assert enemy_attack in expected_attacks

@pytest.mark.parametrize("lives,expected_exception",[(1,EnemyDown)])
def test_enemy_decrease_lives(lives,expected_exception):
    tenemy = Enemy(Hard(),1)
    tenemy.lives = lives
    with pytest.raises(expected_exception):
        Enemy.enemy_decrease_lives(tenemy)

# <!-------- Game ---------!>

@pytest.mark.parametrize(
    "tplayer_attack, tenemy_attack",[(settings.PAPER, settings.PAPER)])
def test_fight_draw(tplayer_attack, tenemy_attack):
    tplayer = Player("test_Andrii")
    tenemy = Enemy(Hard(), 1)
    game = Game(tplayer,tenemy)

    start_player_lives = tplayer.lives
    start_enemy_lives = tenemy.lives
    start_score = tplayer.score

    game.handle_round_result(tplayer_attack, tenemy_attack)

    assert tplayer.lives == start_player_lives
    assert tenemy.lives == start_enemy_lives
    assert tplayer.score == start_score

@pytest.mark.parametrize("tplayer_attack, tenemy_attack",[(settings.PAPER, settings.STONE)])
def test_fight_win(tplayer_attack,tenemy_attack):
    tplayer = Player("test_Andrii")
    tenemy = Enemy(Hard(),1)
    game = Game(tplayer,tenemy)

    start_player_lives = tplayer.lives
    start_enemy_lives = tenemy.lives
    start_score = tplayer.score

    game.handle_round_result(tplayer_attack,tenemy_attack)
    assert tplayer.lives == start_player_lives
    assert tenemy.lives < start_enemy_lives
    assert tplayer.score > start_score


@pytest.mark.parametrize("tplayer_attack, tenemy_attack",[(settings.SCISSORS, settings.STONE)])
def test_fight_lose(tplayer_attack,tenemy_attack):
    tplayer = Player("test_Andrii")
    tenemy = Enemy(Hard(),1)
    game = Game(tplayer,tenemy)

    start_player_lives = tplayer.lives
    start_enemy_lives = tenemy.lives
    start_score = tplayer.score

    game.handle_round_result(tplayer_attack,tenemy_attack)
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
    monkeypatch.setattr(GameUI, "choose_mode", lambda self: mode_number)
    game = Game()
    enemy = game.create_enemy()
    assert enemy.level == settings.START_LEVEL
    assert isinstance(enemy.mode, expected_mode)

# <!-------- PlayerRecord ---------!>

def test_sort_records():
    records = [
        score.PlayerRecord("A", "Normal", 10),
        score.PlayerRecord("B", "Normal", 5),
        score.PlayerRecord("C", "Normal", 20),
    ]

    records.sort(reverse=True)

    scores = [r.score for r in records]

    assert scores == [20, 10, 5]

def test_eq_records():
    records = [
        score.PlayerRecord("A", "Normal", 10),
        score.PlayerRecord("A", "Normal", 5),
    ]  

    assert records[0] == records[1]

# <!-------- GameRecord ---------!>

def test_add_record():
    game_record = GameRecord()
    new_record = PlayerRecord("Andrii", "Hard", 6)

    game_record.add_record(new_record)
    
    assert len(game_record.records) == 1
    assert game_record.records[0] == new_record

def test_change_record():
    game_record = GameRecord()

    new_record = PlayerRecord("Andrii","Hard",6)
    game_record.add_record(new_record)

    new_record2 = PlayerRecord("Andrii","Hard",10)
    game_record.add_record(new_record2)

    assert len(game_record.records) == 1
    assert game_record.records[0] == new_record2

def test_prepare_records_sort_and_limit(monkeypatch):
    monkeypatch.setattr(settings, "MAX_SCORE", 2)

    game_record = GameRecord()

    game_record.records = [
        PlayerRecord("A", "Normal", 10),
        PlayerRecord("B", "Normal", 5),
        PlayerRecord("C", "Normal", 20),
    ]

    game_record.prepare_records()

    scores = [r.score for r in game_record.records]
    assert scores == [20, 10]

    assert len(game_record.records) == 2


# <!-------- ScoreHandler: ---------!>


def test_all_records_types():
    total_board = ScoreHandler("dublicate.txt")

    print(total_board.game_record.records)
    assert len(total_board.game_record.records) > 0
    # 0
    for record in total_board.game_record.records:
        assert isinstance(record.name, str)
        assert isinstance(record.mode, str)
        assert isinstance(record.score, int)

def test_save_records(tmp_path):
    file = tmp_path / "test.txt"
    # создай путь внутри этой папки. tmp_path - pathlib.Path
    # import os         file = os.path.join(tmp_path, "test.txt")

    score_handler = ScoreHandler(str(file))
    score_handler.game_record.records = [
        PlayerRecord("Andrii", "Hard", 10),
        PlayerRecord("Oleg", "Normal", 5),
    ]
    score_handler.save()
    content = file.read_text(encoding="utf-8").splitlines()

    assert content == [
        "Andrii,Hard,10",
        "Oleg,Normal,5",
    ]

