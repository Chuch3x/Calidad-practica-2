import pygame
import pytest
from main import create_sprites
from objects.background import Background
from objects.floor import Floor
from objects.bird import Bird
from objects.gamestart_message import GameStartMessage
from objects.score import Score

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_create_sprites():
    # Crear y obtener los sprites desde la función create_sprites
    bird, game_start_message, score = create_sprites()

    # Verificar que se crearon los objetos Bird, GameStartMessage y Score
    assert isinstance(bird, Bird), "Bird no se creó correctamente"
    assert isinstance(game_start_message, GameStartMessage), "GameStartMessage no se creó correctamente"
    assert isinstance(score, Score), "Score no se creó correctamente"