"""Tests for maze generation."""

import pytest
from utils.maze_core.generator import (
    MazeGenerator,
    TopologyType,
    CostMapType,
    MazeValidator,
)
from utils.maze_core.models import Position


class TestMazeGenerator:
    """Test maze generation."""

    def test_generator_creation(self):
        """Test creating a generator."""
        gen = MazeGenerator(20, 20, seed=42)
        assert gen.width == 20
        assert gen.height == 20
        assert gen.seed == 42

    def test_invalid_dimensions(self):
        """Test invalid maze dimensions."""
        with pytest.raises(ValueError):
            MazeGenerator(0, 10, seed=42)
        with pytest.raises(ValueError):
            MazeGenerator(10, 0, seed=42)
        with pytest.raises(ValueError):
            MazeGenerator(-5, 10, seed=42)

    def test_generate_perfect(self):
        """Test perfect maze generation."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.PERFECT)

        assert maze.width == 10
        assert maze.height == 10
        assert maze.seed == 42
        assert maze.solution_count == 1

    def test_generate_open(self):
        """Test open maze generation."""
        gen = MazeGenerator(5, 5, seed=42)
        maze = gen.generate(topology=TopologyType.OPEN)

        # All cells should be accessible
        assert maze.width == 5
        assert maze.height == 5

    def test_custom_start_goal(self):
        """Test custom start and goal positions."""
        gen = MazeGenerator(10, 10, seed=42)
        start = Position(1, 1)
        goal = Position(8, 8)

        maze = gen.generate(
            topology=TopologyType.PERFECT,
            start=start,
            goal=goal,
        )

        assert maze.start == start
        assert maze.goal == goal

    def test_invalid_start_position(self):
        """Test invalid start position."""
        gen = MazeGenerator(10, 10, seed=42)
        with pytest.raises(ValueError):
            gen.generate(start=Position(100, 100))

    def test_uniform_costs(self):
        """Test uniform cost map."""
        gen = MazeGenerator(5, 5, seed=42)
        maze = gen.generate(
            topology=TopologyType.OPEN,
            cost_map=CostMapType.UNIFORM,
            cost_range=(5, 5),
        )

        # All cells should have cost 5
        for row in maze.cells:
            for cell in row:
                assert cell.cost == 5.0

    def test_random_costs(self):
        """Test random cost map."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(
            topology=TopologyType.PERFECT,
            cost_map=CostMapType.RANDOM,
            cost_range=(1, 10),
        )

        costs = set()
        for row in maze.cells:
            for cell in row:
                costs.add(cell.cost)
                assert 1.0 <= cell.cost <= 10.0

        # Should have variety (not all same)
        assert len(costs) > 1

    def test_heatmap_costs(self):
        """Test heatmap cost map."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(
            topology=TopologyType.PERFECT,
            cost_map=CostMapType.HEATMAP,
            cost_range=(1, 10),
        )

        for row in maze.cells:
            for cell in row:
                assert 1.0 <= cell.cost <= 10.0

    def test_reproducibility(self):
        """Test that same seed produces same maze."""
        gen1 = MazeGenerator(10, 10, seed=42)
        maze1 = gen1.generate(topology=TopologyType.PERFECT)

        gen2 = MazeGenerator(10, 10, seed=42)
        maze2 = gen2.generate(topology=TopologyType.PERFECT)

        # Same topology and costs
        for y in range(10):
            for x in range(10):
                assert maze1.cells[y][x].walls == maze2.cells[y][x].walls
                assert maze1.cells[y][x].cost == maze2.cells[y][x].cost

    def test_different_seeds_different_mazes(self):
        """Test that different seeds produce different mazes."""
        gen1 = MazeGenerator(10, 10, seed=1)
        maze1 = gen1.generate(topology=TopologyType.PERFECT)

        gen2 = MazeGenerator(10, 10, seed=2)
        maze2 = gen2.generate(topology=TopologyType.PERFECT)

        # Should be different (very unlikely to be same)
        walls_equal = all(
            maze1.cells[y][x].walls == maze2.cells[y][x].walls
            for y in range(10)
            for x in range(10)
        )
        assert not walls_equal


class TestMazeValidator:
    """Test maze validation."""

    def test_connected_perfect(self):
        """Test that perfect maze is connected."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.PERFECT)

        assert MazeValidator.is_connected(maze)

    def test_connected_open(self):
        """Test that open maze is connected."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.OPEN)

        assert MazeValidator.is_connected(maze)

    def test_unsolvable_not_connected(self):
        """Test that unsolvable maze is not connected."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.UNSOLVABLE)

        assert not MazeValidator.is_connected(maze)

    def test_count_solutions(self):
        """Test solution counting."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.PERFECT)

        solutions = MazeValidator.count_solutions(maze)
        assert solutions >= 1

    def test_count_dead_ends(self):
        """Test dead-end counting."""
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.PERFECT)

        dead_ends = MazeValidator.count_dead_ends(maze)
        assert dead_ends >= 0
        assert dead_ends < maze.width * maze.height


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
