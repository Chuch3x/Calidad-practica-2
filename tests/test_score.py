import pygame
import pytest
from layer import Layer
from objects.score import * 


@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_score_initialization(setup_pygame):
    score = Score()
    assert score.value == 0
    assert score.image is not None