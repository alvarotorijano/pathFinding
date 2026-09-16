"""
Maze Search Algorithms - Core Data Models and Utilities

This module provides the fundamental data structures and algorithms
for the maze search framework.

Note: The reference solver is compiled to WASM and loaded at runtime
from the labyrinth-solver-wasm private repository. Python source code
for the solver is not available in this repository.
"""

from .models import (
    Direction,
    Position,
    Cell,
    Maze,
    Observation,
    AgentDebugState,
    MazeResult,
)

__all__ = [
    "Direction",
    "Position",
    "Cell",
    "Maze",
    "Observation",
    "AgentDebugState",
    "MazeResult",
]

__version__ = "1.0.0"
