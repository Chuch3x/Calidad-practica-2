from objects.background import *
import pytest
import pygame
import assets
from layer import Layer
from unittest.mock import patch
import configs

@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

@patch('assets.get_sprite')
def test_background_init(mock_get_sprite, setup_pygame):
    mock_get_sprite.return_value = pygame.Surface((100, 100))
    index = 0
    background = Background(index)

    assert background._layer == Layer.BACKGROUND
    assert background.image is not None
    assert background.rect.topleft == (configs.SCREEN_WIDTH * index, 0)

@pytest.mark.parametrize("rect_right, expected_rect_x",
[
    (0, configs.SCREEN_WIDTH), 
    (1, configs.SCREEN_WIDTH)
]
)
@patch('assets.get_sprite')
def test_update(mock_get_sprite, rect_right, expected_rect_x):
    mock_surface = pygame.Surface((100, 100))
    mock_get_sprite.return_value = mock_surface
    index = 0
    background = Background(index)
    background.rect.right = rect_right
    background.update()
    assert background.rect.x == expected_rect_x

