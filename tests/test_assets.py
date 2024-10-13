import os
import sys
import pytest
from unittest import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from assets import load_sprites, get_sprite, sprites

# Fixture para simular pygame.image.load
@pytest.fixture
def mock_pygame():
    with mock.patch("pygame.image.load") as mock_load:
        mock_load.side_effect = lambda x: f"MockedImage({x})"  # Simula la carga de imágenes
        yield mock_load

# Fixture para simular os.listdir
@pytest.fixture
def mock_os_listdir():
    with mock.patch("os.listdir") as mock_listdir:
        # Simula que hay tres imágenes en el directorio
        mock_listdir.return_value = ["0.png", "1.png", "2.png"]
        yield mock_listdir

def test_get_sprite(mock_pygame, mock_os_listdir):
    load_sprites()
    assert get_sprite("0") == "MockedImage(assets/sprites/0.png)"
