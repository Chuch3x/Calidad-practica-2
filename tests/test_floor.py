import os
import sys
import pytest
import pygame
from unittest import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from objects.floor import Floor
import configs
import assets

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    assets.load_sprites()
    yield
    pygame.quit()

def test_floor_initialization():
    index = 0  # Usamos un índice simple
    floor = Floor(index)
    assert floor.image is not None
    assert floor.rect.bottomleft == (configs.SCREEN_WIDTH * index, configs.SCREEN_HEIGHT)
    assert floor._layer == mock.ANY
    assert isinstance(floor.mask, pygame.mask.Mask)

def test_floor_update_moves_left():
    index = 0
    floor = Floor(index)
    initial_x = floor.rect.x

    # Llamar a update debería mover el floor hacia la izquierda en 2 unidades
    floor.update()
    assert floor.rect.x == initial_x - 2, "El suelo no se movió correctamente hacia la izquierda"

def test_floor_repositions_when_out_of_screen():
    index = 0
    floor = Floor(index)

    # Colocar el rect en una posición donde se salga completamente de la pantalla
    floor.rect.right = 0  # Simulando que justo sale de la pantalla

    # Llamar a update debería reposicionar el floor
    floor.update()
    assert floor.rect.x == configs.SCREEN_WIDTH, "El suelo no se reposicionó correctamente cuando salió de la pantalla"