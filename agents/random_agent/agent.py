"""Random agent - baseline that moves randomly."""

import random
from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation


class RandomAgent(Agent):
    """
    Baseline agent that moves randomly.

    This agent picks a random valid direction at each step. Use this as
    a baseline to compare your algorithms against.
    """

    def step(self, observation: Observation) -> Direction:
        """
        Choose a random valid direction.

        Parameters:
            observation: Current maze state with position and goal

        Returns:
            Direction: A random valid direction to move
        """
        # Get all passable neighbors from the maze
        valid_moves = observation.maze.get_neighbors(observation.current)

        # If stuck (no valid moves), return any direction (will be rejected)
        if not valid_moves:
            return Direction.NORTH

        # Return random valid move
        return random.choice(valid_moves)
