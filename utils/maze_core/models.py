"""
Core data models for the maze search framework.

This module defines all fundamental data structures used throughout the system:
- Direction: Movement directions (NORTH, SOUTH, EAST, WEST)
- Position: Coordinates (x, y)
- Cell: Individual maze cell with walls and cost
- Maze: Complete maze with topology and metadata
- Observation: What the agent perceives each step
- AgentDebugState: Visualization data from agents
- MazeResult: Execution results and metrics
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Set, Optional, Any, Tuple
import json


class Direction(Enum):
    """
    Cardinal directions for movement in the maze.

    Each direction has a delta (dx, dy) for coordinate updates.
    """
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    def opposite(self) -> "Direction":
        """
        Return the opposite direction.

        Returns:
            The opposite direction (e.g., NORTH -> SOUTH).
        """
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]

    @property
    def delta(self) -> Tuple[int, int]:
        """Get coordinate delta (dx, dy) for this direction."""
        return self.value

    def __str__(self) -> str:
        """Return direction name."""
        return self.name


@dataclass
class Position:
    """
    A position in the maze (x, y coordinates).

    Attributes:
        x: Column coordinate (0 = leftmost)
        y: Row coordinate (0 = topmost)
    """
    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        """
        Return new position after moving in given direction.

        Parameters:
            direction: Direction to move (NORTH, SOUTH, EAST, WEST)

        Returns:
            New Position after applying the direction delta.
        """
        dx, dy = direction.delta
        return Position(self.x + dx, self.y + dy)

    def distance_to(self, other: "Position") -> int:
        """
        Calculate Manhattan distance to another position.

        Parameters:
            other: Target position

        Returns:
            Manhattan distance (|x1-x2| + |y1-y2|)
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self) -> int:
        """Allow Position to be used in sets and dicts."""
        return hash((self.x, self.y))

    def __eq__(self, other: Any) -> bool:
        """Compare positions."""
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def to_tuple(self) -> Tuple[int, int]:
        """Convert to (x, y) tuple."""
        return (self.x, self.y)

    def __repr__(self) -> str:
        """String representation."""
        return f"Position({self.x}, {self.y})"


@dataclass
class Cell:
    """
    A single cell in the maze maze.

    Attributes:
        walls: 4-bit integer encoding walls (North, East, South, West).
               Bit value 1 = passage open, 0 = wall present.
               From MSB to LSB: N E S W
        cost: Numeric cost to move into this cell (must be positive).
    """
    walls: int  # 4-bit value: 0b1010 format (N E S W)
    cost: float = 1.0

    def has_wall(self, direction: Direction) -> bool:
        """
        Check if there's a wall in the given direction.

        Parameters:
            direction: Direction to check (NORTH, SOUTH, EAST, WEST)

        Returns:
            True if wall exists, False if passage is open.
        """
        bit_positions = {
            Direction.NORTH: 3,  # MSB
            Direction.EAST: 2,
            Direction.SOUTH: 1,
            Direction.WEST: 0,   # LSB
        }
        bit_pos = bit_positions[direction]
        return not bool((self.walls >> bit_pos) & 1)

    def can_move(self, direction: Direction) -> bool:
        """
        Check if movement is possible in the given direction.

        Parameters:
            direction: Direction to check

        Returns:
            True if passage is open (no wall), False otherwise.
        """
        return not self.has_wall(direction)

    def __repr__(self) -> str:
        """String representation."""
        return f"Cell(walls={self.walls:04b}, cost={self.cost})"


@dataclass
class Maze:
    """
    A complete maze with topology and metadata.

    Attributes:
        width: Number of columns
        height: Number of rows
        cells: 2D grid of Cell objects [y][x]
        start: Starting position
        goal: Goal position
        seed: Random seed for reproducibility
        solution_count: Number of solutions (if known)
    """
    width: int
    height: int
    cells: List[List[Cell]]
    start: Position
    goal: Position
    seed: int
    solution_count: Optional[int] = None

    def get_cell(self, pos: Position) -> Optional[Cell]:
        """
        Get cell at position, or None if out of bounds.

        Parameters:
            pos: Position to retrieve

        Returns:
            Cell at position, or None if out of bounds.
        """
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return self.cells[pos.y][pos.x]
        return None

    def is_valid(self, pos: Position) -> bool:
        """
        Check if position is within maze bounds.

        Parameters:
            pos: Position to check

        Returns:
            True if position is within bounds, False otherwise.
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def can_move_to(self, current: Position, direction: Direction) -> bool:
        """
        Check if movement from current position is valid.

        Parameters:
            current: Current position
            direction: Direction to move

        Returns:
            True if movement is valid (no wall, in bounds), False otherwise.
        """
        current_cell = self.get_cell(current)
        if current_cell is None:
            return False

        if current_cell.has_wall(direction):
            return False

        next_pos = current.move(direction)
        return self.is_valid(next_pos)

    def get_neighbors(self, pos: Position) -> List[Direction]:
        """
        Get all valid movement directions from a position.

        Parameters:
            pos: Current position

        Returns:
            List of directions where movement is possible.
        """
        return [d for d in Direction if self.can_move_to(pos, d)]

    def __repr__(self) -> str:
        """String representation."""
        return f"Maze({self.width}x{self.height}, seed={self.seed})"


@dataclass
class Observation:
    """
    What the agent perceives at each step.

    This is the complete information available to the agent.

    Attributes:
        maze: The maze (full or partial depending on visibility mode)
        current: Agent's current position
        goal: Goal position
        step_count: Number of steps taken so far
        path_cost: Accumulated cost so far
    """
    maze: Maze
    current: Position
    goal: Position
    step_count: int = 0
    path_cost: float = 0.0

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Observation("
            f"pos={self.current}, "
            f"goal={self.goal}, "
            f"steps={self.step_count}, "
            f"cost={self.path_cost})"
        )


@dataclass
class AgentDebugState:
    """
    Optional debug/visualization data from an agent.

    Agents can optionally provide this information for visualization
    of their internal search state (frontier, explored set, etc.).

    Attributes:
        frontier: Cells the algorithm is considering next
        explored: Cells already evaluated
        discovered: Cells discovered (for partial observability)
        current_path: Current path being built
        metadata: Any additional debug information
    """
    frontier: Set[Position] = field(default_factory=set)
    explored: Set[Position] = field(default_factory=set)
    discovered: Set[Position] = field(default_factory=set)
    current_path: List[Position] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AgentDebugState("
            f"frontier={len(self.frontier)}, "
            f"explored={len(self.explored)}, "
            f"discovered={len(self.discovered)}, "
            f"path_len={len(self.current_path)})"
        )


@dataclass
class MazeResult:
    """
    Results and metrics from executing an agent on a maze.

    Attributes:
        solved: Whether goal was reached
        steps: Number of steps taken
        path_cost: Total cost accumulated
        optimal_cost: Optimal cost (from reference solver)
        nodes_explored: Number of cells the agent evaluated
        execution_time_ms: Execution time in milliseconds
        invalid_moves: Number of illegal moves attempted
        maze_seed: Seed of the maze (for reproducibility)
        agent_name: Name of the agent used
        trace: Detailed execution trace (JSON-serializable)
    """
    solved: bool
    steps: int
    path_cost: float
    optimal_cost: float
    nodes_explored: int
    execution_time_ms: float
    invalid_moves: int = 0
    maze_seed: int = 0
    agent_name: str = "unknown"
    trace: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def optimality_ratio(self) -> float:
        """
        Calculate optimality as a ratio (optimal / actual).

        Returns:
            Ratio from 0 to 1 (1.0 = optimal, < 1.0 = suboptimal).
            Returns 0.0 if not solved.
        """
        if not self.solved or self.path_cost == 0:
            return 0.0
        return self.optimal_cost / self.path_cost

    @property
    def optimality_percentage(self) -> float:
        """
        Calculate optimality as a percentage.

        Returns:
            Percentage from 0% to 100% (100% = optimal).
        """
        return self.optimality_ratio * 100

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert results to dictionary (JSON-serializable).

        Returns:
            Dictionary representation of results.
        """
        return {
            "solved": self.solved,
            "steps": self.steps,
            "path_cost": self.path_cost,
            "optimal_cost": self.optimal_cost,
            "optimality_ratio": self.optimality_ratio,
            "optimality_percentage": self.optimality_percentage,
            "nodes_explored": self.nodes_explored,
            "execution_time_ms": self.execution_time_ms,
            "invalid_moves": self.invalid_moves,
            "maze_seed": self.maze_seed,
            "agent_name": self.agent_name,
        }

    def to_json(self) -> str:
        """
        Serialize results to JSON string.

        Returns:
            JSON string representation.
        """
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.solved else "FAILED"
        return (
            f"MazeResult("
            f"{status}, "
            f"steps={self.steps}, "
            f"cost={self.path_cost:.1f}, "
            f"optimal={self.optimal_cost:.1f}, "
            f"ratio={self.optimality_percentage:.1f}%)"
        )
