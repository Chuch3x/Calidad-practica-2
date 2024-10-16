import os
import sys
import pytest
import pygame
from unittest import mock
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import assets
import configs
from objects.column import Column

# Inicializar Pygame
@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# Mock para evitar la inicialización real de Pygame
@pytest.fixture(autouse=True)
def mock_pygame():
    with mock.patch('pygame.sprite.Sprite') as mock_sprite:
        yield mock_sprite

@pytest.fixture
def mock_assets():
    with mock.patch('assets.get_sprite') as mock_get_sprite:
        mock_sprite = pygame.Surface((50, 100))  
        mock_get_sprite.return_value = mock_sprite
        yield mock_get_sprite
# UNIT TESTS
@patch('random.uniform')
def test_column_initialization(mock_uniform, mock_pygame, mock_assets):
    mock_uniform.return_value = 150  

    column = Column()

    # Verificar que los atributos clave están inicializados
    assert column.gap == 100
    assert column.passed is False
    assert column.pipe_bottom_rect.topleft == (0, 200)  

    assert column.mask is not None
    assert isinstance(column.mask, pygame.mask.Mask)

    sprite_floor_height = assets.get_sprite("floor").get_rect().height
    assert column.rect.midleft[0] == configs.SCREEN_WIDTH
    assert column.rect.midleft[1] == 150
    assert column.rect.midleft[1] >= 100
    assert column.rect.midleft[1] <= configs.SCREEN_HEIGHT - sprite_floor_height - 100