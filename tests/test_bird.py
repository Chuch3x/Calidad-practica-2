import pytest
import pygame
from objects.bird import *
from objects.column import *
from objects.floor import *
from assets import *
from unittest import mock
from objects.background import *
import configs

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

@pytest.mark.parametrize(
    "initial_x, expected_x", 
    [
        (-50, -47),
        (49, 52),
        (50, 50)
]
)
def test_update(mock_bird_init, initial_x, expected_x):
    bird = Bird()
    bird.rect.x = initial_x
    initial_y = bird.rect.y
    initial_flap = bird.flap

    bird.update()

    assert bird.rect.x == expected_x
    assert bird.rect.y == initial_y + initial_flap
    assert bird.flap == initial_flap + configs.GRAVITY
    assert bird.image == bird.images[0]
    assert bird.images[0] != mock_bird_init['mock_surface_1']

@pytest.mark.parametrize(
    "sprites, rect_x, rect_y, rect_bottom, expected_output", 
    [
        ([mock.Mock(spec=Column, rect=pygame.Rect(95, 0, 10, 10))], 100, 150, 0, False),
        ([mock.Mock(spec=Background, rect=pygame.Rect(0, 0, 10, 10))], 0, 0, 0, False),
        ([mock.Mock(spec=Column, rect=pygame.Rect(95, 150, 10, 10))], 100, 150, 0, True),
        ([mock.Mock(spec=Column, rect=pygame.Rect(0, 0, 10, 10))], 0, -1, -1, True),
    ]
)
def test_check_collision(sprites, rect_x, rect_y, rect_bottom, expected_output):
    assets.load_sprites()
    bird = Bird()
    # bird.mask = pygame.mask.from_surface(assets.sprites["redbird-midflap"])
    bird.rect = pygame.Rect(rect_x, rect_y, 10, 10)
    bird.rect.bottom = rect_bottom
    # for sprite in sprites:
    #     sprite.mask = pygame.mask.from_surface(assets.sprites["pipe-green"])
    # print(bird.mask, sprite.mask)
    assert bird.check_collision(sprites) == expected_output
