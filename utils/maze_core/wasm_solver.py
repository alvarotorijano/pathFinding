"""
WASM Reference Solver - Wrapper for compiled A* algorithm.

This module loads the compiled WASM solver (from labyrinth-solver-wasm repo).
Students cannot see or modify this - it's a black box for evaluation.
"""

from typing import List, Tuple
import sys
import os

# Try to import WASM module
try:
    # When WASM is built and installed, import it
    import labyrinth_solver_wasm as wasm_solver
    WASM_AVAILABLE = True
except ImportError:
    WASM_AVAILABLE = False
    wasm_solver = None


def solve_maze(
    width: int,
    height: int,
    start_x: int,
    start_y: int,
    goal_x: int,
    goal_y: int,
    walls: List[int],
    costs: List[float],
) -> Tuple[bool, List[Tuple[int, int]], float, int]:
    """
    Solve maze using reference solver (WASM).

    Parameters:
        width: Maze width
        height: Maze height
        start_x, start_y: Start position
        goal_x, goal_y: Goal position
        walls: List of 4-bit wall values per cell
        costs: List of costs per cell

    Returns:
        (solved, path, cost, nodes_expanded)

    Note:
        This calls the compiled WASM solver from labyrinth-solver-wasm.
        Source code is private and not available in this repository.
    """
    if not WASM_AVAILABLE:
        raise RuntimeError(
            "WASM solver not available. "
            "Install labyrinth-solver-wasm from private repository."
        )

    result = wasm_solver.solve_maze(
        width, height,
        start_x, start_y,
        goal_x, goal_y,
        walls, costs
    )

    return (
        result.solved,
        result.path,
        result.cost,
        result.nodes_expanded
    )
