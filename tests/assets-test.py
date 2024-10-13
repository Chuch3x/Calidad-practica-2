import os
import sys
import pytest
from unittest import mock
import pygame
# Añade el directorio superior al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Luego puedes importar
from assets import load_sprites, sprites

@pytest.fixture
def mock_pygame():
    with mock.patch("pygame.image.load") as mock_load:
        mock_load.side_effect = lambda x: f"MockedImage({x})"
        yield mock_load

@pytest.fixture
def mock_os_listdir():
    with mock.patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ["sprite1.png", "sprite2.png"]
        yield mock_listdir

def test_load_sprites(mock_pygame, mock_os_listdir):
    # Llamamos a la función que vamos a probar
    load_sprites()

    # Comprobamos que las imágenes fueron cargadas y almacenadas en el diccionario "sprites"
    assert sprites["sprite1"] == "MockedImage(assets/sprites/sprite1.png)"
    assert sprites["sprite2"] == "MockedImage(assets/sprites/sprite2.png)"
    
    # Verificamos que se llamaron las funciones correctamente
    mock_os_listdir.assert_called_once_with(os.path.join("assets", "sprites"))
    mock_pygame.assert_any_call(os.path.join("assets", "sprites", "sprite1.png"))
    mock_pygame.assert_any_call(os.path.join("assets", "sprites", "sprite2.png"))
