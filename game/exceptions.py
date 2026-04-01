class GameException(Exception):
    """Base class for all game exceptions"""
    pass

class GameOver(GameException):
    """Raised when player has no lives left"""
    pass

class EnemyDown(GameException):
    """Raised when enemy has no lives left"""
    pass
class PlayerExit(GameException):
    """Raised when player exit"""
    pass
