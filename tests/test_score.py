import pygame
import pytest
from layer import Layer
from objects.score import * 
from unittest import mock

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