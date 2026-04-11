from game.score import *
from game.models import *
from game.game import *
from game.models import _number_to_attack
import pytest


# Happy Path, Edge Cases / Boundary Cases, Smoke Tests, Negative Cases,Exception Tests
# Integration Tests

# <!-------- PLAYER ---------!>
class TestPlayer:
    def test_create_player_smoke(self):
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
    def test_decrease_lives_negative_case(self,lives):
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
class TestEnemy:
    def test_enemy_happy_path_init(self):
        tenemy = Enemy(Hard(),3)
        assert tenemy is not None


    @pytest.mark.parametrize("mode_number, expected_mode",[(1, models.Normal),(2, models.Hard),])
    def test_create_enemy_happy_path(self,monkeypatch, mode_number, expected_mode):
        monkeypatch.setattr(GameUI, "choose_mode", lambda self: mode_number)
        game = Game()
        enemy = game.create_enemy()

        assert enemy.level == settings.START_LEVEL
        assert isinstance(enemy.mode, expected_mode)


    @pytest.mark.parametrize("mode_number, expected_mode",[(1, models.Normal),(2, models.Hard),])
    def test_create_enemy_edge_case(self,monkeypatch, mode_number, expected_mode):
        monkeypatch.setattr(GameUI, "choose_mode", lambda self: mode_number)
        game = Game()
        enemy = game.create_enemy()
        
        assert enemy.level == settings.START_LEVEL
        assert isinstance(enemy.mode, expected_mode)


    @pytest.mark.parametrize("mode", [None, [], "dsdsd", {}])
    def test_create_enemy_exception_case_type_mode(self, mode):
        with pytest.raises(TypeError):
            Enemy(mode, 3)


    @pytest.mark.parametrize("level", [None, [], "dsdsd", {}])
    def test_create_enemy_exception_case_type_level(self, level):
        with pytest.raises(TypeError):
            Enemy(Hard(),level)

    
    @pytest.mark.parametrize("level", [-1, 0, -9999])
    def test_create_enemy_negative_case_level(self, level):
        tenemy = Enemy(Hard(), level)
        assert tenemy.level == 1


    @pytest.mark.parametrize("mode, level, expected_lives",[(Normal(), 2, 2),
        (Normal(), 4, 4),(Hard(), 5, 7),(Hard(), 6, 8)])
    def test_enemy_lives_happy_path(self,mode, level, expected_lives):
        tenemy = Enemy(mode, level)

        assert tenemy.lives == expected_lives


    @pytest.mark.parametrize("mode, level, expected_lives",[(Normal(), 1, 1),
        (Normal(), 9999, 9999),(Hard(), 1, 3),(Hard(),9997, 9999)])
    def test_enemy_lives_edge_case(self,mode, level, expected_lives):
        tenemy = Enemy(mode, level)

        assert tenemy.lives == expected_lives


    @pytest.mark.parametrize("player_history, expected_attacks",[(settings.PAPER, {settings.SCISSORS, settings.PAPER}),
        (settings.STONE, {settings.PAPER, settings.STONE}),
        (settings.SCISSORS, {settings.STONE, settings.SCISSORS}),])
    def test_select_attack_happy_path(self,player_history, expected_attacks):
        tenemy = Enemy(Hard(), 3)
        tenemy.player_history = player_history
        enemy_attack = tenemy.enemy_select_attack()

        assert enemy_attack in expected_attacks


    def test_select_attack_edge_case(self):
        tenemy = Enemy(Hard(), 3)
        tenemy.player_history = None
        enemy_attack = tenemy.enemy_select_attack()

        assert enemy_attack in {
            settings.PAPER,
            settings.SCISSORS,
            settings.STONE
        }


    @pytest.mark.parametrize("player_history",["snake"])
    def test_select_attack_exception_case(self,player_history):
        tenemy = Enemy(Hard(),5)
        tenemy.player_history = player_history
        
        with pytest.raises(ValueError):
            tenemy.enemy_select_attack()


    @pytest.mark.parametrize("lives,expected_exception",[(1,EnemyDown)])
    def test_enemy_decrease_lives_exception_case(self,lives,expected_exception):
        tenemy = Enemy(Hard(),1)
        tenemy.lives = lives
        with pytest.raises(expected_exception):
            Enemy.enemy_decrease_lives(tenemy)


# <!-------- Game ---------!>
class TestGame:
    @pytest.mark.parametrize("tplayer_attack, tenemy_attack",[(settings.PAPER, settings.PAPER)])
    def test_fight_draw_happy_path(self,tplayer_attack, tenemy_attack):
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
    def test_fight_win_happy_path(self,tplayer_attack,tenemy_attack):
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
    def test_fight_lose_happy_path(self,tplayer_attack,tenemy_attack):
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


    @pytest.mark.parametrize("tplayer_attack, tenemy_attack",[({}, settings.PAPER),(None, settings.STONE),(123, settings.SCISSORS)])
    def test_fight_draw_exception_case_handle_round_type(self,tplayer_attack, tenemy_attack):
        tplayer = Player("test_Andrii")
        tenemy = Enemy(Hard(), 1)
        game = Game(tplayer,tenemy)
       
        with pytest.raises(TypeError):
            game.handle_round_result(tplayer_attack, tenemy_attack)


    @pytest.mark.parametrize("tplayer_attack, tenemy_attack",[("", settings.PAPER),("Snake", settings.STONE),("Oleg", settings.SCISSORS)])
    def test_fight_draw_exception_case_handle_round_value(self,tplayer_attack, tenemy_attack):
        tplayer = Player("test_Andrii")
        tenemy = Enemy(Hard(), 1)
        game = Game(tplayer,tenemy)
       
        with pytest.raises(ValueError):
            game.handle_round_result(tplayer_attack, tenemy_attack)


# <!-------- PlayerRecord ---------!>
class TestPlayerRecord:
    def test_create_player_record_smoke(self):
        tplayer_record = PlayerRecord("Mia", "Normal", 15)
        assert tplayer_record is not None


    def test_create_player_records_exception_case(self):
        with pytest.raises(ValueError):
            records = [
                score.PlayerRecord("B", "Normal", -99),
                score.PlayerRecord("C", "Normal", -9.9),
            ]


    def test_sort_records_happy_path(self):
        records = [
            score.PlayerRecord("A", "Normal", 10),
            score.PlayerRecord("B", "Normal", 5),
            score.PlayerRecord("C", "Normal", 20),
        ]
        records.sort(reverse=True)
        scores = [r.score for r in records]

        assert scores == [20, 10, 5]

    
    def test_sort_records_edge_case(self):
        records = [
            score.PlayerRecord("B", "Normal", 0),
            score.PlayerRecord("C", "Normal", 999),
        ]
        records.sort(reverse=True)
        scores = [r.score for r in records]

        assert scores == [999, 0]    


    def test_eq_records_happy_path(self):
        records = [
            score.PlayerRecord("A", "Normal", 10),
            score.PlayerRecord("A", "Normal", 5),
        ]  

        assert records[0] == records[1]


# <!-------- GameRecord ---------!>
class TestGameRecord:
    def test_add_record_happy_path(self):
        game_record = GameRecord()
        new_record = PlayerRecord("Andrii", "Hard", 6)
        game_record.add_record(new_record)
    
        assert len(game_record.records) == 1
        assert game_record.records[0] == new_record


    def test_add_record_edge_case(self):
        game_record = GameRecord()
        new_record = PlayerRecord("Andrii", "Hard", 6)
        new_record2 = PlayerRecord("Stephan","Normal",3)
        game_record.add_record(new_record)
        game_record.add_record(new_record2)
    
        assert len(game_record.records) == 2
        assert game_record.records == [new_record,new_record2]


    def test_add_record_exception_case(self):
        game_record = GameRecord()

        with pytest.raises(ValueError):
            game_record.add_record("fish")


    def test_change_record_happy_path(self):
        game_record = GameRecord()
        new_record = PlayerRecord("Andrii","Hard",6)
        game_record.add_record(new_record)
        new_record2 = PlayerRecord("Andrii","Hard",10)
        game_record.add_record(new_record2)

        assert len(game_record.records) == 1
        assert game_record.records[0] == new_record2

    def test_change_records_happy_path_high_score(self):
        game_record = GameRecord()
        new_record1 = PlayerRecord("Andrii", "Hard", 6)
        new_record2 = PlayerRecord("Andrii", "Hard", 10)
        new_record3 = PlayerRecord("Andrii", "Hard", 10)

        game_record.add_record(new_record1) 
        game_record.add_record(new_record2)
        game_record.add_record(new_record3)

        assert len(game_record.records) == 1
        assert game_record.records[0] == new_record2


    def test_prepare_records_happy_path(self,monkeypatch):
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


    @pytest.mark.parametrize("limit, expected_limit", [(1000, 999), (1, 0)])
    def test_prepare_records_edge_case(self, monkeypatch, limit, expected_limit):
        monkeypatch.setattr(settings, "MAX_SCORE", expected_limit)
        game_record = GameRecord()
        game_record.records = []
        for i in range(limit):
            game_record.records.append(PlayerRecord("A", "Normal", i + 1))
        game_record.prepare_records()
        scores = [r.score for r in game_record.records]

        assert len(game_record.records) == expected_limit
        assert scores == sorted(scores, reverse=True)


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

