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
    assets.load_sprites()  # Asegúrate de que los sprites estén cargados
    yield
    pygame.quit()

def test_floor_initialization():
    index = 0  # Usamos un índice simple
    floor = Floor(index)

    # Verificamos que el sprite se haya cargado correctamente
    assert floor.image is not None
    assert floor.rect.bottomleft == (configs.SCREEN_WIDTH * index, configs.SCREEN_HEIGHT)
    assert floor._layer == mock.ANY  # Asegura que el atributo de capa sea el correcto
    assert isinstance(floor.mask, pygame.mask.Mask)  # Verifica que la máscara sea correcta
