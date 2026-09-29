"""Maze simulator - runs agents and records metrics."""

import time
from typing import Dict, Any, List

from .agent import Agent
from .models import Maze, Observation, Direction, MazeResult
from .wasm_solver import solve_maze as wasm_solve_maze
from .gui_visualizer import MazeGUIVisualizer


class Simulator:
    """
    Run an agent on a maze and collect metrics.

    Handles step-by-step execution, validation, and evaluation.
    """

    def __init__(self, maze: Maze, agent: Agent, max_steps: int = 10000,
                 visualize: bool = False, speed: float = 1.0):
        """
        Initialize simulator.

        Parameters:
            maze: Maze to solve
            agent: Agent to run
            max_steps: Maximum steps before timeout
            visualize: Whether to show maze visualization
            speed: Animation speed (higher = faster)
        """
        self.maze = maze
        self.agent = agent
        self.max_steps = max_steps
        self.visualize = visualize
        self.speed = speed
        self.visualizer = MazeGUIVisualizer(maze) if visualize else None

    def run(self, record_trace: bool = True) -> MazeResult:
        """
        Run agent on maze.

        Parameters:
            record_trace: Whether to record execution trace

        Returns:
            MazeResult with metrics
        """
        start_time = time.time()
        trace = []
        position = self.maze.start
        path_cost = 0.0
        steps = 0
        nodes_explored = set()
        invalid_moves = 0

        # Show initial maze
        if self.visualize:
            self.visualizer.show(position, self.speed)

        while steps < self.max_steps:
            # Create observation
            observation = Observation(
                maze=self.maze,
                current=position,
                goal=self.maze.goal,
                step_count=steps,
                path_cost=path_cost,
            )

            # Get agent's decision
            try:
                direction = self.agent.step(observation)
            except Exception as e:
                # Agent error
                if self.visualize:
                    self.visualizer.close()
                return MazeResult(
                    solved=False,
                    steps=steps,
                    path_cost=path_cost,
                    optimal_cost=0.0,
                    nodes_explored=len(nodes_explored),
                    execution_time_ms=(time.time() - start_time) * 1000,
                    invalid_moves=invalid_moves,
                    agent_name=self.agent.__class__.__name__,
                )

            # Validate move
            if not isinstance(direction, Direction):
                invalid_moves += 1
                steps += 1
                continue

            if not self.maze.can_move_to(position, direction):
                invalid_moves += 1
                steps += 1
                continue

            # Execute move
            new_pos = position.move(direction)
            cell_cost = self.maze.get_cell(new_pos).cost
            path_cost += cell_cost
            position = new_pos
            nodes_explored.add((position.x, position.y))
            steps += 1

            # Visualize
            if self.visualize:
                self.visualizer.record_step(position)
                self.visualizer.update_metrics(steps, path_cost)
                self.visualizer.show(position, self.speed)

            # Record trace
            if record_trace:
                debug = self.agent.debug_state()
                trace.append({
                    "step": steps,
                    "position": [position.x, position.y],
                    "action": str(direction),
                    "path_cost": path_cost,
                    "nodes_explored": len(nodes_explored),
                })

            # Check if solved
            if position == self.maze.goal:
                execution_time = (time.time() - start_time) * 1000

                # Get optimal solution using WASM reference solver
                try:
                    walls = [self.maze.cells[y][x].walls
                            for y in range(self.maze.height)
                            for x in range(self.maze.width)]
                    costs = [float(self.maze.cells[y][x].cost)
                            for y in range(self.maze.height)
                            for x in range(self.maze.width)]

                    optimal_solved, optimal_path, optimal_cost, _ = wasm_solve_maze(
                        self.maze.width, self.maze.height,
                        self.maze.start.x, self.maze.start.y,
                        self.maze.goal.x, self.maze.goal.y,
                        walls, costs
                    )
                except Exception as e:
                    # WASM solver not available, use 0 as reference
                    optimal_solved = False
                    optimal_cost = 0.0

                if self.visualize:
                    self.visualizer.close()

                return MazeResult(
                    solved=True,
                    steps=steps,
                    path_cost=path_cost,
                    optimal_cost=optimal_cost if optimal_solved else 0.0,
                    nodes_explored=len(nodes_explored),
                    execution_time_ms=execution_time,
                    invalid_moves=invalid_moves,
                    maze_seed=self.maze.seed,
                    agent_name=self.agent.__class__.__name__,
                    trace=trace,
                )

        # Timeout
        execution_time = (time.time() - start_time) * 1000
        if self.visualize:
            self.visualizer.close()
        return MazeResult(
            solved=False,
            steps=steps,
            path_cost=path_cost,
            optimal_cost=0.0,
            nodes_explored=len(nodes_explored),
            execution_time_ms=execution_time,
            invalid_moves=invalid_moves,
            agent_name=self.agent.__class__.__name__,
            trace=trace,
        )
