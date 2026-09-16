"""Maze file format (.maze) - parser and serializer."""

from typing import List
import json

from .models import Maze, Cell, Position


class MazeFormat:
    """
    Parse and serialize mazes to `.maze` text format.

    Format:
    ```
    SIZE <width> <height>
    SEED <seed>
    START <x> <y>
    GOAL <x> <y>

    TOPOLOGY
    <4-bit walls per cell, space-separated>

    COSTS
    <float cost per cell, space-separated>
    ```
    """

    @staticmethod
    def save(maze: Maze, filepath: str) -> None:
        """
        Save maze to .maze file.

        Parameters:
            maze: Maze to save
            filepath: Output file path
        """
        lines = []

        # Header
        lines.append(f"SIZE {maze.width} {maze.height}")
        lines.append(f"SEED {maze.seed}")
        lines.append(f"START {maze.start.x} {maze.start.y}")
        lines.append(f"GOAL {maze.goal.x} {maze.goal.y}")
        lines.append("")

        # Topology (4-bit walls per cell)
        lines.append("TOPOLOGY")
        topology_values = []
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                topology_values.append(f"{cell.walls:04b}")
        lines.append(" ".join(topology_values))
        lines.append("")

        # Costs
        lines.append("COSTS")
        cost_values = []
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                cost_values.append(str(cell.cost))
        lines.append(" ".join(cost_values))

        with open(filepath, "w") as f:
            f.write("\n".join(lines))

    @staticmethod
    def load(filepath: str) -> Maze:
        """
        Load maze from .maze file.

        Parameters:
            filepath: Input file path

        Returns:
            Loaded Maze object

        Raises:
            ValueError: If file format is invalid
        """
        with open(filepath, "r") as f:
            content = f.read()

        lines = content.strip().split("\n")
        idx = 0

        # Parse header
        metadata = {}
        while idx < len(lines) and lines[idx].strip():
            parts = lines[idx].strip().split()
            if parts[0] == "SIZE":
                metadata["width"] = int(parts[1])
                metadata["height"] = int(parts[2])
            elif parts[0] == "SEED":
                metadata["seed"] = int(parts[1])
            elif parts[0] == "START":
                metadata["start"] = Position(int(parts[1]), int(parts[2]))
            elif parts[0] == "GOAL":
                metadata["goal"] = Position(int(parts[1]), int(parts[2]))
            idx += 1

        # Skip blank lines
        while idx < len(lines) and not lines[idx].strip():
            idx += 1

        # Parse TOPOLOGY
        if idx < len(lines) and lines[idx].strip() == "TOPOLOGY":
            idx += 1
            topology_line = lines[idx].strip()
            topology_values = topology_line.split()
            cells_topology = [int(v, 2) for v in topology_values]
            idx += 1
        else:
            raise ValueError("Missing TOPOLOGY section")

        # Skip blank lines
        while idx < len(lines) and not lines[idx].strip():
            idx += 1

        # Parse COSTS
        if idx < len(lines) and lines[idx].strip() == "COSTS":
            idx += 1
            costs_line = lines[idx].strip()
            costs_values = costs_line.split()
            cells_costs = [float(v) for v in costs_values]
        else:
            raise ValueError("Missing COSTS section")

        # Build cell grid
        width = metadata["width"]
        height = metadata["height"]
        cells = []

        idx_cell = 0
        for y in range(height):
            row = []
            for x in range(width):
                cell = Cell(
                    walls=cells_topology[idx_cell],
                    cost=cells_costs[idx_cell],
                )
                row.append(cell)
                idx_cell += 1
            cells.append(row)

        return Maze(
            width=width,
            height=height,
            cells=cells,
            start=metadata["start"],
            goal=metadata["goal"],
            seed=metadata["seed"],
        )

    @staticmethod
    def save_json(maze: Maze, filepath: str) -> None:
        """
        Save maze to JSON format (for debugging).

        Parameters:
            maze: Maze to save
            filepath: Output file path
        """
        data = {
            "width": maze.width,
            "height": maze.height,
            "seed": maze.seed,
            "start": {"x": maze.start.x, "y": maze.start.y},
            "goal": {"x": maze.goal.x, "y": maze.goal.y},
            "cells": [],
        }

        for y in range(maze.height):
            row = []
            for x in range(maze.width):
                cell = maze.cells[y][x]
                row.append({
                    "walls": cell.walls,
                    "walls_binary": f"{cell.walls:04b}",
                    "cost": cell.cost,
                })
            data["cells"].append(row)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
