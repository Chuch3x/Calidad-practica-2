import pygame
import pytest
from layer import Layer
from objects.score import * 
from unittest import mock
import assets

@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_score_initialization(setup_pygame):
    score = Score()
    assert score.value == 0
    assert score.image is not None

def test_score_update(setup_pygame):
    score = Score()
    with mock.patch.object(score, '_Score__create') as mock_create:
        score.update()
        mock_create.assert_called_once()

@pytest.mark.parametrize(
    "value, expected_str_value, expected_images_count",
    [
        (0, "0", 1),
        (1, "1", 1),
        (123, "123", 3),
    ]
)
def test_create(value, expected_str_value, expected_images_count):
    score = Score()
    score.value = value
    score._Score__create()
    assert score.str_value == expected_str_value
    assert len(score.images) == expected_images_count

def test_create_with_empty_string():
    score = Score()
    score.value = None
    with pytest.raises(KeyError, match="N"):
        score._Score__create()