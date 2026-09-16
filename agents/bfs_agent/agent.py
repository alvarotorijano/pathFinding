"""BFS (Breadth-First Search) example agent."""

from collections import deque
from typing import Dict, Set, List, Optional

from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation, Position, AgentDebugState


class BFSAgent(Agent):
    """
    Breadth-First Search agent.

    Expands nodes level-by-level. Optimal for uniform costs.
    """

    def __init__(self):
        """Initialize BFS state."""
        self.frontier = deque()
        self.explored = set()
        self.parent = {}
        self.goal = None
        self.maze = None
        self.path = []
        self.path_index = 0

    def step(self, observation: Observation) -> Direction:
        """
        Execute one BFS step.

        Parameters:
            observation: Current maze state

        Returns:
            Next direction to move
        """
        if self.maze != id(observation.maze):
            # New maze, initialize search
            self.maze = id(observation.maze)
            self.goal = observation.goal
            self.frontier = deque([observation.current])
            self.explored = {observation.current}
            self.parent = {observation.current: None}
            self.path = [observation.current]
            self.path_index = 0

        # Follow computed path if available
        if self.path_index + 1 < len(self.path):
            self.path_index += 1
            current = self.path[self.path_index - 1]
            next_pos = self.path[self.path_index]

            # Find direction to next position
            for direction in observation.maze.get_neighbors(current):
                if current.move(direction) == next_pos:
                    return direction

        # Expand frontier if path not found yet
        if self.frontier:
            current = self.frontier.popleft()

            for direction in observation.maze.get_neighbors(current):
                neighbor = current.move(direction)

                if neighbor not in self.explored:
                    self.explored.add(neighbor)
                    self.parent[neighbor] = current

                    if neighbor == self.goal:
                        # Reconstruct path
                        self.path = []
                        node = self.goal
                        while node is not None:
                            self.path.append(node)
                            node = self.parent.get(node)
                        self.path.reverse()
                        self.path_index = 0

                        # Return first move
                        for d in observation.maze.get_neighbors(self.path[0]):
                            if self.path[0].move(d) == self.path[1]:
                                return d

                    self.frontier.append(neighbor)

        # No solution found, return random valid move
        neighbors = observation.maze.get_neighbors(observation.current)
        return neighbors[0] if neighbors else Direction.NORTH

    def debug_state(self) -> Optional[AgentDebugState]:
        """Return visualization data."""
        return AgentDebugState(
            frontier=set(self.frontier),
            explored=self.explored,
            current_path=self.path,
        )
