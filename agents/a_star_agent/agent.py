"""A* (A-star) agent - Complete implementation."""

from typing import Optional, List

from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation, Position, AgentDebugState, Maze


class AStarAgent(Agent):
    """
    A* search agent.

    Expands the frontier node with lowest f(n) = g(n) + h(n).
    Complete search runs on first step(), then follows computed path.
    """

    def __init__(self):
        """Initialize A* state."""
        self.frontier = []          # list of tuples: (f_score, Position)
        self.explored = set()       # set of explored positions
        self.parent = {}            # position -> parent position
        self.g_score = {}           # position -> actual cost
        self.goal = None
        self.maze = None
        self.path = []              # final computed path (list of Positions)
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
            # New maze, initialize and run complete A* search
            self.maze = id(observation.maze)
            self.goal = observation.goal
            start = observation.current

            # Initialize A* data structures
            self.frontier = []
            self.explored = {start}
            self.parent = {start: None}
            self.g_score = {start: 0.0}
            self.path = [start]
            self.path_index = 0

            # Add start to frontier
            f_start = self.g_score[start] + self._heuristic(start, self.goal)
            self.frontier.append((f_start, start))

            # Run complete A* search
            while self.frontier:
                # Find best node (minimum f)
                best_idx = 0
                best_f = self.frontier[0][0]
                for i, (f, pos) in enumerate(self.frontier):
                    if f < best_f:
                        best_f = f
                        best_idx = i

                f_current, current = self.frontier.pop(best_idx)

                # Check if goal found
                if current == self.goal:
                    # Reconstruct path
                    self.path = []
                    node = self.goal
                    while node is not None:
                        self.path.append(node)
                        node = self.parent.get(node)
                    self.path.reverse()
                    self.path_index = 1

                    # Return first move
                    if len(self.path) > 1:
                        for d in observation.maze.get_neighbors(self.path[0]):
                            if self.path[0].move(d) == self.path[1]:
                                return d
                    return Direction.NORTH

                # Examine neighbors
                for direction in observation.maze.get_neighbors(current):
                    neighbor = current.move(direction)

                    # Skip if already explored
                    if neighbor in self.explored:
                        continue

                    # Calculate provisional g
                    neighbor_cell = observation.maze.get_cell(neighbor)
                    g_provisional = self.g_score[current] + neighbor_cell.cost

                    # New neighbor
                    if neighbor not in self.g_score:
                        h_neighbor = self._heuristic(neighbor, self.goal)
                        f_neighbor = g_provisional + h_neighbor

                        self.frontier.append((f_neighbor, neighbor))
                        self.g_score[neighbor] = g_provisional
                        self.parent[neighbor] = current
                        self.explored.add(neighbor)

                    # Better path to existing neighbor
                    elif g_provisional < self.g_score[neighbor]:
                        h_neighbor = self._heuristic(neighbor, self.goal)
                        f_neighbor = g_provisional + h_neighbor

                        self.frontier.append((f_neighbor, neighbor))
                        self.g_score[neighbor] = g_provisional
                        self.parent[neighbor] = current

            # No path found
            self.path = []
            neighbors = observation.maze.get_neighbors(observation.current)
            return neighbors[0] if neighbors else Direction.NORTH

        # Follow computed path if available
        if self.path_index + 1 < len(self.path):
            current = self.path[self.path_index]
            next_pos = self.path[self.path_index + 1]
            self.path_index += 1

            # Find direction to next position
            for direction in observation.maze.get_neighbors(current):
                if current.move(direction) == next_pos:
                    return direction

        # No solution found, return random valid move
        neighbors = observation.maze.get_neighbors(observation.current)
        return neighbors[0] if neighbors else Direction.NORTH

    @staticmethod
    def _heuristic(position: Position, goal: Position) -> float:
        """
        Admissible heuristic: Manhattan distance to the goal.

        Parameters:
            position: Position to estimate the remaining cost from.
            goal: Goal position.

        Returns:
            Manhattan distance between position and goal.
        """
        dx = abs(position.x - goal.x)
        dy = abs(position.y - goal.y)
        return float(dx + dy)

    def debug_state(self) -> Optional[AgentDebugState]:
        """Return visualization data."""
        frontier_positions = {pos for f, pos in self.frontier}
        return AgentDebugState(
            frontier=frontier_positions,
            explored=self.explored,
            current_path=self.path,
        )
