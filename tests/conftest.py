"""
Pytest configuration and fixtures.

Provides common fixtures for all test modules.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.maze_core.models import Cell, Maze, Position


@pytest.fixture
def simple_maze_2x2():
    """
    Fixture: Simple 2x2 maze for testing.

    Layout:
        (0,0) (1,0)
        (0,1) (1,1)

    All cells have walls 0b1010 (N and S blocked, E and W open).
    """
    cells = [
        [Cell(0b1010, 1), Cell(0b1010, 1)],
        [Cell(0b1010, 1), Cell(0b1010, 1)],
    ]
    return Maze(
        width=2,
        height=2,
        cells=cells,
        start=Position(0, 0),
        goal=Position(1, 1),
        seed=42,
    )


@pytest.fixture
def simple_maze_3x3():
    """
    Fixture: Simple 3x3 maze for testing.

    All cells have walls 0b1111 (all passages open).
    """
    cells = [
        [Cell(0b1111, 1), Cell(0b1111, 1), Cell(0b1111, 1)],
        [Cell(0b1111, 1), Cell(0b1111, 1), Cell(0b1111, 1)],
        [Cell(0b1111, 1), Cell(0b1111, 1), Cell(0b1111, 1)],
    ]
    return Maze(
        width=3,
        height=3,
        cells=cells,
        start=Position(0, 0),
        goal=Position(2, 2),
        seed=99,
    )


@pytest.fixture
def blocked_maze_3x3():
    """
    Fixture: 3x3 maze where center is completely isolated.

    All cells have walls 0b0000 (all walls, no passages).
    """
    cells = [
        [Cell(0b0000, 1), Cell(0b0000, 1), Cell(0b0000, 1)],
        [Cell(0b0000, 1), Cell(0b0000, 1), Cell(0b0000, 1)],
        [Cell(0b0000, 1), Cell(0b0000, 1), Cell(0b0000, 1)],
    ]
    return Maze(
        width=3,
        height=3,
        cells=cells,
        start=Position(0, 0),
        goal=Position(2, 2),
        seed=77,
    )
