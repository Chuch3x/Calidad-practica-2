import pytest
import pygame
from objects.bird import *
from assets import *
from unittest import mock

@pytest.fixture
def mock_bird_init():
    mock_surface_1 = mock.Mock(spec=pygame.Surface)
    mock_surface_2 = mock.Mock(spec=pygame.Surface)
    mock_surface_3 = mock.Mock(spec=pygame.Surface)

    mock_surface_1.get_rect.return_value = pygame.Rect(-50, 50, 100, 100)
    mock_surface_2.get_rect.return_value = pygame.Rect(-50, 50, 100, 100)
    mock_surface_3.get_rect.return_value = pygame.Rect(-50, 50, 100, 100)

    with mock.patch('assets.get_sprite') as mock_get_sprite, \
         mock.patch('pygame.mask.from_surface') as mock_from_surface, \
         mock.patch('assets.play_audio') as mock_play_audio:

        mock_get_sprite.side_effect = [mock_surface_1, mock_surface_2, mock_surface_3]
        mock_from_surface.return_value = 'mock_mask'

        yield {
            'mock_get_sprite': mock_get_sprite,
            'mock_from_surface': mock_from_surface,
            'mock_surface_1': mock_surface_1,
            'mock_surface_2': mock_surface_2,
            'mock_surface_3': mock_surface_3,
            'mock_play_audio': mock_play_audio
        }

def test_bird_init(mock_bird_init):
    mock_get_sprite = mock_bird_init['mock_get_sprite']
    mock_from_surface = mock_bird_init['mock_from_surface']
    mock_surface_1 = mock_bird_init['mock_surface_1']
    mock_surface_2 = mock_bird_init['mock_surface_2']
    mock_surface_3 = mock_bird_init['mock_surface_3']

    bird = Bird()

    assert bird._layer == Layer.PLAYER
    assert bird.images == [mock_surface_1, mock_surface_2, mock_surface_3]
    assert bird.image == mock_surface_1
    assert bird.rect.topleft == (-50, 50)
    assert bird.mask == 'mock_mask'
    assert bird.flap == 0
    assert mock_get_sprite.call_count == 3

@pytest.mark.parametrize(
    "event, expected_output", 
    [
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE), -6),
        (pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE), 0)
    ]
)
def test_handle_event(mock_bird_init, event, expected_output):
    bird = Bird()
    bird.handle_event(event)
    assert bird.flap == expected_output



