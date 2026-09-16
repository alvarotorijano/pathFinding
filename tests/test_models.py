"""
Tests for core data models.

Tests verify instantiation, properties, and methods of all data models.
"""

import pytest
from utils.maze_core.models import (
    Direction,
    Position,
    Cell,
    Maze,
    Observation,
    AgentDebugState,
    MazeResult,
)


class TestDirection:
    """Test Direction enum."""

    def test_all_directions_exist(self):
        """Test that all four cardinal directions exist."""
        assert Direction.NORTH is not None
        assert Direction.SOUTH is not None
        assert Direction.EAST is not None
        assert Direction.WEST is not None

    def test_direction_deltas(self):
        """Test direction delta values."""
        assert Direction.NORTH.delta == (0, -1)
        assert Direction.SOUTH.delta == (0, 1)
        assert Direction.EAST.delta == (1, 0)
        assert Direction.WEST.delta == (-1, 0)

    def test_opposite_direction(self):
        """Test getting opposite directions."""
        assert Direction.NORTH.opposite() == Direction.SOUTH
        assert Direction.SOUTH.opposite() == Direction.NORTH
        assert Direction.EAST.opposite() == Direction.WEST
        assert Direction.WEST.opposite() == Direction.EAST

    def test_direction_string(self):
        """Test string representation of directions."""
        assert str(Direction.NORTH) == "NORTH"
        assert str(Direction.SOUTH) == "SOUTH"


class TestPosition:
    """Test Position class."""

    def test_position_creation(self):
        """Test creating a position."""
        pos = Position(5, 10)
        assert pos.x == 5
        assert pos.y == 10

    def test_position_move(self):
        """Test moving a position."""
        pos = Position(5, 5)

        north = pos.move(Direction.NORTH)
        assert north.x == 5 and north.y == 4

        south = pos.move(Direction.SOUTH)
        assert south.x == 5 and south.y == 6

        east = pos.move(Direction.EAST)
        assert east.x == 6 and east.y == 5

        west = pos.move(Direction.WEST)
        assert west.x == 4 and west.y == 5

    def test_position_distance(self):
        """Test Manhattan distance calculation."""
        pos1 = Position(0, 0)
        pos2 = Position(3, 4)

        assert pos1.distance_to(pos2) == 7
        assert pos2.distance_to(pos1) == 7
        assert pos1.distance_to(pos1) == 0

    def test_position_hashable(self):
        """Test that positions can be used in sets."""
        pos1 = Position(5, 5)
        pos2 = Position(5, 5)
        pos3 = Position(6, 6)

        s = {pos1, pos2, pos3}
        assert len(s) == 2  # pos1 and pos2 are equal
        assert pos1 in s
        assert pos3 in s

    def test_position_equality(self):
        """Test position equality."""
        pos1 = Position(5, 5)
        pos2 = Position(5, 5)
        pos3 = Position(6, 6)

        assert pos1 == pos2
        assert pos1 != pos3
        assert pos1 != "not a position"

    def test_position_to_tuple(self):
        """Test converting position to tuple."""
        pos = Position(3, 7)
        assert pos.to_tuple() == (3, 7)


class TestCell:
    """Test Cell class."""

    def test_cell_creation(self):
        """Test creating a cell."""
        cell = Cell(walls=0b1010, cost=2.5)
        assert cell.walls == 0b1010
        assert cell.cost == 2.5

    def test_cell_default_cost(self):
        """Test cell default cost."""
        cell = Cell(walls=0b1111)
        assert cell.cost == 1.0

    def test_has_wall(self):
        """Test checking for walls."""
        cell = Cell(walls=0b1010)  # N=1, E=0, S=1, W=0 (1=passage open, 0=wall)

        assert not cell.has_wall(Direction.NORTH)  # Passage open (1)
        assert cell.has_wall(Direction.EAST)  # Wall (0)
        assert not cell.has_wall(Direction.SOUTH)  # Passage open (1)
        assert cell.has_wall(Direction.WEST)  # Wall (0)

    def test_can_move(self):
        """Test checking if movement is possible."""
        cell = Cell(walls=0b1010)  # N=1 (open), E=0 (wall), S=1 (open), W=0 (wall)

        assert cell.can_move(Direction.NORTH)  # Passage open
        assert not cell.can_move(Direction.EAST)  # Wall blocks
        assert cell.can_move(Direction.SOUTH)  # Passage open
        assert not cell.can_move(Direction.WEST)  # Wall blocks

    def test_cell_all_open(self):
        """Test cell with all passages open."""
        cell = Cell(walls=0b1111)

        assert not cell.has_wall(Direction.NORTH)
        assert not cell.has_wall(Direction.SOUTH)
        assert not cell.has_wall(Direction.EAST)
        assert not cell.has_wall(Direction.WEST)

    def test_cell_all_blocked(self):
        """Test cell with all walls."""
        cell = Cell(walls=0b0000)

        assert cell.has_wall(Direction.NORTH)
        assert cell.has_wall(Direction.SOUTH)
        assert cell.has_wall(Direction.EAST)
        assert cell.has_wall(Direction.WEST)


class TestMaze:
    """Test Maze class."""

    @pytest.fixture
    def simple_maze(self):
        """Create a simple 2x2 maze for testing."""
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

    def test_maze_creation(self, simple_maze):
        """Test creating a maze."""
        assert simple_maze.width == 2
        assert simple_maze.height == 2
        assert simple_maze.start == Position(0, 0)
        assert simple_maze.goal == Position(1, 1)
        assert simple_maze.seed == 42

    def test_get_cell_valid(self, simple_maze):
        """Test getting a cell within bounds."""
        cell = simple_maze.get_cell(Position(0, 0))
        assert cell is not None
        assert isinstance(cell, Cell)

    def test_get_cell_out_of_bounds(self, simple_maze):
        """Test getting a cell outside bounds."""
        cell = simple_maze.get_cell(Position(10, 10))
        assert cell is None

    def test_is_valid_bounds(self, simple_maze):
        """Test bounds checking."""
        assert simple_maze.is_valid(Position(0, 0))
        assert simple_maze.is_valid(Position(1, 1))
        assert not simple_maze.is_valid(Position(-1, 0))
        assert not simple_maze.is_valid(Position(2, 2))

    def test_can_move_to(self, simple_maze):
        """Test movement validation."""
        # Cell at (0,0) has walls 0b1010 (N=open, E=wall, S=open, W=wall)
        # But (0,0) is at boundary, so can't move NORTH (out of bounds)
        # Can move SOUTH to (0,1) which is in bounds

        assert not simple_maze.can_move_to(Position(0, 0), Direction.EAST)  # Wall
        assert not simple_maze.can_move_to(Position(0, 0), Direction.NORTH)  # Out of bounds
        assert not simple_maze.can_move_to(Position(0, 0), Direction.WEST)  # Wall
        assert simple_maze.can_move_to(Position(0, 0), Direction.SOUTH)  # Open and in bounds

    def test_can_move_out_of_bounds(self, simple_maze):
        """Test movement to out-of-bounds position."""
        # Can't move north from (0, 0) even if wall is open
        assert not simple_maze.can_move_to(Position(0, 0), Direction.NORTH)

    def test_get_neighbors(self, simple_maze):
        """Test getting valid neighbor directions."""
        neighbors = simple_maze.get_neighbors(Position(0, 0))
        # walls are 0b1010 (N=open, E=wall, S=open, W=wall)
        # But can't go NORTH or SOUTH because they're out of bounds at y<0 and y>1
        assert Direction.NORTH not in neighbors  # Out of bounds
        assert Direction.SOUTH in neighbors  # Open, in bounds
        assert Direction.EAST not in neighbors  # Wall
        assert Direction.WEST not in neighbors  # Wall


class TestObservation:
    """Test Observation class."""

    def test_observation_creation(self):
        """Test creating an observation."""
        cells = [[Cell(0b1111, 1)]]
        maze = Maze(
            width=1,
            height=1,
            cells=cells,
            start=Position(0, 0),
            goal=Position(0, 0),
            seed=1,
        )

        obs = Observation(
            maze=maze,
            current=Position(0, 0),
            goal=Position(0, 0),
            step_count=5,
            path_cost=10.5,
        )

        assert obs.current == Position(0, 0)
        assert obs.step_count == 5
        assert obs.path_cost == 10.5

    def test_observation_defaults(self):
        """Test observation default values."""
        cells = [[Cell(0b1111, 1)]]
        maze = Maze(
            width=1,
            height=1,
            cells=cells,
            start=Position(0, 0),
            goal=Position(0, 0),
            seed=1,
        )

        obs = Observation(maze=maze, current=Position(0, 0), goal=Position(0, 0))

        assert obs.step_count == 0
        assert obs.path_cost == 0.0


class TestAgentDebugState:
    """Test AgentDebugState class."""

    def test_debug_state_creation(self):
        """Test creating debug state."""
        debug = AgentDebugState(
            frontier={Position(0, 0)},
            explored={Position(1, 1)},
        )

        assert len(debug.frontier) == 1
        assert len(debug.explored) == 1
        assert len(debug.discovered) == 0
        assert len(debug.current_path) == 0

    def test_debug_state_defaults(self):
        """Test debug state default values."""
        debug = AgentDebugState()

        assert isinstance(debug.frontier, set)
        assert isinstance(debug.explored, set)
        assert isinstance(debug.discovered, set)
        assert isinstance(debug.current_path, list)
        assert isinstance(debug.metadata, dict)


class TestMazeResult:
    """Test MazeResult class."""

    def test_result_creation(self):
        """Test creating a result."""
        result = MazeResult(
            solved=True,
            steps=100,
            path_cost=150.0,
            optimal_cost=140.0,
            nodes_explored=300,
            execution_time_ms=5.2,
        )

        assert result.solved
        assert result.steps == 100
        assert result.path_cost == 150.0

    def test_optimality_ratio(self):
        """Test optimality ratio calculation."""
        result = MazeResult(
            solved=True,
            steps=100,
            path_cost=150.0,
            optimal_cost=100.0,
            nodes_explored=300,
            execution_time_ms=5.0,
        )

        assert abs(result.optimality_ratio - (100.0 / 150.0)) < 0.001

    def test_optimality_percentage(self):
        """Test optimality percentage calculation."""
        result = MazeResult(
            solved=True,
            steps=100,
            path_cost=150.0,
            optimal_cost=100.0,
            nodes_explored=300,
            execution_time_ms=5.0,
        )

        expected = (100.0 / 150.0) * 100
        assert abs(result.optimality_percentage - expected) < 0.1

    def test_optimality_unsolved(self):
        """Test optimality ratio when not solved."""
        result = MazeResult(
            solved=False,
            steps=100,
            path_cost=0.0,
            optimal_cost=100.0,
            nodes_explored=300,
            execution_time_ms=5.0,
        )

        assert result.optimality_ratio == 0.0
        assert result.optimality_percentage == 0.0

    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        result = MazeResult(
            solved=True,
            steps=50,
            path_cost=100.0,
            optimal_cost=90.0,
            nodes_explored=150,
            execution_time_ms=2.5,
            maze_seed=123,
            agent_name="test_agent",
        )

        d = result.to_dict()

        assert d["solved"] is True
        assert d["steps"] == 50
        assert d["path_cost"] == 100.0
        assert "optimality_ratio" in d
        assert d["agent_name"] == "test_agent"

    def test_result_to_json(self):
        """Test converting result to JSON string."""
        result = MazeResult(
            solved=True,
            steps=50,
            path_cost=100.0,
            optimal_cost=90.0,
            nodes_explored=150,
            execution_time_ms=2.5,
        )

        json_str = result.to_json()

        assert isinstance(json_str, str)
        assert "solved" in json_str
        assert "steps" in json_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
