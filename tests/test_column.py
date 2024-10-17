import os
import sys
import pytest
import pygame
from unittest import mock
from unittest.mock import patch
import assets
import configs
from objects.column import *

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
    mock_sprite = pygame.Surface((50, 100)) 
    with mock.patch('assets.get_sprite', return_value=mock_sprite):
        yield  

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

def test_column_update_moves_column(mock_assets):
    column = Column()
    column.rect.x = 100 
    column.update()
    assert column.rect.x == 98

def test_column_update_kills_column(mock_assets):
    column = Column()
    column.rect.x = -1 
    column.update()
    assert column.alive() is False 

def test_is_passed_when_column_passes_limit(mock_assets):
    column = Column()
    column.rect.x = 49 
    assert column.is_passed() is True
    assert column.passed is True 

def test_is_passed_when_column_does_not_pass_limit(mock_assets):
    column = Column()
    column.rect.x = 51  
    assert column.is_passed() is False
    assert column.passed is False 
