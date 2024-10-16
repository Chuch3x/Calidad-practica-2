import os
import sys
import pytest
from unittest import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from assets import *


@pytest.fixture
def mock_pygame():
    with mock.patch("pygame.image.load") as mock_load:
        mock_load.side_effect = lambda x: f"MockedImage({x})"
        yield mock_load

@pytest.fixture
def mock_pygame_sound():
    with mock.patch("pygame.mixer.Sound") as mock_sound:
        mock_sound.side_effect = lambda x: mock.MagicMock()
        yield mock_sound

@pytest.fixture
def mock_os_listdir():
    with mock.patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ["0.png", "1.png", "2.png"]
        yield mock_listdir
        
def test_load_sprites(mock_pygame, mock_os_listdir):
    load_sprites()
    assert "0" in sprites
    assert "1" in sprites
    expected_path = os.path.join("assets", "sprites", "0.png")
    assert sprites["0"] == f"MockedImage({expected_path})"
    expected_path = os.path.join("assets", "sprites", "1.png")
    assert sprites["1"] == f"MockedImage({expected_path})"

def test_get_sprite(mock_pygame, mock_os_listdir):
    load_sprites()
    expected_path = os.path.join("assets", "sprites", "0.png")
    assert get_sprite("0") == f"MockedImage({expected_path})"

def test_get_sprite_not_found():
    sprites.clear()
    with pytest.raises(KeyError):
        get_sprite("non_existent_sprite")

def test_load_audios(mock_pygame_sound, mock_os_listdir):
    mock_os_listdir.return_value = ["audio1.wav", "audio2.mp3"]
    load_audios()
    assert "audio1" in audios
    assert "audio2" in audios
    assert isinstance(audios["audio1"], mock.MagicMock)
    assert isinstance(audios["audio2"], mock.MagicMock)

def test_play_audio():
    audios.clear()
    mock_audio = mock.MagicMock()
    audios["test_audio"] = mock_audio
    play_audio("test_audio")
    mock_audio.play.assert_called_once()

def test_play_audio_not_found():
    audios.clear()
    with pytest.raises(KeyError):
        play_audio("non_existent_audio")
