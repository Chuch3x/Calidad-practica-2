from objects.gameover_message import *
from objects.gamestart_message import *
import assets
from layer import Layer

def test_gameover_init():
    game_over = GameOverMessage()
    assert game_over._layer is Layer.UI
    assert game_over.image is not None

def test_gamestart_init():
    game_start = GameStartMessage()
    assert game_start._layer is Layer.UI
    assert game_start.image is not None