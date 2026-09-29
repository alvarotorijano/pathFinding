"""A* (A-star) agent - STUDENT TEMPLATE.

Fill in the "YOUR CODE GOES HERE" block inside step(): that is the search
itself. Everything else (reading the maze, following the already-computed
path) is already implemented, using the same structure as the DFS example
in agents/dfs_agent/agent.py.
"""

from typing import Optional

from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation, Position, AgentDebugState


class AStarAgent(Agent):
    """
    A* search agent.

    Expands the frontier node with lowest f(n) = g(n) + h(n). Like the DFS
    example, it only needs to search once per maze: self.path then holds the
    full route and later calls just follow it.
    """

    def __init__(self):
        """Initialize A* state."""
        self.frontier = []      # list of candidate positions
        self.explored = set()
        self.parent = {}
        self.g_score = {}
        self.goal = None
        self.maze = None
        self.path = []
        self.path_index = 0

    def step(self, observation: Observation) -> Direction:
        """
        Execute one A* step.

        Parameters:
            observation: Current maze state

        Returns:
            Next direction to move
        """
        if self.maze != id(observation.maze):
            # New maze, initialize search
            self.maze = id(observation.maze)
            self.goal = observation.goal
            start = observation.current
            self.frontier = [start]
            self.explored = set()
            self.parent = {start: None}
            self.g_score = {start: 0.0}
            self.path = [start]
            self.path_index = 0

        # Follow computed path if available
        if self.path_index + 1 < len(self.path):
            current = self.path[self.path_index]
            next_pos = self.path[self.path_index + 1]
            self.path_index += 1

            # Find direction to next position
            for direction in observation.maze.get_neighbors(current):
                if current.move(direction) == next_pos:
                    return direction

        # ------------------------------------------------------------------
        # YOUR CODE GOES HERE
        # ------------------------------------------------------------------

        # No solution found, return random valid move
        neighbors = observation.maze.get_neighbors(observation.current)
        return neighbors[0] if neighbors else Direction.NORTH

    @staticmethod
    def _heuristic(position: Position, goal: Position) -> float:
        """
        Admissible heuristic: Manhattan distance to the goal.

        Already implemented, no need to change it.

        Parameters:
            position: Position to estimate the remaining cost from.
            goal: Goal position.

        Returns:
            Manhattan distance between `position` and `goal`.
        """
        return float(position.distance_to(goal))

    def debug_state(self) -> Optional[AgentDebugState]:
        """Return visualization data."""
        return AgentDebugState(
            frontier=set(self.frontier),
            explored=self.explored,
            current_path=self.path,
        )
