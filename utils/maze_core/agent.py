"""Agent base class and interface."""

from abc import ABC, abstractmethod
from typing import Optional

from .models import Direction, Observation, AgentDebugState


class Agent(ABC):
    """
    Base class for maze-solving agents.

    Students must implement step() method.
    Agents maintain persistent state between calls.
    """

    @abstractmethod
    def step(self, observation: Observation) -> Direction:
        """
        Decide next move based on current observation.

        Parameters:
            observation: Current state (maze, position, goal, metrics)

        Returns:
            Direction to move (NORTH, SOUTH, EAST, WEST)

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass

    def debug_state(self) -> Optional[AgentDebugState]:
        """
        Optional: return visualization/debug data.

        Override to provide frontier, explored, discovered data
        for visualization.

        Returns:
            AgentDebugState or None if not visualizable
        """
        return None
