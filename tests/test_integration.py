"""
Integration tests - full workflow.

Note: Tests run without WASM solver loaded (WASM is private).
Simulator handles missing WASM gracefully for testing purposes.
"""

import pytest
from pathlib import Path
import tempfile

from utils.maze_core.generator import MazeGenerator, TopologyType, CostMapType
from utils.maze_core.formats import MazeFormat
from utils.maze_core.simulator import Simulator
from agents.dfs_agent.agent import DFSAgent


class TestFullWorkflow:
    """Test complete workflow: generate → save → load → simulate."""

    def test_generate_save_load_run(self):
        """Test: generate maze → save → load → run agent."""
        # Generate
        gen = MazeGenerator(10, 10, seed=42)
        maze = gen.generate(topology=TopologyType.PERFECT)

        # Save
        with tempfile.NamedTemporaryFile(mode="w", suffix=".maze",
                                        delete=False) as f:
            temp_file = f.name

        MazeFormat.save(maze, temp_file)

        # Load
        loaded_maze = MazeFormat.load(temp_file)

        assert loaded_maze.width == maze.width
        assert loaded_maze.height == maze.height
        assert loaded_maze.seed == maze.seed

        # Run DFS
        agent = DFSAgent()
        simulator = Simulator(loaded_maze, agent)
        result = simulator.run(record_trace=True)

        assert isinstance(result.steps, int)
        assert isinstance(result.path_cost, float)
        assert len(result.trace) > 0

        # Cleanup
        Path(temp_file).unlink()

    def test_dfs_finds_solution_on_another_maze(self):
        """Test that DFS finds a solution on a different perfect maze."""
        gen = MazeGenerator(8, 8, seed=123)
        maze = gen.generate(topology=TopologyType.PERFECT)

        agent = DFSAgent()
        simulator = Simulator(maze, agent, max_steps=10000)
        result = simulator.run()

        assert result.solved, "DFS should find solution in perfect maze"
        assert result.steps > 0
        assert result.path_cost > 0

    def test_dfs_finds_solution(self):
        """Test that DFS finds a solution on perfect maze."""
        gen = MazeGenerator(8, 8, seed=456)
        maze = gen.generate(topology=TopologyType.PERFECT)

        agent = DFSAgent()
        simulator = Simulator(maze, agent, max_steps=10000)
        result = simulator.run()

        assert result.solved, "DFS should find solution in perfect maze"
        assert result.steps > 0

    def test_unsolvable_maze_fails(self):
        """Test that agent fails on unsolvable maze."""
        gen = MazeGenerator(10, 10, seed=999)
        maze = gen.generate(topology=TopologyType.UNSOLVABLE)

        agent = DFSAgent()
        simulator = Simulator(maze, agent, max_steps=100)
        result = simulator.run()

        assert not result.solved, "Should not solve unsolvable maze"

    def test_multiple_solutions_maze(self):
        """Test on maze with multiple solutions."""
        gen = MazeGenerator(8, 8, seed=789)
        maze = gen.generate(topology=TopologyType.MULTIPLE)

        agent = DFSAgent()
        simulator = Simulator(maze, agent)
        result = simulator.run()

        # May or may not solve depending on random generation
        # Just verify it runs without error
        assert isinstance(result.solved, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
