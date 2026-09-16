"""
Maze generation algorithms and configuration.

This module provides maze generation with different topologies
and cost maps, independent of external maze libraries.
"""

from enum import Enum
from typing import List, Tuple, Set, Optional
import random

from .models import Cell, Maze, Position, Direction


class TopologyType(Enum):
    """
    Maze topology types.

    Attributes:
        PERFECT: Exactly one path between any two cells (tree structure)
        MULTIPLE: Multiple paths between some cells (has cycles)
        UNSOLVABLE: No path from start to goal
        CORRIDOR: Single linear path with no branches
        OPEN: Fully connected maze (all passages open)
    """
    PERFECT = "perfect"
    MULTIPLE = "multiple"
    UNSOLVABLE = "unsolvable"
    CORRIDOR = "corridor"
    OPEN = "open"


class CostMapType(Enum):
    """
    Cell cost distribution types.

    Attributes:
        UNIFORM: All cells have cost 1.0
        RANDOM: Each cell has random cost in range
        HEATMAP: Smooth cost gradient from center/edges
    """
    UNIFORM = "uniform"
    RANDOM = "random"
    HEATMAP = "heatmap"


class MazeGenerator:
    """
    Generate mazes with configurable topology and cost maps.

    This is a standalone implementation that doesn't depend on
    external maze libraries, ensuring Python version compatibility.
    """

    def __init__(self, width: int, height: int, seed: int):
        """
        Initialize maze generator.

        Parameters:
            width: Maze width (number of columns)
            height: Maze height (number of rows)
            seed: Random seed for reproducibility
        """
        if width < 1 or height < 1:
            raise ValueError("Maze dimensions must be >= 1")

        self.width = width
        self.height = height
        self.seed = seed
        self.rng = random.Random(seed)

    def generate(
        self,
        topology: TopologyType = TopologyType.PERFECT,
        cost_map: CostMapType = CostMapType.UNIFORM,
        cost_range: Tuple[int, int] = (1, 1),
        start: Optional[Position] = None,
        goal: Optional[Position] = None,
    ) -> Maze:
        """
        Generate a maze.

        Parameters:
            topology: Type of maze (PERFECT, MULTIPLE, UNSOLVABLE, etc.)
            cost_map: How to distribute cell costs
            cost_range: (min_cost, max_cost) for cost generation
            start: Starting position (default: (0, 0))
            goal: Goal position (default: (width-1, height-1))

        Returns:
            Generated Maze object

        Raises:
            ValueError: If parameters are invalid
        """
        if cost_range[0] < 1 or cost_range[1] < cost_range[0]:
            raise ValueError("Cost range must be positive")

        # Generate topology (walls)
        cells = self._generate_topology(topology)

        # Generate costs
        self._apply_cost_map(cells, cost_map, cost_range)

        # Default positions
        if start is None:
            start = Position(0, 0)
        if goal is None:
            goal = Position(self.width - 1, self.height - 1)

        # Validate positions
        if not (0 <= start.x < self.width and 0 <= start.y < self.height):
            raise ValueError(f"Start position {start} out of bounds")
        if not (0 <= goal.x < self.width and 0 <= goal.y < self.height):
            raise ValueError(f"Goal position {goal} out of bounds")

        # Count solutions if possible
        solution_count = None
        if topology == TopologyType.PERFECT:
            solution_count = 1
        elif topology == TopologyType.UNSOLVABLE:
            solution_count = 0

        return Maze(
            width=self.width,
            height=self.height,
            cells=cells,
            start=start,
            goal=goal,
            seed=self.seed,
            solution_count=solution_count,
        )

    def _generate_topology(self, topology: TopologyType) -> List[List[Cell]]:
        """
        Generate maze topology (walls).

        Parameters:
            topology: Type of topology to generate

        Returns:
            2D grid of Cell objects with walls set
        """
        if topology == TopologyType.PERFECT:
            return self._generate_perfect()
        elif topology == TopologyType.MULTIPLE:
            return self._generate_multiple()
        elif topology == TopologyType.UNSOLVABLE:
            return self._generate_unsolvable()
        elif topology == TopologyType.CORRIDOR:
            return self._generate_corridor()
        elif topology == TopologyType.OPEN:
            return self._generate_open()
        else:
            raise ValueError(f"Unknown topology: {topology}")

    def _generate_perfect(self) -> List[List[Cell]]:
        """
        Generate perfect maze (one path between any two cells).

        Uses depth-first search (DFS) maze generation algorithm.
        """
        # Start with all walls
        cells = [[Cell(walls=0b0000, cost=1.0) for _ in range(self.width)]
                 for _ in range(self.height)]

        visited = set()
        stack = [Position(0, 0)]
        visited.add((0, 0))

        while stack:
            current = stack[-1]

            # Get unvisited neighbors
            neighbors = []
            for direction in [Direction.NORTH, Direction.SOUTH,
                            Direction.EAST, Direction.WEST]:
                next_pos = current.move(direction)
                if (0 <= next_pos.x < self.width and
                    0 <= next_pos.y < self.height and
                    (next_pos.x, next_pos.y) not in visited):
                    neighbors.append((next_pos, direction))

            if neighbors:
                # Pick random neighbor and carve passage
                next_pos, direction = self.rng.choice(neighbors)
                visited.add((next_pos.x, next_pos.y))

                # Carve passage in both cells
                self._carve_passage(cells, current, next_pos, direction)

                stack.append(next_pos)
            else:
                stack.pop()

        return cells

    def _generate_multiple(self) -> List[List[Cell]]:
        """
        Generate maze with multiple paths.

        Starts with perfect maze, then adds random passages.
        """
        cells = self._generate_perfect()

        # Add random passages to create cycles
        num_passages = max(1, (self.width * self.height) // 8)
        for _ in range(num_passages):
            x = self.rng.randint(0, self.width - 1)
            y = self.rng.randint(0, self.height - 1)
            direction = self.rng.choice(list(Direction))

            next_x = x + direction.delta[0]
            next_y = y + direction.delta[1]

            if 0 <= next_x < self.width and 0 <= next_y < self.height:
                self._carve_passage(
                    cells, Position(x, y), Position(next_x, next_y), direction
                )

        return cells

    def _generate_unsolvable(self) -> List[List[Cell]]:
        """
        Generate unsolvable maze (no path from start to goal).

        Creates two separate regions with no connection.
        """
        cells = [[Cell(walls=0b0000, cost=1.0) for _ in range(self.width)]
                 for _ in range(self.height)]

        # Create vertical wall down the middle
        mid_x = self.width // 2
        for y in range(self.height):
            cell = cells[y][mid_x]
            # Block EAST passage on left side
            cell.walls = cell.walls & ~(1 << 2)  # Clear EAST bit

        return cells

    def _generate_corridor(self) -> List[List[Cell]]:
        """
        Generate single corridor (linear path).

        One long winding path, no branches.
        """
        cells = [[Cell(walls=0b0000, cost=1.0) for _ in range(self.width)]
                 for _ in range(self.height)]

        # Create a random path from (0,0) to (width-1, height-1)
        x, y = 0, 0
        visited = {(0, 0)}

        while (x, y) != (self.width - 1, self.height - 1):
            # Only allow moves toward goal area
            possible = []
            if x < self.width - 1:
                possible.append((x + 1, y, Direction.EAST))
            if y < self.height - 1:
                possible.append((x, y + 1, Direction.SOUTH))
            if x > 0 and (x - 1, y) not in visited:
                possible.append((x - 1, y, Direction.WEST))
            if y > 0 and (x, y - 1) not in visited:
                possible.append((x, y - 1, Direction.NORTH))

            if possible:
                x, y, direction = self.rng.choice(possible)
                visited.add((x, y))

                # Carve from previous to here
                prev_x = x - direction.delta[0]
                prev_y = y - direction.delta[1]
                self._carve_passage(
                    cells, Position(prev_x, prev_y), Position(x, y), direction
                )

        return cells

    def _generate_open(self) -> List[List[Cell]]:
        """
        Generate fully open maze (all passages available).
        """
        return [[Cell(walls=0b1111, cost=1.0) for _ in range(self.width)]
                for _ in range(self.height)]

    def _carve_passage(
        self,
        cells: List[List[Cell]],
        from_pos: Position,
        to_pos: Position,
        direction: Direction,
    ) -> None:
        """
        Carve a passage between two cells.

        Parameters:
            cells: Maze grid
            from_pos: Starting position
            to_pos: Ending position
            direction: Direction of passage
        """
        # Set passage in from_pos
        from_cell = cells[from_pos.y][from_pos.x]
        bit_pos = {
            Direction.NORTH: 3,
            Direction.SOUTH: 1,
            Direction.EAST: 2,
            Direction.WEST: 0,
        }[direction]
        from_cell.walls = from_cell.walls | (1 << bit_pos)

        # Set passage in to_pos (opposite direction)
        to_cell = cells[to_pos.y][to_pos.x]
        opposite_dir = direction.opposite()
        opposite_bit_pos = {
            Direction.NORTH: 3,
            Direction.SOUTH: 1,
            Direction.EAST: 2,
            Direction.WEST: 0,
        }[opposite_dir]
        to_cell.walls = to_cell.walls | (1 << opposite_bit_pos)

    def _apply_cost_map(
        self,
        cells: List[List[Cell]],
        cost_map: CostMapType,
        cost_range: Tuple[int, int],
    ) -> None:
        """
        Apply cost distribution to all cells.

        Parameters:
            cells: Maze grid
            cost_map: Type of cost distribution
            cost_range: (min_cost, max_cost)
        """
        if cost_map == CostMapType.UNIFORM:
            self._apply_uniform_costs(cells, cost_range[0])
        elif cost_map == CostMapType.RANDOM:
            self._apply_random_costs(cells, cost_range)
        elif cost_map == CostMapType.HEATMAP:
            self._apply_heatmap_costs(cells, cost_range)

    def _apply_uniform_costs(self, cells: List[List[Cell]], cost: int) -> None:
        """Set all cells to same cost."""
        for row in cells:
            for cell in row:
                cell.cost = float(cost)

    def _apply_random_costs(
        self, cells: List[List[Cell]], cost_range: Tuple[int, int]
    ) -> None:
        """Set random cost for each cell."""
        min_cost, max_cost = cost_range
        for row in cells:
            for cell in row:
                cell.cost = float(self.rng.randint(min_cost, max_cost))

    def _apply_heatmap_costs(
        self, cells: List[List[Cell]], cost_range: Tuple[int, int]
    ) -> None:
        """
        Create smooth cost gradient (heatmap).

        Simulates terrain with smooth difficulty regions.
        """
        min_cost, max_cost = cost_range

        # Simple heatmap: distance from center scaled to cost range
        center_x, center_y = self.width / 2, self.height / 2
        max_distance = ((self.width / 2) ** 2 + (self.height / 2) ** 2) ** 0.5

        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                # Distance from center
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                # Normalize to [0, 1]
                normalized = dist / max_distance
                # Scale to cost range
                cost = min_cost + (normalized * (max_cost - min_cost))
                cell.cost = float(int(cost))


class MazeValidator:
    """Validate maze properties and characteristics."""

    @staticmethod
    def is_connected(maze: Maze) -> bool:
        """
        Check if all reachable cells form one connected component.

        Parameters:
            maze: Maze to validate

        Returns:
            True if connected, False otherwise
        """
        visited = set()
        stack = [maze.start]

        while stack:
            pos = stack.pop()
            if (pos.x, pos.y) in visited:
                continue

            visited.add((pos.x, pos.y))

            for direction in maze.get_neighbors(pos):
                next_pos = pos.move(direction)
                if (next_pos.x, next_pos.y) not in visited:
                    stack.append(next_pos)

        return (maze.goal.x, maze.goal.y) in visited

    @staticmethod
    def count_solutions(maze: Maze, max_solutions: int = 100) -> int:
        """
        Count number of paths from start to goal.

        Parameters:
            maze: Maze to analyze
            max_solutions: Stop counting after this many solutions

        Returns:
            Number of distinct paths (capped at max_solutions)
        """
        count = [0]

        def dfs(pos: Position, visited: Set[Tuple[int, int]]) -> None:
            if pos == maze.goal:
                count[0] += 1
                return

            if count[0] >= max_solutions:
                return

            for direction in maze.get_neighbors(pos):
                next_pos = pos.move(direction)
                if (next_pos.x, next_pos.y) not in visited:
                    visited.add((next_pos.x, next_pos.y))
                    dfs(next_pos, visited)
                    visited.remove((next_pos.x, next_pos.y))

        visited = {(maze.start.x, maze.start.y)}
        dfs(maze.start, visited)
        return count[0]

    @staticmethod
    def count_dead_ends(maze: Maze) -> int:
        """
        Count cells with only one passage (dead ends).

        Parameters:
            maze: Maze to analyze

        Returns:
            Number of dead-end cells
        """
        count = 0
        for y in range(maze.height):
            for x in range(maze.width):
                pos = Position(x, y)
                neighbors = maze.get_neighbors(pos)
                if len(neighbors) == 1:
                    count += 1
        return count
